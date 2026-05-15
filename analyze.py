#!/usr/bin/env python3
"""Level 1 Analysis Engine — Claude"""

import argparse
import time
import threading
from datetime import date
from pathlib import Path

import anthropic
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

client = anthropic.Anthropic()

VAULT_ROOT = Path(__file__).parent.resolve()
WIKI_DIR = VAULT_ROOT / "wiki"
RESEARCH_DIR = WIKI_DIR / "research"
SPEC_FILE = VAULT_ROOT / "LEVEL1.md"
MODEL = "claude-opus-4-7"

TODAY = date.today().isoformat()

ANALYSIS_PROMPTS: dict[str, str] = {
    "synthesis": (
        f"Run the synthesis analysis mode defined in your system spec. "
        f"Target output file: wiki/research/synthesis-{TODAY}.md"
    ),
    "gaps": (
        f"Run the gaps analysis mode defined in your system spec. "
        f"Target output file: wiki/research/gap-analysis-{TODAY}.md"
    ),
    "research-agenda": (
        f"Run the research-agenda analysis mode defined in your system spec. "
        f"Target output file: wiki/research/research-agenda-{TODAY}.md"
    ),
}

OUTPUT_FILENAMES: dict[str, str] = {
    "synthesis": f"synthesis-{TODAY}.md",
    "gaps": f"gap-analysis-{TODAY}.md",
    "research-agenda": f"research-agenda-{TODAY}.md",
}


def load_spec() -> str:
    if SPEC_FILE.exists():
        return SPEC_FILE.read_text(encoding="utf-8")
    return "You are a knowledge synthesis engine. Analyze the provided wiki and produce structured research notes."


def load_wiki_context() -> str:
    parts: list[str] = []
    for md_file in sorted(WIKI_DIR.rglob("*.md")):
        # Skip today's output files to avoid self-reference loops
        if md_file.parent == RESEARCH_DIR and md_file.name in OUTPUT_FILENAMES.values():
            continue
        rel = md_file.relative_to(VAULT_ROOT)
        content = md_file.read_text(encoding="utf-8")
        parts.append(f"=== {rel} ===\n{content}")
    return "\n\n".join(parts)


def run_analysis(mode: str) -> Path:
    print(f"[{mode}] Loading wiki context...")
    spec = load_spec()
    wiki_context = load_wiki_context()

    print(f"[{mode}] Calling Claude ({MODEL})...")
    response = client.messages.create(
        model=MODEL,
        max_tokens=8096,
        system=[
            # Cache the system spec — it rarely changes
            {"type": "text", "text": spec, "cache_control": {"type": "ephemeral"}}
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    # Cache the wiki context — expensive to re-send on each analysis mode
                    {
                        "type": "text",
                        "text": f"WIKI CONTEXT:\n\n{wiki_context}",
                        "cache_control": {"type": "ephemeral"},
                    },
                    {"type": "text", "text": ANALYSIS_PROMPTS[mode]},
                ],
            }
        ],
    )

    output = response.content[0].text.strip()

    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESEARCH_DIR / OUTPUT_FILENAMES[mode]
    out_path.write_text(output, encoding="utf-8")

    usage = response.usage
    cache_read = getattr(usage, "cache_read_input_tokens", 0)
    cache_written = getattr(usage, "cache_creation_input_tokens", 0)
    print(
        f"[{mode}] Written: {out_path.relative_to(VAULT_ROOT)} | "
        f"tokens in={usage.input_tokens} cache_read={cache_read} "
        f"cache_written={cache_written} out={usage.output_tokens}"
    )

    return out_path


def run_all():
    for mode in ANALYSIS_PROMPTS:
        run_analysis(mode)


class WikiWatcher(FileSystemEventHandler):
    """Debounced watcher — waits for a quiet period before triggering a full analysis run."""

    def __init__(self, debounce_seconds: int = 30):
        self._debounce = debounce_seconds
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    def _schedule(self):
        with self._lock:
            if self._timer:
                self._timer.cancel()
            self._timer = threading.Timer(self._debounce, run_all)
            self._timer.daemon = True
            self._timer.start()
            print(f"Wiki change detected — analysis scheduled in {self._debounce}s")

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            self._schedule()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".md"):
            self._schedule()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Level 1: Claude Analysis Engine")
    parser.add_argument(
        "--mode",
        choices=[*ANALYSIS_PROMPTS.keys(), "all"],
        default="all",
        help="Analysis mode to run (default: all)",
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch wiki/ for changes and re-run analysis automatically (debounced 30s)",
    )
    parser.add_argument(
        "--debounce",
        type=int,
        default=30,
        help="Seconds of quiet after last wiki change before triggering analysis (default: 30)",
    )
    args = parser.parse_args()

    if args.watch:
        print(f"Watching {WIKI_DIR} for changes (debounce={args.debounce}s)...")
        watcher = WikiWatcher(debounce_seconds=args.debounce)
        observer = Observer()
        observer.schedule(watcher, path=str(WIKI_DIR), recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        if args.mode == "all":
            run_all()
        else:
            run_analysis(args.mode)
