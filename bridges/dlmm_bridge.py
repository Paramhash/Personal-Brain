"""Bridge: mirror dlmm-hedge-bot's curated documents into the vault. READ-ONLY on the bot repo.

    python bridges/dlmm_bridge.py              # dry run (default): print what would change
    python bridges/dlmm_bridge.py --apply      # write mirrors under wiki/dlmm/ and copy research to raw/
    python bridges/dlmm_bridge.py --only adr   # restrict to one kind: adr | blueprint | report | finding | raw

What it does (configured in bridges/dlmm_bridge.toml):
- ADRs, blueprints, CL policy reports and selected findings become verbatim mirror notes under wiki/dlmm/<kind>/,
  with provenance (source path, the commit that last changed the file, sha256, export time), `bridge_managed: true`
  (ingestion refuses to touch them) and `reviewed: true` (they are not inbox material). Links between bot documents
  and mentions of `ADR-0NN` become [[wikilinks]] to the mirrors.
- wiki/dlmm/adr-index.md is regenerated from the ADR headers (number, title, status, date).
- Research notes, the LVR paper and the delta-hedging page are copied to raw/ for Gemini concept extraction.

Safety: only files matching the config's globs are read; a hard denylist (env files, keys, C:/observation, node_modules)
applies on top; every text file is scanned for secrets and refused on a hit; only read-only git commands are run
against the bot repo (`rev-parse`, `log`, `status`). A ledger (bridges/.state/dlmm_ledger.json) skips unchanged files.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tomllib
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

VAULT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(VAULT))
import ingest  # noqa: E402

CONFIG = VAULT / "bridges" / "dlmm_bridge.toml"
LEDGER = VAULT / "bridges" / ".state" / "dlmm_ledger.json"
RAW_DIR = VAULT / "raw"
ADR_INDEX = VAULT / "wiki" / "dlmm" / "adr-index.md"
PREFIX = {"adr": "adr-", "blueprint": "blueprint-", "report": "", "finding": "finding-"}

DENY_GLOBS = ("*.env", ".env*", "*.key", "*.pem", "*keypair*.json", "*secret*", "*credential*")
DENY_PARTS = ("node_modules", ".git", "observation")
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"https://(?:ptb\.|canary\.)?discord(?:app)?\.com/api/webhooks/\d+/[\w-]+"),
    re.compile(r"(?i)\b(?:api[_-]?key|secret[_-]?key|private[_-]?key|access[_-]?token|webhook[_-]?url)\s*[=:]\s*['\"]?[A-Za-z0-9_\-/+]{20,}"),
    re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{86,90}\b"),  # base58 64-byte secret keys (public keys are 32-44 chars)
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b"),
]


# --------------------------------------------------------------------------------------------- pure helpers


def denied(rel: str) -> bool:
    parts = [part.lower() for part in Path(rel).parts]
    return any(part in DENY_PARTS for part in parts) or any(
        fnmatch.fnmatch(part, g) for part in parts for g in DENY_GLOBS
    )


def find_secret(text: str) -> str | None:
    for pat in SECRET_PATTERNS:
        m = pat.search(text)
        if m:
            return pat.pattern[:40]
    return None


def mirror_slug(kind: str, src: Path) -> str:
    stem = src.stem
    if kind == "adr":  # '052-ev-gate-...' -> 'adr-052-ev-gate-...'
        return "adr-" + ingest.slugify(stem)
    return PREFIX.get(kind, "") + ingest.slugify(stem)


def adr_number(src_name: str) -> str | None:
    m = re.match(r"^(\d{3})-", src_name)
    return m.group(1) if m else None


def rewrite_links(text: str, src_rel: str, targets: dict[str, str], adr_slugs: dict[str, str]) -> str:
    """Turn links between bot documents into [[mirror]] links, and plain 'ADR-0NN' mentions into links.

    `targets` maps a bot-relative path ('docs/architect/ev_policy.md') to its mirror slug; `adr_slugs` maps '052' to
    the ADR mirror's slug. Fenced code blocks and inline code are left untouched.
    """
    src_dir = Path(src_rel).parent

    def md_link(m: re.Match) -> str:
        label, href = m.group(1), m.group(2)
        anchor = ""
        if "#" in href:
            href, anchor = href.split("#", 1)
        resolved = (src_dir / href).as_posix()
        parts: list[str] = []
        for part in resolved.split("/"):
            if part == "..":
                if parts:
                    parts.pop()
            elif part not in (".", ""):
                parts.append(part)
        key = "/".join(parts)
        slug = targets.get(key)
        if slug is None:
            return m.group(0)
        return f"[[{slug}{'#' + anchor if anchor else ''}|{label}]]"

    def adr_mention(m: re.Match) -> str:
        slug = adr_slugs.get(m.group(1))
        return f"[[{slug}|{m.group(0)}]]" if slug else m.group(0)

    out: list[str] = []
    in_fence = False
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        pieces = line.split("`")
        for i in range(0, len(pieces), 2):  # even pieces are outside inline code
            seg = re.sub(r"\[([^\]]+)\]\(([^)\s]+\.md(?:#[^)]*)?)\)", md_link, pieces[i])
            seg = re.sub(r"(?<![\[\w|-])ADR-(\d{3})(?!\d)(?![^\[]*\]\])", adr_mention, seg)
            pieces[i] = seg
        out.append("`".join(pieces))
    return "".join(out)


def parse_adr_header(text: str) -> tuple[str, str, str]:
    """(title, status, date) from an ADR's first lines."""
    title = re.search(r"^#\s+(?:ADR-\d{3}\s*[—-]\s*)?(.+)$", text, re.M)
    status = re.search(r"^-\s+\*\*Status:\*\*\s*(.+)$", text, re.M)
    when = re.search(r"^-\s+\*\*Date:\*\*\s*(\S+)", text, re.M)
    clean = lambda s: re.sub(r"\*\*|`", "", s).strip()  # noqa: E731
    return (clean(title.group(1)) if title else "",
            clean(status.group(1))[:90] if status else "",
            when.group(1) if when else "")


