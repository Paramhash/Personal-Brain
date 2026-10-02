"""Level 0 ingestion engine: raw/ -> Gemini -> wiki/ (see GEMINI.md).

Usage:
    python ingest.py                 # watch raw/ (needs INGEST_HOST in .env to match this machine)
    python ingest.py --once          # process everything in raw/ now, then exit
    python ingest.py --file PATH     # process one file
    python ingest.py --once --dry-run  # call Gemini and print the plan; write nothing, archive nothing

Safety rules (enforced here, not only asked of the model):
- writes go only to wiki/{concepts,entities,sources,research}; wiki/dlmm, wiki/curriculum, wiki/decisions,
  wiki/observations and wiki/playbooks belong to the bridge and to Level 1, and are never written by ingestion;
- an existing note is never overwritten: new content is merged as a dated "Update from" section, and a note
  marked `bridge_managed: true` is never touched;
- filenames are slugged (lowercase-hyphen) and checked against existing slugs and aliases, so a concept that
  already exists is merged into rather than duplicated;
- `domain` is checked against DOMAINS;
- a raw file whose content was already ingested is skipped (raw/assets/ingested-hashes.json).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import queue
import re
import socket
import sys
import threading
import time
import unicodedata
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

VAULT_ROOT = Path(__file__).parent.resolve()
WIKI_DIR = VAULT_ROOT / "wiki"
RAW_DIR = VAULT_ROOT / "raw"
PROCESSED_DIR = RAW_DIR / "assets" / "processed"
INGESTION_LOG = RAW_DIR / "assets" / "ingestion-log.md"
SOURCE_LEDGER = RAW_DIR / "assets" / "ingested-hashes.json"
SPEC_FILE = VAULT_ROOT / "GEMINI.md"

MODEL = "gemini-2.5-flash"
ALLOWED_SUBDIRS = ("concepts", "entities", "sources", "research")
PROTECTED_SUBDIRS = ("dlmm", "curriculum", "decisions", "observations", "playbooks")
DOMAINS = ("derivatives", "fine-art", "meta", "cl-market-making")
UNCLASSIFIED = "unclassified"
MAX_TEXT_BYTES = 200_000
UPDATE_HEADING = "## Update from"

_client = None


def get_client():
    """The Gemini client, created on first use so the pure functions import without an API key."""
    global _client
    if _client is None:
        from google import genai  # imported lazily for the same reason

        load_dotenv()
        _client = genai.Client()
    return _client


# --------------------------------------------------------------------------------------------- pure helpers


@dataclass
class NoteBlock:
    rel_path: str
    content: str


@dataclass
class WriteResult:
    rel_path: str
    action: str  # created | merged | skipped:<why> | rejected:<why>
    detail: str = ""


def slugify(name: str) -> str:
    """A lowercase-hyphen slug of a file name or title, without extension: 'Stock Market Regimes.md' -> 'stock-market-regimes'."""
    stem = name[:-3] if name.lower().endswith(".md") else name
    # Accents fold away (é -> e); any other non-ASCII character (an en dash, say) separates words.
    folded = "".join(
        c if ord(c) < 128 else ("" if unicodedata.combining(c) else "-")
        for c in unicodedata.normalize("NFKD", stem)
    )
    slug = re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")
    return slug


def strip_fences(text: str) -> str:
    """Remove a code fence the model sometimes wraps around a whole note."""
    clean = text.strip()
    if clean.startswith("```markdown"):
        clean = clean[len("```markdown"):]
    elif clean.startswith("```md"):
        clean = clean[len("```md"):]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    return clean.strip()


def parse_response(text: str) -> list[NoteBlock]:
    """Split a model reply on '=== FILE: path ===' lines. Text before the first marker is ignored."""
    blocks: list[NoteBlock] = []
    current: str | None = None
    lines: list[str] = []
    for line in text.splitlines():
        if line.strip().startswith("=== FILE:"):
            if current is not None and "".join(lines).strip():
                blocks.append(NoteBlock(current, "\n".join(lines)))
            current = line.strip()[len("=== FILE:"):].replace("===", "").strip()
            lines = []
        elif current is not None:
            lines.append(line)
    if current is not None and "".join(lines).strip():
        blocks.append(NoteBlock(current, "\n".join(lines)))
    return blocks


def confine_path(rel: str) -> tuple[Path | None, str]:
    """Map a model-proposed path onto wiki/<allowed>/<slug>.md, or reject it with a reason.

    Accepts 'wiki/concepts/x.md', '/wiki/concepts/x.md' or 'concepts/x.md'. Every component is slugged, so the
    result is a canonical name. Absolute paths, drive letters and '..' are rejected outright.
    """
    raw = rel.strip().replace("\\", "/")
    if re.match(r"^[A-Za-z]:", raw) or raw.startswith("//"):
        return None, "absolute"
    parts = [p for p in raw.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        return None, "traversal"
    if parts and parts[0] == "wiki":
        parts = parts[1:]
    if len(parts) < 2:
        return None, "no-subfolder"
    sub = parts[0].lower()
    if sub in PROTECTED_SUBDIRS:
        return None, f"protected:{sub}"
    if sub not in ALLOWED_SUBDIRS:
        return None, f"not-allowed:{sub}"
    tail = [slugify(p) for p in parts[1:]]
    if any(t == "" for t in tail):
        return None, "empty-name"
    target = (WIKI_DIR / sub / Path(*tail[:-1]) / f"{tail[-1]}.md").resolve()
    root = (WIKI_DIR / sub).resolve()
    if root not in target.parents:
        return None, "escaped"
    return target, ""


_FM_RE = re.compile(r"\A(?:﻿)?(?:yaml\s*\n)?---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", re.S)


def split_frontmatter(text: str) -> tuple[dict, str]:
    """(frontmatter, body). Tolerates a stray 'yaml' line before the opening '---'. Unparseable YAML -> ({}, text)."""
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}, text
    if not isinstance(fm, dict):
        return {}, text
    return fm, text[m.end():]


def render_frontmatter(fm: dict) -> str:
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n"


def _as_list(v) -> list:
    if v is None:
        return []
    if isinstance(v, list):
        return [x for x in v if x is not None and str(x).strip() != ""]
    return [v] if str(v).strip() else []


def _union(a: list, b: list) -> list:
    out = list(a)
    for x in b:
        if x not in out:
            out.append(x)
    return out


def _valid_date(v) -> bool:
    if isinstance(v, (date, datetime)):
        return True
    try:
        datetime.strptime(str(v), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_frontmatter(fm: dict, source_name: str, today: str, fallback_domain: str | None = None) -> tuple[dict, list[str]]:
    """Enforce the schema in GEMINI.md. Returns the repaired frontmatter and a list of warnings."""
    warnings: list[str] = []
    out = dict(fm)
    domain = out.get("domain")
    if domain not in DOMAINS:
        repaired = fallback_domain if fallback_domain in DOMAINS else UNCLASSIFIED
        warnings.append(f"domain {domain!r} -> {repaired}")
        out["domain"] = repaired
    out["tags"] = _as_list(out.get("tags"))
    out["aliases"] = _as_list(out.get("aliases"))
    if not _valid_date(out.get("created")):
        if "created" in out:
            warnings.append(f"created {out.get('created')!r} -> {today}")
        out["created"] = today
    out["reviewed"] = False
    out["source_origin"] = source_name
    ordered = {k: out.pop(k) for k in ("domain", "tags", "aliases", "created", "reviewed", "source_origin") if k in out}
    ordered.update(out)
    return ordered, warnings


def body_hash(body: str) -> str:
    normalized = re.sub(r"\s+", " ", body).strip()
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:16]


def merge_note(existing_text: str, new_text: str, source_name: str, today: str) -> tuple[str, bool]:
    """Merge a newly generated note into an existing one without a second LLM call.

    Keeps the existing frontmatter and `created`, unions tags and aliases, marks the note unreviewed, and appends the
    new body as '## Update from <source> (<date>)'. A body whose hash is already recorded in `ingest_hashes` (or that
    equals the existing body) changes nothing, so re-ingesting identical output is a no-op.
    """
    old_fm, old_body = split_frontmatter(existing_text)
    new_fm, new_body = split_frontmatter(new_text)
    new_body = new_body.strip()
    h = body_hash(new_body)
    hashes = _as_list(old_fm.get("ingest_hashes"))
    if not new_body or h in hashes or body_hash(old_body) == h:
        return existing_text, False

    fm = dict(old_fm)
    fm["tags"] = _union(_as_list(old_fm.get("tags")), _as_list(new_fm.get("tags")))
    fm["aliases"] = _union(_as_list(old_fm.get("aliases")), _as_list(new_fm.get("aliases")))
    if old_fm.get("domain") not in DOMAINS and new_fm.get("domain") in DOMAINS:
        fm["domain"] = new_fm["domain"]
    fm["reviewed"] = False
    fm["updated"] = today
    fm["sources"] = _union(_as_list(old_fm.get("sources")) or _as_list(old_fm.get("source_origin")), [source_name])
    fm["ingest_hashes"] = hashes + [h]
    merged_body = old_body.rstrip() + f"\n\n{UPDATE_HEADING} {source_name} ({today})\n\n{new_body}\n"
    return render_frontmatter(fm) + merged_body.lstrip("\n"), True


def build_slug_index(wiki_dir: Path) -> dict[str, list[Path]]:
    """slug -> notes, keyed on each note's slugged filename and slugged aliases."""
    index: dict[str, list[Path]] = {}
    for path in sorted(wiki_dir.rglob("*.md")):
        keys = {slugify(path.name)}
        try:
            fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            fm = {}
        keys.update(slugify(str(a)) for a in _as_list(fm.get("aliases")))
        for k in keys:
            if k:
                index.setdefault(k, []).append(path)
    return index


