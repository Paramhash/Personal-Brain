"""Merge duplicate notes into one canonical note, and repoint every link to them.

    python tools/merge_notes.py --canonical wiki/concepts/gamma-exposure-gex.md \
        --merge wiki/concepts/gex.md wiki/concepts/gamma_exposure_gex.md          # dry run: prints the plan
    python tools/merge_notes.py ... --apply                                      # does it

For each merged note: its body is appended to the canonical note as '## Merged from <name>', its tags and aliases
are unioned in, and its old name (and title) become aliases of the canonical note. Every link to it, in both styles
used in this vault ([[path|label]] and [label](path.md)), is rewritten to the canonical note. Then the merged file is
deleted. Notes marked `bridge_managed: true` are refused. Commit before running with --apply.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import ingest  # noqa: E402

WIKILINK = re.compile(r"\[\[([^\]|#]+)((?:#[^\]|]*)?)((?:\|[^\]]*)?)\]\]")
MDLINK = re.compile(r"(\]\()([^)\s]+\.md)((?:#[^)]*)?\))")


def vault_path(arg: str) -> Path:
    p = (ingest.VAULT_ROOT / arg).resolve()
    if ingest.WIKI_DIR.resolve() not in p.parents:
        raise SystemExit(f"not under wiki/: {arg}")
    if not p.exists():
        raise SystemExit(f"not found: {arg}")
    return p


def title_of(body: str) -> str | None:
    m = re.search(r"^#\s+(.+)$", body, re.M)
    return m.group(1).strip() if m else None


def rewrite_links(text: str, linker: Path, old: Path, canonical: Path, old_label: str) -> tuple[str, int]:
    """Repoint links in `text` (a note at `linker`) from `old` to `canonical`. Returns (text, count).

    A link with no label gets `old_label` (the merged note's title), so what the reader sees does not change.
    """
    old_name = old.stem.lower()
    count = 0

    def names_old(raw: str) -> bool:
        # Obsidian resolves a link by file name, case-insensitively; '.md' is optional.
        name = Path(raw.strip().replace("\\", "/")).name
        name = name[:-3] if name.lower().endswith(".md") else name
        return name.lower() == old_name

    def new_target(raw: str) -> str:
        if "/" in raw or "\\" in raw:
            rel = os.path.relpath(canonical, linker.parent).replace("\\", "/")
            return rel if raw.lower().endswith(".md") else rel[:-3]
        return canonical.stem

    def wiki_sub(m: re.Match) -> str:
        nonlocal count
        raw, anchor, label = m.group(1), m.group(2), m.group(3)
        if not names_old(raw):
            return m.group(0)
        count += 1
        label = label or f"|{old_label}"
        return f"[[{new_target(raw.strip())}{anchor}{label}]]"

    def md_sub(m: re.Match) -> str:
        nonlocal count
        raw = m.group(2)
        target = (linker.parent / raw).resolve()
        if target != old.resolve():
            return m.group(0)
        count += 1
        return f"{m.group(1)}{new_target(raw)}{m.group(3)}"

    text = WIKILINK.sub(wiki_sub, text)
    text = MDLINK.sub(md_sub, text)
    return text, count


def plan_and_apply(canonical: Path, merges: list[Path], apply: bool) -> int:
    today = date.today().isoformat()
    can_text = canonical.read_text(encoding="utf-8")
    can_fm, _ = ingest.split_frontmatter(can_text)
    if can_fm.get("bridge_managed") is True:
        raise SystemExit(f"refusing: {canonical.name} is bridge_managed")
    rel = lambda p: p.relative_to(ingest.VAULT_ROOT).as_posix()  # noqa: E731
    print(f"canonical: {rel(canonical)}")

    for m in merges:
        if m.resolve() == canonical.resolve():
            raise SystemExit("a note cannot be merged into itself")
        m_text = m.read_text(encoding="utf-8")
        m_fm, m_body = ingest.split_frontmatter(m_text)
        if m_fm.get("bridge_managed") is True:
            raise SystemExit(f"refusing: {m.name} is bridge_managed")
        new_aliases = [m.stem] + ([title_of(m_body)] if title_of(m_body) else [])
        incoming = m_fm | {"aliases": ingest._as_list(m_fm.get("aliases")) + new_aliases}
        merged_text, changed = ingest.merge_note(can_text, ingest.render_frontmatter(incoming) + m_body,
                                                 f"merged note {m.name}", today)
        merged_text = merged_text.replace(f"{ingest.UPDATE_HEADING} merged note {m.name} ({today})",
                                          f"## Merged from {m.name} ({today})")
        if not changed:  # identical body: still carry the aliases over
            fm, body = ingest.split_frontmatter(can_text)
            fm["aliases"] = ingest._union(ingest._as_list(fm.get("aliases")), new_aliases)
            merged_text = ingest.render_frontmatter(fm) + body
        can_text = merged_text
        print(f"  merge {rel(m)}  (body {'appended' if changed else 'identical, aliases only'}; aliases + {new_aliases})")

    labels = {}
    for m in merges:
        _, m_body = ingest.split_frontmatter(m.read_text(encoding="utf-8"))
        labels[m] = title_of(m_body) or m.stem
    total_links = 0
    edits: dict[Path, str] = {}
    for note in sorted(ingest.WIKI_DIR.rglob("*.md")):
        if note in merges:
            continue
        text = can_text if note == canonical else note.read_text(encoding="utf-8")
        new = text
        for m in merges:
            new, n = rewrite_links(new, note, m, canonical, labels[m])
            total_links += n
        if new != text or note == canonical:
            edits[note] = new
    print(f"  links repointed: {total_links} in {len([n for n in edits if n != canonical])} notes")

    if not apply:
        print("dry run: nothing changed (add --apply)")
        return 0
    for note, text in edits.items():
        ingest.atomic_write(note, text)
    for m in merges:
        m.unlink()
    print("applied")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge duplicate notes into a canonical note")
    parser.add_argument("--canonical", required=True)
    parser.add_argument("--merge", nargs="+", required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    return plan_and_apply(vault_path(args.canonical), [vault_path(m) for m in args.merge], args.apply)


if __name__ == "__main__":
    sys.exit(main())
