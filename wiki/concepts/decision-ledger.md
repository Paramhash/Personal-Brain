---
tags: ["decision-ledger", "audit-trail", "observer-track", "maopm", "data-model"]
created: 2026-05-19
reviewed: false
source_origin: "maopm-design"
---
# Decision Ledger

The **Decision Ledger** is the append-only, persistent record of all decisions, recommendations, debates, fills, and Board directives produced by the [MAOPM](../research/Current%20Research%20Initiatives.md) system. It is maintained exclusively by the [Recording Secretary](../concepts/recording-secretary-agent.md) in the Observer Track. It is the system's authoritative state on restart and the primary source for performance attribution.

## Design Principles

- **Append-only**: Entries are never modified or deleted. Corrections are new entries with `type: "correction"` referencing the original `entry_id`.
- **Cycle-linked**: Every entry carries a `cycle_id` that links it to the MAOPM analysis cycle in which it was produced. This enables full cycle-level audit reconstruction.
- **Source-attributed**: Every entry records its `source` (agent name, "Board", or "System") — no anonymous entries.
- **Disposition-tracked**: Every recommendation and proposal entry reaches a final `disposition` (`approved`, `rejected`, `overridden`, `expired`) before the cycle closes.

## Entry Schema

All ledger entries share a common envelope:

```json
{
  "entry_id": "uuid-v4",
  "cycle_id": "2026-05-19T09:30:00Z",
  "timestamp": "ISO-8601",
  "source": "agent-name | Board | System",
  "type": "entry-type",
  "content": { },
  "disposition": "pending | approved | rejected | overridden | expired | n/a",
  "disposed_by": "agent-name | Board | n/a",
  "disposed_at": "ISO-8601 | null",
  "rationale": "free text",
  "tags": []
}
```

## Entry Types

| Type | Produced by | When |
|---|---|---|
| `board-directive` | Board Interface | Board issues a directive |
| `analyst-report` | Any Analyst agent | ANALYZING phase completes |
| `agent-recommendation` | Researchers, Portfolio Manager | DEBATING / REVIEWING phase |
| `debate-turn` | Long-Vol / Short-Vol Researchers | Each turn in the debate |
| `approval` | Portfolio Manager, Risk Team | Proposal approved |
| `rejection` | Portfolio Manager, Risk Team | Proposal rejected |
| `board-override` | Board Interface | Board forces a state transition or blocks a trade |
| `fill` | Execution Agent | Order filled |
| `greek-breach` | Greeks Analyst, Risk Team | Greek threshold crossed |
| `expiry-alert` | System / Expiration monitor | DTE threshold reached |
| `performance-summary` | Performance Observer | Post-close attribution entry |
| `correction` | Recording Secretary | Erroneously recorded entry requires annotation |

## Content Schema by Type

### `agent-recommendation`
```json
{
  "strategy": "iron condor",
  "underlying": "SPY",
  "legs": [],
  "dte": 45,
  "max_loss": -1500,
  "pop": 0.72,
  "net_greek_impact": { "delta": 12, "gamma": -0.8, "vega": -180, "theta": 42 },
  "rationale": "IVR at 68, GEX coherent, positive theta targeting $42/day"
}
```

### `greek-breach`
```json
{
  "metric": "net_vega",
  "threshold": 3000,
  "current_value": 3420,
  "position_id": "...",
  "required_action": "reduce vega exposure before next cycle"
}
```

### `fill`
```json
{
  "order_id": "...",
  "underlying": "SPY",
  "strategy": "iron condor",
  "legs": [],
  "fill_price": 2.85,
  "mid_at_fill": 2.90,
  "slippage": -0.05,
  "timestamp": "..."
}
```

### `performance-summary`
```json
{
  "position_id": "...",
  "originating_cycle_id": "...",
  "originating_recommendation_entry_id": "...",
  "result": "profit",
  "pnl": 285,
  "pop_predicted": 0.72,
  "realized_win": true,
  "iv_at_entry": 0.28,
  "realized_vol": 0.19,
  "iv_premium_captured": 0.09,
  "theta_captured": 320,
  "theta_from_realized_moves": -35
}
```

## Query Patterns

The ledger supports several standard query patterns used by the [Recording Secretary](../concepts/recording-secretary-agent.md) to generate the Prior Decisions Context Block:

- **Last N approved proposals**: Filter `type = "approval"`, sort by `timestamp desc`, limit N
- **Active Board directives**: Filter `type = "board-directive"`, `disposition = "pending"`, `content.expiry > now()`
- **Cycle reconstruction**: Filter by `cycle_id` to reconstruct the full audit trail for a single cycle
- **Agent accountability**: Filter by `source = "Short-Vol Researcher"` + `type = "agent-recommendation"` to review all recommendations by a specific agent
- **Performance attribution**: Join `fill` entries to `performance-summary` entries via `position_id`
- **Directive enforcement history**: Filter `type = "rejection"`, join to `board-directive` entries via `directive_id` in `rationale`

## Storage Options

Storage format is deferred to implementation. Candidates:

| Option | Pros | Cons |
|---|---|---|
| Append-only JSONL file | Simplest; zero dependencies; human-readable | No indexed queries; full-file scans for complex filters |
| SQLite | Queryable; single file; no server required | Concurrent write limits (single-writer model fits MAOPM) |
| Time-series DB (InfluxDB, TimescaleDB) | Optimized for time-indexed event streams | Additional infrastructure; overkill for Phase 1 |

**Recommendation for Phase 1**: SQLite with a single `entries` table indexed on `cycle_id`, `type`, `source`, and `timestamp`. Migrate to a time-series store if query latency becomes a bottleneck in Phase 2+.

## Related Concepts

- [[recording-secretary-agent.md]] — The agent that writes all entries to this ledger
- [[board-directive-protocol.md]] — Defines the `board-directive` entry type in detail
- [[structured-communication-protocol.md]] — JSON-schema enforcement that ensures `content` fields are well-formed