def resolve_existing(index: dict[str, list[Path]], target: Path, aliases: list) -> Path | None:
    """The note a block should merge into: the exact target if it exists, else a slug or alias hit (same folder first)."""
    if target.exists():
        return target
    keys = [slugify(target.name)] + [slugify(str(a)) for a in aliases]
    for k in keys:
        hits = index.get(k, [])
        if hits:
            same = [h for h in hits if h.parent == target.parent]
            return (same or hits)[0]
    return None


def existing_notes_listing(wiki_dir: Path, limit: int = 2000) -> str:
    """'folder/slug | aliases | domain' lines for the prompt, so the model links to and extends existing notes."""
    rows = []
    for path in sorted(wiki_dir.rglob("*.md"))[:limit]:
        try:
            fm, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError):
            fm = {}
        rel = path.relative_to(wiki_dir).as_posix()[:-3]
        aliases = ", ".join(str(a) for a in _as_list(fm.get("aliases")))
        rows.append(f"{rel} | {aliases} | {fm.get('domain', '')}")
    return "\n".join(rows)


_WIKILINK = re.compile(r"\[\[([^\]|#]+)((?:#[^\]|]*)?)((?:\|[^\]]*)?)\]\]")


def normalize_links(body: str, index: dict[str, list[Path]]) -> str:
    """Rewrite [[folder/x.md|label]] and [[../concepts/x|label]] to [[x|label]] when note x exists in the vault.

    The model is asked for bare slugs but sometimes adds folders or '.md'; a folder that does not match the vault's
    layout can leave the link unresolved. Links to notes that do not exist yet are left as written.
    """

    def sub(m: re.Match) -> str:
        target, anchor, label = m.group(1).strip(), m.group(2), m.group(3)
        name = target.replace("\\", "/").split("/")[-1]
        name = name[:-3] if name.lower().endswith(".md") else name
        hits = index.get(slugify(name))
        if not hits or ("/" not in target and not target.lower().endswith(".md") and target == hits[0].stem):
            return m.group(0)
        return f"[[{hits[0].stem}{anchor}{label}]]"

    return _WIKILINK.sub(sub, body)


