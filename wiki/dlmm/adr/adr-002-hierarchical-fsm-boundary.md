---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-002
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/002-hierarchical-fsm-boundary.md
bot_commit: 93d497d
source_sha256: 40bb639a70c7ff23bcbf0d7382cef85d74b64e8ea0a66bdee3b67f06a2577666
exported_at: '2026-10-02T12:50:24Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/002-hierarchical-fsm-boundary.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-002-hierarchical-fsm-boundary|ADR-002]] — Hierarchical FSM boundary

- **Date:** 2026-09-14
- **Status:** accepted
- **Context:** The active architecture carries two distinct state surfaces that solve different problems. The operational architecture in Q007 uses an eight-state actuator-oriented FSM to reconcile venues and sequence jobs such as `UNWINDING`, `REBALANCING`, `DEPLOYING`, and `HEDGING`. F-004 defines a five-state macro controller for regime policy: `MONITORING`, `THREAT_EVALUATION`, `DEFENSIVE_WITHDRAWAL`, `REGIME_OBSERVATION`, and `REDEPLOYMENT`. Flattening these into a single 13-state loop would merge policy and actuation, create colliding transitions around shared names such as `MONITORING`, and make the implementation fragile to partial execution and restart recovery.
- **Decision:** Formalize a strictly separated two-tier hierarchical FSM.
  - The Macro Strategy FSM owned by Q004 is a pure transition function over the five macro states. It consumes off-chain GEX intelligence, EV gating, hedge feasibility, and execution confirmation signals.
  - The Operational Actuator FSM owns the eight execution-oriented states and is the only layer that sequences venue-facing jobs.
  - The sole forward transport payload from macro policy into operational execution is `ExecutionIntentEvent` with `action: 'WITHDRAW' | 'REDEPLOY'`.
  - Entering `DEFENSIVE_WITHDRAWAL` at the macro level emits `ExecutionIntentEvent { eventType: 'EXECUTION_INTENT', action: 'WITHDRAW', priorityFeeMode: 'AGGRESSIVE' | 'NORMAL' }` and forces the operational FSM onto the `UNWINDING` path.
  - Entering `REDEPLOYMENT` at the macro level emits `ExecutionIntentEvent { eventType: 'EXECUTION_INTENT', action: 'REDEPLOY', priorityFeeMode: 'NORMAL' | 'AGGRESSIVE' }` and authorizes the operational redeploy sequence.
  - Claude Code is explicitly forbidden from flattening the five macro states and the eight operational states into a single loop. Q004 must remain isolated, pure, and side-effect free; the operational orchestrator consumes its emitted intents and performs the job sequence.
- **Consequences:** Policy and execution are now testable in isolation, restart recovery stays attached to the operational FSM, and macro transitions can be replayed without replaying venue side effects. The naming overlap around `MONITORING` is no longer ambiguous because macro and operational states live in separate state machines with a typed boundary event between them. This also means any future implementation that tries to embed RPC calls, exchange logic, or venue retries inside Q004 is a design defect.
- **Alternatives rejected:**
  - Flatten the five macro states and eight operational states into one 13-state loop.
  - Let the macro FSM call execution modules directly instead of emitting typed intent events.
  - Rename one of the state sets and still keep a single state machine implementation with mixed policy and execution concerns.