def render_mirror(kind: str, src_rel: str, body: str, prov: dict, aliases: list[str]) -> str:
    fm = {
        "domain": "cl-market-making",
        "tags": ["dlmm-hedge-bot", kind],
        "aliases": aliases,
        "created": prov["exported_at"][:10],
        "reviewed": True,
        "bridge_managed": True,
        "source_path": f"dlmm-hedge-bot/development/{src_rel}",
        "bot_commit": prov["commit"],
        "source_sha256": prov["sha256"],
        "exported_at": prov["exported_at"],
    }
    callout = (f"> [!info] Read-only mirror of `dlmm-hedge-bot/development/{src_rel}` at commit `{prov['commit']}`. "
               f"Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.\n\n")
    return ingest.render_frontmatter(fm) + callout + body


# --------------------------------------------------------------------------------------------- side effects


def git(bot_root: Path, *args: str) -> str:
    """Read-only git query against the bot repo."""
    assert args[0] in ("rev-parse", "log", "status"), "the bridge runs read-only git commands only"
    out = subprocess.run(["git", "-C", str(bot_root), *args], capture_output=True, text=True, check=False)
    return out.stdout.strip()


def provenance(bot_root: Path, rel: str, data: bytes) -> dict:
    commit = git(bot_root, "log", "-1", "--format=%h", "--", rel) or "untracked"
    if git(bot_root, "status", "--porcelain", "--", rel):
        commit += "+dirty"
    return {
        "commit": commit,
        "sha256": hashlib.sha256(data).hexdigest(),
        "exported_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def load_ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {}


def save_ledger(ledger: dict) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(ledger, indent=1, sort_keys=True) + "\n", encoding="utf-8")