def atomic_write(path: Path, text: str) -> None:
    """Write via a temporary file in the same folder, then os.replace, so a sync tool never sees half a note."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / f".{path.name}.ingest-tmp"
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def commit_blocks(blocks: list[NoteBlock], source_name: str, dry_run: bool, today: str,
                  wiki_dir: Path | None = None) -> list[WriteResult]:
    """Apply parsed blocks to the vault: create new notes, merge into existing ones, reject anything unsafe."""
    wiki_dir = wiki_dir or WIKI_DIR
    index = build_slug_index(wiki_dir)
    results: list[WriteResult] = []
    for block in blocks:
        target, reason = confine_path(block.rel_path)
        if target is None:
            results.append(WriteResult(block.rel_path, f"rejected:{reason}"))
            continue
        if wiki_dir != WIKI_DIR:  # tests run against a temporary vault
            target = wiki_dir / target.relative_to(WIKI_DIR)
        content = strip_fences(block.content)
        new_fm, new_body = split_frontmatter(content)
        content = (render_frontmatter(new_fm) if new_fm else "") + normalize_links(new_body, index)
        existing = resolve_existing(index, target, _as_list(new_fm.get("aliases")))
        rel = lambda p: p.relative_to(wiki_dir.parent).as_posix()  # noqa: E731
        if existing is not None:
            old_text = existing.read_text(encoding="utf-8")
            old_fm, _ = split_frontmatter(old_text)
            if old_fm.get("bridge_managed") is True:
                results.append(WriteResult(rel(existing), "rejected:bridge-managed"))
                continue
            merged, changed = merge_note(old_text, content, source_name, today)
            if not changed:
                results.append(WriteResult(rel(existing), "skipped:unchanged"))
                continue
            if not dry_run:
                atomic_write(existing, merged)
            detail = "" if existing == target else f"proposed {rel(target)}"
            results.append(WriteResult(rel(existing), "merged", detail))
            continue
        fm, body = split_frontmatter(content)
        fm, warnings = validate_frontmatter(fm, source_name, today)
        if str(fm.get("created")) != today:  # `created` is the ingestion date; the model sometimes invents one
            warnings.append(f"created {fm.get('created')} -> {today}")
            fm["created"] = today
        fm["ingest_hashes"] = [body_hash(body.strip())]
        text = render_frontmatter(fm) + body.lstrip("\n")
        if not dry_run:
            atomic_write(target, text)
            index.setdefault(slugify(target.name), []).append(target)
            for a in fm.get("aliases", []):
                index.setdefault(slugify(str(a)), []).append(target)
        results.append(WriteResult(rel(target), "created", "; ".join(warnings)))
    return results


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def is_ignorable(path: Path) -> bool:
    name = path.name
    return (
        name.startswith(".")
        or name.startswith("~syncthing~")
        or ".sync-conflict-" in name
        or path.suffix.lower() in (".tmp", ".part", ".crdownload")
    )


# --------------------------------------------------------------------------------------------- side effects


def load_system_spec() -> str:
    if SPEC_FILE.exists():
        return SPEC_FILE.read_text(encoding="utf-8")
    return "You are an expert infrastructure agent organizing data into a markdown wiki."


def load_ledger() -> dict:
    if SOURCE_LEDGER.exists():
        try:
            return json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_ledger(ledger: dict) -> None:
    SOURCE_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    atomic_write(SOURCE_LEDGER, json.dumps(ledger, indent=1, sort_keys=True))


def log_ingestion(file_name: str, results: list[WriteResult], success: bool, usage: str = "", note: str = "") -> None:
    INGESTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not INGESTION_LOG.exists():
        INGESTION_LOG.write_text("# Ingestion Log\n\n", encoding="utf-8")
    status = "OK" if success else "FAIL"
    lines = [f"## [{status}] `{file_name}` — {datetime.now().isoformat(timespec='seconds')}"]
    if note:
        lines.append(f"- note: {note}")
    if usage:
        lines.append(f"- tokens: {usage}")
    for r in results:
        lines.append(f"- {r.action} `{r.rel_path}`" + (f" ({r.detail})" if r.detail else ""))
    lines.append("")
    with INGESTION_LOG.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def build_prompt(file_name: str) -> str:
    return f"""
