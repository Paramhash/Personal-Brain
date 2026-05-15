# Personal-Brain

A two-level AI knowledge vault. Drop raw files in; get a structured, cross-linked wiki out. Browse it in Obsidian.

## Architecture

```
raw/                        ← drop files here
  └─ paper.md
        │
        ▼  Level 0 — Gemini (ingest.py)
wiki/
  ├─ concepts/              ← abstract ideas, frameworks
  ├─ entities/              ← people, orgs, tools
  ├─ sources/               ← papers, articles, books
  └─ research/              ← Level 1 analysis output
        │
        ▼  Level 1 — Claude in IDE (LEVEL1.md as context)
wiki/research/
  ├─ synthesis-YYYY-MM-DD.md
  ├─ gap-analysis-YYYY-MM-DD.md
  └─ research-agenda-YYYY-MM-DD.md
```

**Level 0 — Gemini ingestion (`ingest.py`):** Watches `raw/` for new files. Each file is sent to Gemini with the system spec in `GEMINI.md`. Gemini produces structured markdown notes split across `wiki/concepts/`, `wiki/entities/`, and `wiki/sources/`. Processed files are archived to `raw/assets/processed/`.

**Level 1 — Claude analysis (IDE):** Open `LEVEL1.md` in your IDE and ask Claude to read the wiki and run an analysis mode. No script needed — the AI reads the vault directly and writes output to `wiki/research/`.

**Obsidian UI:** Open the vault root in Obsidian to browse the wiki. `index.md` is the home dashboard, powered by the Dataview plugin.

## Setup

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```
GEMINI_API_KEY=your_gemini_key
```

## Usage

**Start the ingestion watcher:**

```bash
python ingest.py
```

Drop any file into `raw/`. Gemini structures it into the wiki automatically.

**Run Level 1 analysis:**

In your IDE, load `LEVEL1.md` as context and ask Claude to run one or more analysis modes over the wiki:

- **synthesis** — maps the conceptual landscape across all notes
- **gaps** — identifies what is missing or underdocumented
- **research-agenda** — proposes the highest-value questions to pursue next

Output is written to `wiki/research/`.

## Project structure

```
personal-brain/
├── ingest.py               # Level 0 ingestion engine (Gemini)
├── GEMINI.md               # Gemini system spec
├── LEVEL1.md               # Claude system spec for analysis
├── index.md                # Obsidian home dashboard (Dataview)
├── requirements.txt
├── .env                    # API keys (not committed)
├── .obsidian/              # Obsidian config + Dataview plugin
├── raw/                    # Drop files here
│   └── assets/
│       ├── processed/      # Archived after ingestion
│       └── ingestion-log.md
├── wiki/
│   ├── concepts/
│   ├── entities/
│   ├── sources/
│   └── research/
└── docs/                   # Setup notes
```