def expand(bot_root: Path, globs: list[str]) -> list[str]:
    found: list[str] = []
    for g in globs:
        for p in sorted(bot_root.glob(g)):
            if p.is_file():
                rel = p.relative_to(bot_root).as_posix()
                if not denied(rel) and rel not in found:
                    found.append(rel)
    return found


def run(apply: bool, only: str | None) -> int:
    cfg = tomllib.loads(CONFIG.read_text(encoding="utf-8"))
    bot_root = Path(cfg["bot_root"])
    if not (bot_root / "docs" / "decisions").is_dir():
        print(f"bot repo not found at {bot_root}")
        return 2
    head = git(bot_root, "rev-parse", "--short", "HEAD")
    ledger = load_ledger()
    print(f"bot {bot_root} @ {head}  ({'APPLY' if apply else 'dry run'})")

    # Plan every mirror first, so links can point at any mirrored document.
    mirrors: list[tuple[str, str, Path, bool]] = []  # kind, rel, dest file, also_raw
    for m in cfg.get("mirror", []):
        for rel in expand(bot_root, m["globs"]):
            dest = VAULT / m["dest"] / f"{mirror_slug(m['kind'], Path(rel))}.md"
            mirrors.append((m["kind"], rel, dest, bool(m.get("also_raw"))))
    targets = {rel: dest.stem for _, rel, dest, _ in mirrors}
    adr_slugs = {adr_number(Path(rel).name): dest.stem for kind, rel, dest, _ in mirrors
                 if kind == "adr" and adr_number(Path(rel).name)}

    counts = {"written": 0, "unchanged": 0, "refused": 0, "raw": 0}
    adr_rows = []
    for kind, rel, dest, also_raw in mirrors:
        data = (bot_root / rel).read_bytes()
        text = data.decode("utf-8")
        if kind == "adr":
            title, status, when = parse_adr_header(text)
            adr_rows.append((adr_number(Path(rel).name), dest.stem, title, status, when))
        if only and only != kind:
            continue
        hit = find_secret(text)
        if hit:
            print(f"  REFUSED (secret-like content: {hit}…)  {rel}")
            counts["refused"] += 1
            continue
        sha = hashlib.sha256(data).hexdigest()
        if ledger.get(rel, {}).get("sha256") == sha and dest.exists():
            counts["unchanged"] += 1
            continue
        prov = provenance(bot_root, rel, data)
        aliases = [f"ADR-{adr_number(Path(rel).name)}"] if kind == "adr" else []
        note = render_mirror(kind, rel, rewrite_links(text, rel, targets, adr_slugs), prov, aliases)
        print(f"  {'update' if dest.exists() else 'create'} {dest.relative_to(VAULT).as_posix()}")
        if apply:
            ingest.atomic_write(dest, note)
            ledger[rel] = {"sha256": sha, "dest": dest.relative_to(VAULT).as_posix(), "commit": prov["commit"],
                           "exported_at": prov["exported_at"]}
        counts["written"] += 1
        if also_raw:
            counts["raw"] += copy_to_raw(bot_root, rel, data, prov, apply)

    if not only or only == "raw":
        for r in cfg.get("raw", []):
            for rel in expand(bot_root, r["globs"]):
                data = (bot_root / rel).read_bytes()
                key = f"raw::{rel}"
                sha = hashlib.sha256(data).hexdigest()
                if ledger.get(key, {}).get("sha256") == sha:
                    counts["unchanged"] += 1
                    continue
                if rel.lower().endswith((".md", ".html", ".txt")):
                    hit = find_secret(data.decode("utf-8", errors="replace"))
                    if hit:
                        print(f"  REFUSED (secret-like content: {hit}…)  {rel}")
                        counts["refused"] += 1
                        continue
                prov = provenance(bot_root, rel, data)
                counts["raw"] += copy_to_raw(bot_root, rel, data, prov, apply)
                if apply:
                    ledger[key] = {"sha256": sha, "commit": prov["commit"], "exported_at": prov["exported_at"]}

    if not only or only == "adr":
        index = render_adr_index(adr_rows, head)
        old = ADR_INDEX.read_text(encoding="utf-8") if ADR_INDEX.exists() else ""
        if strip_volatile(old) != strip_volatile(index):
            print(f"  {'update' if old else 'create'} {ADR_INDEX.relative_to(VAULT).as_posix()}")
            if apply:
                ingest.atomic_write(ADR_INDEX, index)
            counts["written"] += 1

    if apply:
        save_ledger(ledger)
    print(f"done: {counts}")
    return 0


