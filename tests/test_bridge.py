"""Offline tests for bridges/dlmm_bridge.py's pure helpers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bridges"))
import dlmm_bridge as b  # noqa: E402


def test_denied_paths():
    for rel in ("C:/observation/observer.env", ".env", "config/prod.env", "keys/devnet-keypair.json",
                "node_modules/x/README.md", "secrets/a.md", "x.pem"):
        assert b.denied(rel), rel
    for rel in ("docs/decisions/052-ev-gate.md", "docs/architect/observation_archive.md", "todo/findings/F-026 - x.md"):
        assert not b.denied(rel), rel


def test_find_secret():
    assert b.find_secret("-----BEGIN OPENSSH PRIVATE KEY-----")
    assert b.find_secret("https://discord.com/api/webhooks/123456/abcDEF-ghi")
    assert b.find_secret("API_KEY=abcdefghijklmnopqrstuvwxyz123456")
    assert b.find_secret("sk-ant-api03-abcdefghijklmnopqrstuv")
    assert b.find_secret("5" + "K" * 87)  # 88-char base58 secret key
    # Ordinary bot prose: a pool address (44 chars), env key NAMES without values, an hourly cron line.
    assert b.find_secret("pool 5rCf1DM8LjKTw4YqhnoLcngyZYeNnQqztScTogYHAS6 and `WHATELSE_DISCORD_WEBHOOK_URL`") is None
    assert b.find_secret("Set NOTIFIER_DISCORD_WEBHOOK_URL in notifier.env") is None


def test_mirror_slug():
    assert b.mirror_slug("adr", Path("052-ev-gate-prices-lvr.md")) == "adr-052-ev-gate-prices-lvr"
    assert b.mirror_slug("blueprint", Path("ev_policy.md")) == "blueprint-ev-policy"
    assert b.mirror_slug("report", Path("CL_POLICY_REPORT_2026-10-01.md")) == "cl-policy-report-2026-10-01"
    assert b.mirror_slug("finding", Path("F-026 - The EV gate has no rent term.md")) == "finding-f-026-the-ev-gate-has-no-rent-term"


def test_rewrite_links_and_adr_mentions():
    targets = {"docs/architect/ev_policy.md": "blueprint-ev-policy",
               "docs/decisions/046-hurdle.md": "adr-046-hurdle"}
    adrs = {"046": "adr-046-hurdle", "052": "adr-052-ev-gate"}
    text = (
        "See [the EV policy](../architect/ev_policy.md#3b) and ADR-046; ADR-099 is unknown.\n"
        "Inline `ADR-052` and `../architect/ev_policy.md` stay as code.\n"
        "```\nADR-052 in a fence\n```\n"
        "Already linked: [[adr-052-ev-gate|ADR-052]]. Unmirrored [x](../../src/a.md).\n"
    )
    out = b.rewrite_links(text, "docs/decisions/052-ev-gate.md", targets, adrs)
    assert "[[blueprint-ev-policy#3b|the EV policy]]" in out
    assert "[[adr-046-hurdle|ADR-046]]" in out and "ADR-099 is unknown" in out
    assert "`ADR-052`" in out and "`../architect/ev_policy.md`" in out
    assert "```\nADR-052 in a fence\n```" in out
    assert out.count("[[adr-052-ev-gate|ADR-052]]") == 1  # not double-wrapped
    assert "[x](../../src/a.md)" in out


def test_parse_adr_header():
    text = "# ADR-052 — The EV Gate Prices LVR\n\n- **Date:** 2026-10-01 (revised)\n- **Status:** **Active.** Ratified.\n"
    assert b.parse_adr_header(text) == ("The EV Gate Prices LVR", "Active. Ratified.", "2026-10-01")


def test_strip_volatile_ignores_date_and_commit():
    a = b.render_adr_index([("052", "adr-052-x", "T", "Active", "2026-10-01")], "abc1234")
    c = a.replace("abc1234", "def5678")
    assert b.strip_volatile(a) == b.strip_volatile(c)
