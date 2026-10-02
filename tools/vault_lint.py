"""Read-only vault lint: duplicates, filename collisions, domains, broken links, orphans.

    python tools/vault_lint.py            # writes docs/lint-report.md and prints a summary
    python tools/vault_lint.py --stdout   # print the full report instead

It never modifies wiki/. Suggested domains for unclassified notes are proposals only; nothing is applied.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ingest  # noqa: E402

WIKI = ingest.WIKI_DIR
REPORT = ingest.VAULT_ROOT / "docs" / "lint-report.md"

WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
MDLINK = re.compile(r"\]\(([^)\s]+\.md)(?:#[^)]*)?\)")

KEYWORDS = {
    "fine-art": ("art", "artist", "modernis", "museum", "painting", "gallery", "sculpture", "biennale", "curat",
                 "collection", "sea-", "singapore", "aesthetic", "avant", "exhibition"),
    "derivatives": ("option", "volatil", "gamma", "gex", "greek", "regime", "hmm", "markov", "garch", "delta",
                    "skew", "vix", "theta", "vega", "implied", "dealer", "straddle", "spread", "maopm", "dispersion",
                    "black-scholes", "bsm", "surface", "0dte", "hedg"),
    "cl-market-making": ("amm", "uniswap", "dlmm", "meteora", "orca", "whirlpool", "liquidity-pool", "lvr",
                         "impermanent", "concentrated", "funding", "perpetual", "market-making", "inventory",
                         "avellaneda", "glosten", "kyle"),
    "meta": ("vault", "obsidian", "ingestion", "dataview", "template"),
}


def notes() -> list[Path]:
    return sorted(WIKI.rglob("*.md"))


def read(path: Path) -> tuple[dict, str]:
    try:
        return ingest.split_frontmatter(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError):
        return {}, ""


def link_targets(path: Path, body: str, by_stem: dict[str, list[Path]]) -> tuple[set[Path], list[str]]:
    """Resolved link targets of a note, and the raw text of links that resolve to nothing."""
    found: set[Path] = set()
    broken: list[str] = []
    for raw in WIKILINK.findall(body):
        stem = ingest.slugify(Path(raw.strip()).name)
        hits = by_stem.get(stem)
        if hits:
            found.add(hits[0])
        else:
            broken.append(raw.strip())
    for raw in MDLINK.findall(body):
        target = (path.parent / raw).resolve()
        if target.exists():
            found.add(target)
        else:
            hits = by_stem.get(ingest.slugify(Path(raw).name))
            if hits:
                found.add(hits[0])
            else:
                broken.append(raw)
    return found, broken


def suggest_domain(path: Path, fm: dict, neighbours: list[str]) -> tuple[str, str]:
    text = " ".join([path.stem.lower()] + [str(t).lower() for t in ingest._as_list(fm.get("tags"))])
    scores = {d: sum(k in text for k in kws) for d, kws in KEYWORDS.items()}
    best = max(scores, key=scores.get)
    if scores[best] > 0:
        return best, "keywords"
    counted = Counter(n for n in neighbours if n in ingest.DOMAINS)
    if counted:
        return counted.most_common(1)[0][0], "neighbours"
    return "?", "no signal"


def build_report() -> tuple[str, dict]:
    files = notes()
    meta = {p: read(p) for p in files}
    by_stem: dict[str, list[Path]] = defaultdict(list)
    by_name: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        by_stem[ingest.slugify(p.name)].append(p)
        by_name[p.stem.lower()].append(p)

    rel = lambda p: p.relative_to(ingest.VAULT_ROOT).as_posix()  # noqa: E731
    slug_collisions = {k: v for k, v in by_stem.items() if len(v) > 1}
    basename_collisions = {k: v for k, v in by_name.items() if len({x.parent for x in v}) > 1}

    domains = Counter()
    unclassified = []
    for p, (fm, _) in meta.items():
        d = fm.get("domain")
        if d in ingest.DOMAINS:
            domains[d] += 1
        else:
            domains["(missing)" if d in (None, "") else f"(invalid: {d})"] += 1
            unclassified.append(p)

    incoming: dict[Path, int] = defaultdict(int)
    broken_by_note: dict[Path, list[str]] = {}
    outgoing: dict[Path, set[Path]] = {}
    for p, (fm, body) in meta.items():
        targets, broken = link_targets(p, body, by_stem)
        targets.discard(p)
        outgoing[p] = targets
        for t in targets:
            incoming[t.resolve()] += 1
        if broken:
            broken_by_note[p] = broken
    orphans = [p for p in files if incoming.get(p.resolve(), 0) == 0 and not outgoing.get(p)]

    lines = [f"# Vault lint report — {date.today().isoformat()}", "",
             f"Read-only. {len(files)} notes under `wiki/`.", ""]
    lines += ["## Domains", "", "| domain | notes |", "|---|---:|"]
    lines += [f"| {d} | {n} |" for d, n in domains.most_common()]
    lines += ["", f"## Slug collisions ({len(slug_collisions)})", "",
              "Different file names that slug to the same name — candidates for `tools/merge_notes.py`.", ""]
    for k, v in sorted(slug_collisions.items()):
        lines.append(f"- `{k}`: " + ", ".join(f"`{rel(x)}`" for x in v))
    lines += ["", f"## Same file name in different folders ({len(basename_collisions)})", "",
              "These make `[[name]]` links ambiguous.", ""]
    for k, v in sorted(basename_collisions.items()):
        lines.append(f"- `{k}`: " + ", ".join(f"`{rel(x)}`" for x in v))
    total_broken = sum(len(v) for v in broken_by_note.values())
    lines += ["", f"## Broken links ({total_broken} in {len(broken_by_note)} notes)", ""]
    for p, b in sorted(broken_by_note.items()):
        shown = ", ".join(f"`{x}`" for x in b[:8]) + (f" … +{len(b) - 8}" if len(b) > 8 else "")
        lines.append(f"- `{rel(p)}`: {shown}")
    lines += ["", f"## Orphans — no links in or out ({len(orphans)})", ""]
    lines += [f"- `{rel(p)}`" for p in orphans]
    lines += ["", f"## Suggested domains for {len(unclassified)} unclassified notes (proposal only, not applied)", "",
              "| note | suggestion | basis |", "|---|---|---|"]
    suggestions = Counter()
    for p in unclassified:
        fm, _ = meta[p]
        neighbour_domains = [meta[t][0].get("domain") for t in outgoing.get(p, ()) if t in meta]
        s, basis = suggest_domain(p, fm, neighbour_domains)
        suggestions[s] += 1
        lines.append(f"| `{rel(p)}` | {s} | {basis} |")
    summary = {
        "notes": len(files),
        "slug_collisions": len(slug_collisions),
        "basename_collisions": len(basename_collisions),
        "broken_links": total_broken,
        "orphans": len(orphans),
        "unclassified": len(unclassified),
        "suggested": dict(suggestions),
    }
    return "\n".join(lines) + "\n", summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only vault lint")
    parser.add_argument("--stdout", action="store_true", help="print the report instead of writing docs/lint-report.md")
    args = parser.parse_args(argv)
    report, summary = build_report()
    if args.stdout:
        print(report)
    else:
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(report, encoding="utf-8")
        print(f"Wrote {REPORT.relative_to(ingest.VAULT_ROOT).as_posix()}")
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
