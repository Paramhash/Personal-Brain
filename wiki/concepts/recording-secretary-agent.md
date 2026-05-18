---
tags: ["agent-role", "multi-agent-systems", "observer-track", "audit", "maopm"]
created: 2026-05-19
reviewed: false
source_origin: "maopm-design"
---
# Recording Secretary Agent

The **Recording Secretary** is a passive observer agent in the [MAOPM](../research/Current%20Research%20Initiatives.md) [Observer Track](../research/Current%20Research%20Initiatives.md) that maintains an immutable, append-only [Decision Ledger](../concepts/decision-ledger.md) of all system activity. It has no decision-making authority and participates in no debates. Its sole function is to observe every state transition and structured document produced by the Agent State Track and record them in a structured, queryable, human-readable form.

## Role in the Two-Track Architecture

The MAOPM operates on two parallel tracks:

- **Track 1 (Agent State Track)**: The decision/execution pipeline — Analysts → Researchers → Portfolio Manager → Risk Team → Execution Agent — running the state machine `ANALYZING → DEBATING → REVIEWING → APPROVED → EXECUTING → MONITORING`.
- **Track 2 (Observer Track)**: The Recording Secretary, [Board Interface](../concepts/board-directive-protocol.md), and Performance Observer — persistent, passive, providing longitudinal context across cycles.

The Recording Secretary sits entirely within Track 2. It receives events from Track 1 via **Seam A** (event emission interface) and contributes a **Prior Decisions Context Block** to Track 1 at the start of each ANALYZING phase via **Seam B** (context injection interface).

## Events Observed (Seam A Input)

The Recording Secretary subscribes to every state transition and document produced by Track 1:

| Event Type | Source | What is recorded |
|---|---|---|
| `state-transition` | State machine | From-state, to-state, cycle ID, timestamp |
| `analyst-report` | Any Analyst agent | Full JSON-schema document |
| `debate-turn` | Long-Vol / Short-Vol Researchers | Speaker, content, turn number, cycle ID |
| `agent-recommendation` | Any agent | Agent name, structured recommendation, rationale |
| `approval` | Portfolio Manager or Risk Team | Approver, approved proposal summary, cycle ID |
| `rejection` | Portfolio Manager or Risk Team | Rejector, reason, overriding directive (if any) |
| `board-override` | Board Interface | Directive ID, affected state, forced transition |
| `fill` | Execution Agent | Trade details, fill price, slippage vs. mid |
| `greek-breach` | Greeks Analyst or Risk Team | Breached metric, threshold, current value |
| `expiry-alert` | Expiration monitor | Position, DTE remaining, required action |

## Prior Decisions Context Block (Seam B Output)

At the start of each ANALYZING phase, the Recording Secretary generates a structured context block injected into Track 1. This block gives the current cycle's agents awareness of relevant history without requiring them to query the full ledger.

**Default content** (configurable):
- Last 5 approved trade proposals with outcome (open / closed profitable / closed at loss)
- All active [Board Directives](../concepts/board-directive-protocol.md) (hard-block and advisory)
- Last regime classification from the previous cycle
- Any unresolved Greek breach events from prior cycles
- The most recent Performance Observer summary (win rate vs. PoP, IV premium capture rate)

## Design Constraints

- **No LLM inference**: The Recording Secretary is fully deterministic. It formats and appends entries to the [Decision Ledger](../concepts/decision-ledger.md) using a fixed schema — no language model is involved.
- **Append-only**: Ledger entries are never modified or deleted after write. Corrections are new entries with `type: "correction"` referencing the original `entry_id`.
- **No veto authority**: The Recording Secretary cannot block, delay, or alter any Track 1 action. Its only influence on Track 1 is through the Prior Decisions Context Block (Seam B), which agents receive as read-only context.
- **Process-restart resilience**: Because Track 1 is in-memory per cycle, the Recording Secretary's ledger is the authoritative persistent state of the system. On restart, the ledger is the rehydration source.

## LLM Model Assignment

None. The Recording Secretary is a deterministic structured-data service, not an LLM agent. Implementation is a lightweight process (Python) that subscribes to Track 1 events and appends to the ledger store.

## Related Concepts

- [[decision-ledger.md]] — Schema, entry types, and query patterns for the ledger this agent maintains
- [[board-directive-protocol.md]] — Board directives that appear as `board-directive` entries in the ledger
- [[structured-communication-protocol.md]] — The JSON-schema enforcement this agent relies on to receive well-formed Track 1 events
- [[multi-agent-systems.md]] — General architecture context
