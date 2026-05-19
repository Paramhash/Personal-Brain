---
tags:
  - board-directive
  - observer-track
  - maopm
  - governance
  - human-in-the-loop
created: 2026-05-19
reviewed: true
source_origin: maopm-design
---
# Board Directive Protocol

The **Board Directive Protocol** defines how the operator (the Board — i.e., the human principal) issues binding instructions to the [MAOPM](../research/current%20research%20initiatives.md) system that persist across cycles, override agent recommendations, and are enforced at the [Portfolio Manager](../concepts/fund-manager-agent.md) and [Risk Team](../concepts/risk-management-team-agent.md) level. It is the mechanism by which the Board exercises governance without disrupting the Agent State Track mid-cycle.

## Motivation

The MAOPM agent architecture is autonomous within a cycle. Left unconstrained, agents optimize for the Greek-target and strategy signals they receive — they have no persistent awareness of Board-level context (e.g., "we are approaching earnings season," "I expect elevated macro risk this week," "do not open new positions until I review the Q4 report"). Without a formal directive protocol, the only way to communicate such constraints is to modify agent prompts or system parameters manually — ad hoc, unlogged, and inconsistent across cycles.

The Board Directive Protocol solves this by providing a structured, logged, enforceable mechanism for Board instructions.

## Directive Structure

```json
{
  "directive_id": "uuid-v4",
  "issued_at": "ISO-8601",
  "issued_by": "Board",
  "content": "No new short-vol positions until VIX closes below 20 for two consecutive sessions.",
  "scope": "persistent | cycle-local | expiry-date",
  "expiry": "ISO-8601 | null",
  "priority": "hard-block | advisory",
  "affects": ["Short-Vol Researcher", "Portfolio Manager", "Risk Team"],
  "status": "active | expired | revoked",
  "revoked_at": "ISO-8601 | null",
  "revocation_reason": "..."
}
```

## Scope and Priority

### Scope
- **`persistent`**: Active indefinitely until explicitly revoked by the Board. Survives process restarts.
- **`cycle-local`**: Active for the current cycle only; auto-expires at MONITORING phase completion.
- **`expiry-date`**: Active until a specified timestamp (e.g., "expires after earnings close on 2026-05-22T16:00:00Z").

### Priority
- **`hard-block`**: Automatically causes rejection of any trade proposal that violates the directive. The [Portfolio Manager](../concepts/fund-manager-agent.md) or [Risk Team](../concepts/risk-management-team-agent.md) records a `rejection` entry in the [Decision Ledger](../concepts/decision-ledger.md) with `disposed_by: "Board"` and cites the `directive_id`. No agent debate can override a hard-block.
- **`advisory`**: Presented to the Research Team and Portfolio Manager as a constraint preference. Agents may override with explicit rationale. The rationale for override is logged as a `debate-turn` entry linked to the directive.

## Enforcement Points

Board directives are enforced at two points in the Track 1 state machine:

1. **Portfolio Manager** (REVIEWING phase): Before approving a trade proposal, the Portfolio Manager checks the Active Directives List (delivered via Seam B). If any `hard-block` directive applies to the proposed trade, the proposal is auto-rejected and a `rejection` entry is written to the ledger.
2. **Risk Team** (REVIEWING phase): The Risk Team's approval step also checks the Active Directives List as a secondary enforcement gate. An advisory directive is included in the Risk Team's deliberation context.

The Board can also issue a **force-restart directive** that interrupts the state machine at any state and reverts to ANALYZING. This is recorded as a `board-override` entry in the [Decision Ledger](../concepts/decision-ledger.md).

## Board Interrupt Path

In addition to per-cycle directives, the Board can trigger:

- **Forced cycle restart** (any state → ANALYZING): Used when market conditions change rapidly and the current cycle's analysis is stale.
- **Emergency halt** (any state → suspended): Blocks all new order submission; existing positions remain open. Requires explicit Board resume to lift.

Both interrupt types are logged as `board-override` entries with full timestamp and rationale.

## Active Directives List (Seam B)

The [Recording Secretary](../concepts/recording-secretary-agent.md) compiles the Active Directives List from the [Decision Ledger](../concepts/decision-ledger.md) at the start of each ANALYZING phase and delivers it to Track 1 via Seam B as part of the Prior Decisions Context Block:

```json
{
  "active_directives": [
    {
      "directive_id": "...",
      "priority": "hard-block",
      "content": "No new short-vol positions until VIX < 20 for two consecutive sessions.",
      "issued_at": "2026-05-19T09:00:00Z",
      "expiry": null
    }
  ]
}
```

## Accountability

Every directive issuance, expiry, and revocation is logged in the Decision Ledger as a `board-directive` entry. Every rejection caused by a directive is linked to that directive's `directive_id`. This creates a closed audit trail: Board directive → rejected trade → logged rationale → queryable history.

## Related Concepts

- [[recording-secretary-agent.md]] — The agent that logs all directives and delivers the Active Directives List via Seam B
- [[decision-ledger.md]] — Where all directive entries and directive-caused rejections are stored
- [[fund-manager-agent.md]] — Primary enforcement point for hard-block directives
- [[risk-management-team-agent.md]] — Secondary enforcement point and advisory directive context
