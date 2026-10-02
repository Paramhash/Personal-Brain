"""Offline tests for ingest.py's pure functions and its write rules. No network, no API key."""

from pathlib import Path

import pytest

import ingest

TODAY = "2026-10-02"


def note(fm: str, body: str) -> str:
    return f"---\n{fm.strip()}\n---\n{body}"


@pytest.fixture
def vault(tmp_path: Path) -> Path:
    wiki = tmp_path / "wiki"
    for sub in ("concepts", "entities", "sources", "research", "dlmm/adr"):
        (wiki / sub).mkdir(parents=True)
    (wiki / "concepts" / "gamma-exposure-gex.md").write_text(
        note("domain: derivatives\ntags: [gex]\naliases: [GEX, gamma exposure]\ncreated: 2026-05-01\nreviewed: true\nsource_origin: a.md",
             "# Gamma exposure\n\nOriginal body.\n"),
        encoding="utf-8",
    )
    (wiki / "dlmm" / "adr" / "adr-052-ev-gate.md").write_text(
        note("domain: cl-market-making\nbridge_managed: true\nreviewed: true", "# ADR-052\n"), encoding="utf-8"
    )
    return wiki


# ---------------------------------------------------------------- slugify, fences, parsing


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("Stock Market Regimes.md", "stock-market-regimes"),
        ("gamma_exposure_gex", "gamma-exposure-gex"),
        ("  LVR (Loss-Versus-Rebalancing)  ", "lvr-loss-versus-rebalancing"),
        ("Guéant–Lehalle", "gueant-lehalle"),
        ("a---b__c", "a-b-c"),
    ],
)
def test_slugify(raw, expected):
    assert ingest.slugify(raw) == expected


def test_strip_fences():
    assert ingest.strip_fences("```markdown\n# A\n```") == "# A"
    assert ingest.strip_fences("```\n# A\n```") == "# A"
    assert ingest.strip_fences("# A") == "# A"


def test_parse_response_multiple_blocks_and_preamble():
    text = "Here you go:\n=== FILE: wiki/concepts/a.md ===\n# A\n\n=== FILE: wiki/sources/b.md ===\n# B\n"
    blocks = ingest.parse_response(text)
    assert [b.rel_path for b in blocks] == ["wiki/concepts/a.md", "wiki/sources/b.md"]
    assert blocks[0].content.strip() == "# A"


def test_parse_response_drops_empty_blocks():
    assert ingest.parse_response("=== FILE: wiki/concepts/a.md ===\n\n") == []


# ---------------------------------------------------------------- confinement


@pytest.mark.parametrize(
    "rel,reason",
    [
        ("../../evil.md", "traversal"),
        ("wiki/concepts/../../x.md", "traversal"),
        ("C:\\Windows\\x.md", "absolute"),
        ("wiki/dlmm/adr/x.md", "protected:dlmm"),
        ("wiki/curriculum/m01.md", "protected:curriculum"),
        ("raw/x.md", "not-allowed:raw"),
        ("wiki/x.md", "no-subfolder"),
    ],
)
def test_confine_path_rejects(rel, reason):
    target, why = ingest.confine_path(rel)
    assert target is None and why == reason


@pytest.mark.parametrize(
    "rel,expected",
    [
        ("wiki/concepts/Loss Versus Rebalancing.md", "concepts/loss-versus-rebalancing.md"),
        ("/wiki/entities/Meteora.md", "entities/meteora.md"),
        ("sources/Milionis_2022.md", "sources/milionis-2022.md"),
    ],
)
def test_confine_path_accepts_and_slugs(rel, expected):
    target, why = ingest.confine_path(rel)
    assert why == "" and target.relative_to(ingest.WIKI_DIR).as_posix() == expected


# ---------------------------------------------------------------- frontmatter


def test_frontmatter_round_trip_and_stray_yaml_line():
    text = "yaml\n---\ndomain: meta\ntags: [a]\n---\n# Body\n"
    fm, body = ingest.split_frontmatter(text)
    assert fm == {"domain": "meta", "tags": ["a"]} and body == "# Body\n"
    again, body2 = ingest.split_frontmatter(ingest.render_frontmatter(fm) + body)
    assert again == fm and body2 == body


def test_validate_frontmatter_repairs():
    fm, warnings = ingest.validate_frontmatter({"domain": "defi", "created": "soon", "reviewed": True}, "src.md", TODAY)
    assert fm["domain"] == "unclassified" and fm["created"] == TODAY
    assert fm["reviewed"] is False and fm["source_origin"] == "src.md"
    assert fm["tags"] == [] and fm["aliases"] == [] and len(warnings) == 2
    fm2, _ = ingest.validate_frontmatter({"domain": "nope"}, "s.md", TODAY, fallback_domain="derivatives")
    assert fm2["domain"] == "derivatives"


# ---------------------------------------------------------------- merge


def test_merge_appends_once_and_is_idempotent():
    old = note("domain: derivatives\ntags: [gex]\ncreated: 2026-05-01\nreviewed: true\nsource_origin: a.md", "Old.\n")
    new = note("domain: derivatives\ntags: [walls]\naliases: [GEX]", "New fact.\n")
    merged, changed = ingest.merge_note(old, new, "b.md", TODAY)
    assert changed
    fm, body = ingest.split_frontmatter(merged)
    assert fm["tags"] == ["gex", "walls"] and fm["aliases"] == ["GEX"] and fm["reviewed"] is False
    assert str(fm["created"]) == "2026-05-01" and fm["sources"] == ["a.md", "b.md"]
    assert body.count("## Update from b.md (2026-10-02)") == 1 and "Old." in body and "New fact." in body
    again, changed2 = ingest.merge_note(merged, new, "b.md", TODAY)
    assert not changed2 and again == merged