class _TextOnly(HTMLParser):
    """Visible text of an HTML page: drops scripts, styles and markup; keeps paragraph breaks."""

    BLOCK = {"p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "pre"}

    def __init__(self) -> None:
        super().__init__()
        self.out: list[str] = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip += 1
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)


def html_to_text(html: str) -> str:
    parser = _TextOnly()
    parser.feed(html)
    text = "".join(parser.out)
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n\s*\n+", "\n\n", text).strip() + "\n"


def copy_to_raw(bot_root: Path, rel: str, data: bytes, prov: dict, apply: bool) -> int:
    """Copy one document to raw/ for Gemini. Markdown and HTML (as extracted text) get a provenance header."""
    src = Path(rel)
    suffix = src.suffix.lower()
    name = "dlmm-" + ingest.slugify(src.stem) + (".md" if suffix in (".md", ".html", ".htm") else suffix)
    print(f"  raw  raw/{name}")
    if not apply:
        return 1
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    tmp = RAW_DIR / f".{name}.bridge-tmp"  # dotfile: the ingestion watcher ignores it until the rename
    header = (f"<!-- Source: dlmm-hedge-bot/development/{rel} at commit {prov['commit']}, "
              f"exported {prov['exported_at']} by bridges/dlmm_bridge.py -->\n\n")
    if suffix == ".md":
        tmp.write_text(header + data.decode("utf-8"), encoding="utf-8")
    elif suffix in (".html", ".htm"):
        tmp.write_text(header + html_to_text(data.decode("utf-8", errors="replace")), encoding="utf-8")
    else:
        shutil.copyfile(bot_root / rel, tmp)
    tmp.replace(RAW_DIR / name)
    return 1


def render_adr_index(rows: list[tuple], head: str) -> str:
    rows = sorted(r for r in rows if r[0])
    fm = {
        "domain": "cl-market-making",
        "tags": ["dlmm-hedge-bot", "adr-index"],
        "aliases": ["ADR index", "dlmm-hedge-bot decisions"],
        "created": date.today().isoformat(),
        "reviewed": True,
        "bridge_managed": True,
        "bot_commit": head,
    }
    lines = ["# dlmm-hedge-bot — architecture decision records", "",
             f"> [!info] Generated by `bridges/dlmm_bridge.py` from the bot repo at `{head}`. The bot repo is the "
             "source of truth; statuses here can lag it.", "",
             "| ADR | Title | Status | Date |", "|---|---|---|---|"]
    for num, slug, title, status, when in rows:
        lines.append(f"| [[{slug}|ADR-{num}]] | {title.replace('|', '/')} | {status.replace('|', '/')} | {when} |")
    return ingest.render_frontmatter(fm) + "\n".join(lines) + "\n"


def strip_volatile(text: str) -> str:
    """The ADR index without its date and commit, so a re-run with no ADR changes writes nothing."""
    return re.sub(r"(created|bot_commit): .*\n|at `[^`]+`", "", text)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mirror dlmm-hedge-bot documents into the vault (read-only on the bot)")
    parser.add_argument("--apply", action="store_true", help="write changes (default is a dry run)")
    parser.add_argument("--only", choices=["adr", "blueprint", "report", "finding", "raw"])
    args = parser.parse_args(argv)
    return run(args.apply, args.only)


if __name__ == "__main__":
    sys.exit(main())
