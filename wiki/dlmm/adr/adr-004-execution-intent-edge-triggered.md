---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-004
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/004-execution-intent-edge-triggered.md
bot_commit: 93d497d
source_sha256: 5087dee07636028d11eae0c505a37a6408df248a4d4905c56b6850b9035a9cca
exported_at: '2026-10-02T12:50:24Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/004-execution-intent-edge-triggered.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-004-execution-intent-edge-triggered|ADR-004]] — `ExecutionIntentEvent` is edge-triggered, not level-triggered

- **Date:** 2026-09-14
- **Status:** accepted
- **Context:** [[adr-002-hierarchical-fsm-boundary|ADR-002]] establishes `ExecutionIntentEvent` as the sole forward transport
  from macro policy into operational execution, and `state_machine.md` §4.0 maps entering
  `DEFENSIVE_WITHDRAWAL` to `{ action: 'WITHDRAW' }` and entering `REDEPLOYMENT` to
  `{ action: 'REDEPLOY' }`. Neither says what happens on the ticks *after* entry. The
  question is forced by F-004, whose macro FSM remains in `DEFENSIVE_WITHDRAWAL` with the
  action `REQUEST_DEFENSIVE_WITHDRAWAL` attached to every tick until withdrawal is
  confirmed on-chain. Read literally as a level signal, that re-issues a withdrawal intent
  on every Q003 snapshot — at the assumed 5-second cadence — while an exit is already in
  flight. F-004's own integration assertion that `DEFENSIVE_WITHDRAWAL` must be idempotent
  while confirmation is pending is then satisfied only by downstream de-duplication, which
  places the burden on the wrong layer.
- **Decision:**
  - `ExecutionIntentEvent` is emitted only on the transition that **enters**
    `DEFENSIVE_WITHDRAWAL` or `REDEPLOYMENT`.
  - A tick on which the macro state does not change emits `null`.
  - Leaving a state and later re-entering it emits a new event; the edge is per-entry, not
    per-process.
  - The `REQUEST_DEFENSIVE_WITHDRAWAL` and `REQUEST_REDEPLOYMENT` actions carried on a
    decision are **telemetry** — they describe why the macro layer is still in that state.
    They are not commands and do not cross the boundary.
  - The operational actuator FSM must treat an arriving intent as a one-shot edge and own
    its own job persistence thereafter.
- **Consequences:** The operational FSM cannot be implemented as a poller of "the current
  intent"; once the edge arrives it runs the job to a confirmed terminal condition on its
  own, which is what `state_machine.md` §4.1 already requires of every non-hub state.
  Recovery from a dropped or unconfirmed intent runs through the operational layer's own
  confirmation logic and its `DEFENSIVE_HOLD` fault edge, not through repeated delivery —
  so that fault edge is load-bearing rather than incidental. Boundary traffic is
  proportional to regime changes rather than to snapshot cadence, which keeps the replay
  log readable. The cost is that the transport is assumed reliable in-process; if the two
  FSMs are ever split across a process or queue boundary, that assumption needs an explicit
  delivery guarantee and this ADR should be revisited.
- **Alternatives rejected:**
  - Re-emit on every tick while the state persists. Turns the operational FSM into a level
    follower, contradicts the job model in §4.1, and pushes de-duplication downstream.
  - Emit nothing and let the operational layer read macro state directly. Violates [[adr-002-hierarchical-fsm-boundary|ADR-002]]:
    the event is the only transport across the boundary.
  - Emit on entry and additionally on a slow keepalive interval. Reintroduces level
    semantics with extra timing state, and no failure mode currently justifies it.
