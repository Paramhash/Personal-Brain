import time
import threading
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

load_dotenv()
client = genai.Client()

VAULT_ROOT = Path(__file__).parent.resolve()
RAW_DIR = VAULT_ROOT / "raw"
PROCESSED_DIR = RAW_DIR / "assets" / "processed"
INGESTION_LOG = RAW_DIR / "assets" / "ingestion-log.md"
SPEC_FILE = VAULT_ROOT / "GEMINI.md"


def load_system_spec() -> str:
    if SPEC_FILE.exists():
        return SPEC_FILE.read_text(encoding="utf-8")
    return "You are an expert infrastructure agent organizing data into a markdown wiki."


def log_ingestion(file_name: str, output_paths: list[str], success: bool):
    INGESTION_LOG.parent.mkdir(parents=True, exist_ok=True)
    if not INGESTION_LOG.exists():
        INGESTION_LOG.write_text("# Ingestion Log\n\n", encoding="utf-8")

    timestamp = datetime.now().isoformat(timespec="seconds")
    status = "OK" if success else "FAIL"
    lines = [f"## [{status}] `{file_name}` — {timestamp}"]
    for p in output_paths:
        lines.append(f"- `{p}`")
    lines.append("")

    with INGESTION_LOG.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def process_file(file_path: Path):
    print(f"Ingesting: {file_path.name}")

    try:
        raw_content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        log_ingestion(file_path.name, [], success=False)
        return

    prompt = f"""
Analyze and ingest the following raw payload file: '{file_path.name}'.
Follow all directory formatting, architectural linking, and metadata rules defined in your system spec.

Return ONLY the completed markdown files. If you generate multiple notes, separate them with:
=== FILE: path/to/filename.md ===

RAW PAYLOAD CONTENT:
{raw_content}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=load_system_spec(),
                temperature=0.2,
            ),
        )

        output_paths = parse_and_write_outputs(response.text)
        archive_raw_file(file_path)
        log_ingestion(file_path.name, output_paths, success=True)
        print(f"Done: {file_path.name} -> {len(output_paths)} file(s)")

    except Exception as e:
        print(f"Gemini error processing {file_path.name}: {e}")
        log_ingestion(file_path.name, [], success=False)


def parse_and_write_outputs(response_text: str) -> list[str]:
    current_path: Path | None = None
    accumulator: list[str] = []
    written: list[str] = []

    for line in response_text.split("\n"):
        if line.startswith("=== FILE:"):
            if current_path and accumulator:
                write_to_vault(current_path, "\n".join(accumulator))
                written.append(str(current_path.relative_to(VAULT_ROOT)))
                accumulator = []
            rel = line.replace("=== FILE:", "").replace("===", "").strip()
            p = Path(rel)
            if p.is_absolute() or rel.startswith(("/", "\\")):
                import os
                _, no_drive = os.path.splitdrive(rel)
                rel = no_drive.lstrip("/\\")
            current_path = VAULT_ROOT / rel
        elif current_path is not None:
            accumulator.append(line)

    if current_path and accumulator:
        write_to_vault(current_path, "\n".join(accumulator))
        written.append(str(current_path.relative_to(VAULT_ROOT)))

    return written


def write_to_vault(target_path: Path, content: str):
    clean = content.strip()

    # Strip code fences Gemini sometimes wraps around the whole block
    if clean.startswith("```markdown"):
        clean = clean[len("```markdown"):]
    elif clean.startswith("```"):
        clean = clean[3:]
    if clean.endswith("```"):
        clean = clean[:-3]
    clean = clean.strip()

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(clean, encoding="utf-8")
    print(f"  Written: {target_path.relative_to(VAULT_ROOT)}")


def archive_raw_file(file_path: Path):
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    dest = PROCESSED_DIR / file_path.name
    if dest.exists():
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        dest = PROCESSED_DIR / f"{file_path.stem}-{ts}{file_path.suffix}"
    file_path.rename(dest)
    print(f"  Archived: {dest.relative_to(VAULT_ROOT)}")


class RawFolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix == ".tmp" or path.name.startswith("."):
            return
        # Small buffer to ensure the file write has fully closed before reading
        time.sleep(1)
        threading.Thread(target=process_file, args=(path,), daemon=True).start()


def scan_existing():
    """Process any files already sitting in raw/ at startup."""
    pending = [
        f for f in RAW_DIR.iterdir()
        if f.is_file() and f.suffix != ".tmp" and not f.name.startswith(".")
    ]
    if not pending:
        return
    print(f"Found {len(pending)} unprocessed file(s) in raw/ — ingesting now...")
    for f in pending:
        threading.Thread(target=process_file, args=(f,), daemon=True).start()


if __name__ == "__main__":
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Level 0 Ingestion Engine online. Watching: {RAW_DIR}")

    scan_existing()

    handler = RawFolderHandler()
    observer = Observer()
    observer.schedule(handler, path=str(RAW_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