Analyze and ingest the following raw payload file: '{file_name}'.
Follow all directory, naming, linking and metadata rules in your system spec.

EXISTING NOTES (folder/slug | aliases | domain). If a concept below already exists, write to THAT path (it will be
merged), and link to existing notes with [[slug|label]] instead of creating near-duplicates:
{existing_notes_listing(WIKI_DIR)}

Return ONLY the completed markdown files, each starting with a line of the form:
=== FILE: wiki/<concepts|entities|sources|research>/<slug>.md ===
"""


def archive_raw_file(file_path: Path) -> Path:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    dest = PROCESSED_DIR / file_path.name
    if dest.exists():
        dest = PROCESSED_DIR / f"{file_path.stem}-{datetime.now().strftime('%Y%m%d-%H%M%S')}{file_path.suffix}"
    file_path.rename(dest)
    return dest


def process_file(file_path: Path, dry_run: bool = False, archive: bool = True) -> list[WriteResult]:
    """Ingest one raw file. Returns the planned (dry run) or applied write results."""
    name = file_path.name
    print(f"Ingesting: {name}{' (dry run)' if dry_run else ''}")
    digest = file_sha256(file_path)
    ledger = load_ledger()
    if digest in ledger:
        print(f"  Skipped: identical content already ingested as {ledger[digest]['name']} on {ledger[digest]['at']}")
        if not dry_run:
            log_ingestion(name, [], success=True, note=f"skipped: duplicate of {ledger[digest]['name']}")
            if archive:
                archive_raw_file(file_path)
        return []

    is_pdf = file_path.suffix.lower() == ".pdf"
    if not is_pdf and file_path.stat().st_size > MAX_TEXT_BYTES:
        msg = f"refused: {file_path.stat().st_size} bytes > {MAX_TEXT_BYTES}; split the file"
        print(f"  {msg}")
        log_ingestion(name, [], success=False, note=msg)
        return []

    try:
        client = get_client()
        from google.genai import types

        prompt = build_prompt(name)
        if is_pdf:
            contents = [client.files.upload(file=file_path), prompt]
        else:
            contents = prompt + f"\n\nRAW PAYLOAD CONTENT:\n{file_path.read_text(encoding='utf-8')}"
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(system_instruction=load_system_spec(), temperature=0.2),
        )
    except Exception as e:  # noqa: BLE001 - one bad file must not stop the watcher
        print(f"  Error: {e}")
        log_ingestion(name, [], success=False, note=f"error: {e}")
        return []

    usage = ""
    meta = getattr(response, "usage_metadata", None)
    if meta is not None:
        usage = f"prompt {getattr(meta, 'prompt_token_count', '?')}, output {getattr(meta, 'candidates_token_count', '?')}"

    today = date.today().isoformat()
    results = commit_blocks(parse_response(response.text or ""), name, dry_run, today)
    for r in results:
        print(f"  {r.action:<28} {r.rel_path}" + (f"  ({r.detail})" if r.detail else ""))
    if dry_run:
        print(f"  Dry run: nothing written. {usage}")
        return results
    if archive:
        archive_raw_file(file_path)
    ledger[digest] = {"name": name, "at": datetime.now().isoformat(timespec="seconds")}
    save_ledger(ledger)
    log_ingestion(name, results, success=True, usage=usage)
    print(f"Done: {name} -> {sum(r.action in ('created', 'merged') for r in results)} note(s) written")
    return results


def wait_until_stable(path: Path, checks: int = 3, interval: float = 1.0, timeout: float = 120.0) -> bool:
    """True once the file size stops changing for `checks` consecutive intervals."""
    last, same, start = -1, 0, time.time()
    while time.time() - start < timeout:
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False
        same = same + 1 if size == last else 0
        if same >= checks:
            return True
        last = size
        time.sleep(interval)
    return False


def pending_raw_files() -> list[Path]:
    return sorted(f for f in RAW_DIR.iterdir() if f.is_file() and not is_ignorable(f))


def check_host(force: bool) -> bool:
    """Ingestion that writes runs on one machine only, so Syncthing peers never ingest the same file twice."""
    load_dotenv()
    want = os.environ.get("INGEST_HOST", "").strip()
    have = socket.gethostname()
    if force or (want and want.lower() == have.lower()):
        return True
    if not want:
        print(f"Refusing to write: set INGEST_HOST={have} in .env on the one machine that should ingest.")
    else:
        print(f"Refusing to write: INGEST_HOST is {want!r}, this machine is {have!r}.")
    return False


def watch(dry_run: bool, archive: bool) -> None:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer

    work: queue.Queue[Path] = queue.Queue()

    def worker():
        while True:
            path = work.get()
            try:
                if path.exists() and wait_until_stable(path):
                    process_file(path, dry_run=dry_run, archive=archive)
            finally:
                work.task_done()

    class RawFolderHandler(FileSystemEventHandler):
        def on_created(self, event):
            path = Path(event.src_path)
            if not event.is_directory and not is_ignorable(path):
                work.put(path)

    threading.Thread(target=worker, daemon=True).start()
    for f in pending_raw_files():
        work.put(f)
    observer = Observer()
    observer.schedule(RawFolderHandler(), path=str(RAW_DIR), recursive=False)
    observer.start()
    print(f"Level 0 ingestion online. Watching: {RAW_DIR}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Level 0 ingestion: raw/ -> Gemini -> wiki/")
    parser.add_argument("--once", action="store_true", help="process everything in raw/ and exit")
    parser.add_argument("--file", type=Path, help="process one file")
    parser.add_argument("--dry-run", action="store_true", help="call Gemini and print the plan; write nothing")
    parser.add_argument("--no-archive", action="store_true", help="leave processed files in place")
    parser.add_argument("--force-host", action="store_true", help="skip the INGEST_HOST check")
    args = parser.parse_args(argv)
    archive = not args.no_archive

    if not args.dry_run and not check_host(args.force_host):
        return 2
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if args.file:
        process_file(args.file.resolve(), dry_run=args.dry_run, archive=archive and not args.dry_run)
        return 0
    if args.once:
        for f in pending_raw_files():
            process_file(f, dry_run=args.dry_run, archive=archive and not args.dry_run)
        return 0
    watch(dry_run=args.dry_run, archive=archive and not args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