def test_merge_ignores_identical_body():
    old = note("domain: meta", "Same body.\n")
    _, changed = ingest.merge_note(old, note("domain: meta", "Same   body.\n"), "x.md", TODAY)
    assert not changed


# ---------------------------------------------------------------- commit_blocks


def test_commit_creates_merges_and_protects(vault):
    blocks = [
        ingest.NoteBlock("wiki/concepts/Loss Versus Rebalancing.md",
                         note("domain: cl-market-making\ntags: [lvr]\ncreated: 2026-10-02", "# LVR\n")),
        ingest.NoteBlock("wiki/concepts/gex.md", note("domain: derivatives\naliases: [GEX]", "Walls matter.\n")),
        ingest.NoteBlock("wiki/concepts/gamma exposure.md", note("domain: derivatives", "Alias hit.\n")),
        ingest.NoteBlock("wiki/dlmm/adr/adr-052-ev-gate.md", note("domain: meta", "overwrite attempt\n")),
        ingest.NoteBlock("../../evil.md", "x"),
    ]
    results = ingest.commit_blocks(blocks, "paper.md", dry_run=False, today=TODAY, wiki_dir=vault)
    actions = [(r.action, r.rel_path) for r in results]
    assert actions[0] == ("created", "wiki/concepts/loss-versus-rebalancing.md")
    assert actions[1] == ("merged", "wiki/concepts/gamma-exposure-gex.md")  # alias 'GEX' -> canonical note
    assert actions[2] == ("merged", "wiki/concepts/gamma-exposure-gex.md")  # alias 'gamma exposure'
    assert actions[3][0] == "rejected:protected:dlmm"
    assert actions[4][0] == "rejected:traversal"
    assert not (vault / "concepts" / "gex.md").exists()
    canonical = (vault / "concepts" / "gamma-exposure-gex.md").read_text(encoding="utf-8")
    assert "Original body." in canonical and "Walls matter." in canonical and "Alias hit." in canonical
    assert "overwrite attempt" not in (vault / "dlmm" / "adr" / "adr-052-ev-gate.md").read_text(encoding="utf-8")
    created_fm, _ = ingest.split_frontmatter((vault / "concepts" / "loss-versus-rebalancing.md").read_text(encoding="utf-8"))
    assert created_fm["domain"] == "cl-market-making" and created_fm["source_origin"] == "paper.md"


def test_commit_never_merges_into_bridge_managed_via_alias(vault):
    adr = vault / "dlmm" / "adr" / "adr-052-ev-gate.md"
    adr.write_text(note("domain: cl-market-making\nbridge_managed: true\naliases: [EV gate]", "# ADR-052\n"), encoding="utf-8")
    results = ingest.commit_blocks([ingest.NoteBlock("wiki/concepts/ev-gate.md", note("domain: meta", "x\n"))],
                                   "p.md", dry_run=False, today=TODAY, wiki_dir=vault)
    assert results[0].action == "rejected:bridge-managed"
    assert adr.read_text(encoding="utf-8").endswith("# ADR-052\n")


def test_commit_rerun_is_noop_and_dry_run_writes_nothing(vault):
    block = ingest.NoteBlock("wiki/concepts/fee-growth.md", note("domain: cl-market-making", "Fees.\n"))
    first = ingest.commit_blocks([block], "s.md", dry_run=False, today=TODAY, wiki_dir=vault)
    second = ingest.commit_blocks([block], "s.md", dry_run=False, today=TODAY, wiki_dir=vault)
    assert first[0].action == "created" and second[0].action == "skipped:unchanged"
    dry = ingest.commit_blocks([ingest.NoteBlock("wiki/concepts/new-one.md", note("domain: meta", "N\n"))],
                               "s.md", dry_run=True, today=TODAY, wiki_dir=vault)
    assert dry[0].action == "created" and not (vault / "concepts" / "new-one.md").exists()


def test_is_ignorable():
    for name in (".hidden.md", "~syncthing~x.md.tmp", "paper.sync-conflict-20261002-1.md", "x.part", "y.tmp"):
        assert ingest.is_ignorable(Path(name))
    assert not ingest.is_ignorable(Path("paper.pdf"))


# ---------------------------------------------------------------- link normalisation and created date


def test_normalize_links_strips_folders_for_existing_notes(vault):
    index = ingest.build_slug_index(vault)
    body = ("See [[curriculum/gamma-exposure-gex|GEX]], [[../concepts/gamma-exposure-gex.md]], "
            "[[gamma-exposure-gex#walls|walls]], and [[future/not-yet-a-note|later]].")
    out = ingest.normalize_links(body, index)
    assert "[[gamma-exposure-gex|GEX]]" in out
    assert "[[gamma-exposure-gex]]" in out
    assert "[[gamma-exposure-gex#walls|walls]]" in out
    assert "[[future/not-yet-a-note|later]]" in out  # unknown targets are left alone


def test_commit_forces_created_to_today(vault):
    block = ingest.NoteBlock("wiki/concepts/x-note.md", note("domain: meta\ncreated: 2023-10-27", "Body [[concepts/gamma-exposure-gex|g]].\n"))
    results = ingest.commit_blocks([block], "s.md", dry_run=False, today=TODAY, wiki_dir=vault)
    fm, body = ingest.split_frontmatter((vault / "concepts" / "x-note.md").read_text(encoding="utf-8"))
    assert str(fm["created"]) == TODAY and "created 2023-10-27" in results[0].detail
    assert "[[gamma-exposure-gex|g]]" in body
