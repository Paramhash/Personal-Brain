---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-009
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/009-orchestration-loop-architecture.md
bot_commit: 93d497d
source_sha256: 4ae629c5ff844a1d879f1e7e4eab85fb29f9f3503641fc2e588e75b3784915e9
exported_at: '2026-10-02T12:50:24Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/009-orchestration-loop-architecture.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-009-orchestration-loop-architecture|ADR-009]] — Orchestration loop architecture

- **Date:** 2026-09-15
- **Status:** accepted
- **Context:** The repository has isolated producers and consumers: the Deribit WebSocket
  client produces normalized snapshots; the GEX engine produces `SolGexSignalPayload`; the
  macro and operational FSMs consume distinct boundary facts; and the DLMM withdrawal
  executor performs the first venue action. No composition root currently wires those
  components into an end-to-end event pipeline. The State domain now owns durable restart
  state and requires `INITIALIZING` to reconcile it against live venue facts before
  operational work resumes.
- **Decision:** Implement `src/index.ts` as the singular composition root. It must run a
  strictly sequential, event-driven pipeline. On boot it must synchronously call
  `stateStore.loadSync()` and run `reconcileBootState` before opening any persistent network
  stream. One-off REST/RPC queries needed to gather the live venue facts consumed by
  `reconcileBootState` are authorized and required before that reconciliation completes.
  The Deribit WebSocket snapshot callback is the primary clock: each fresh
  snapshot is processed in order by the GEX engine, then the Macro FSM, then the Operational
  FSM. Any edge-triggered `ExecutionIntentEvent` is passed only to the Operational FSM. An
  `UNWINDING` operational state invokes the existing DLMM withdrawal boundary and feeds its
  reconciled status back through the established FSM and state-store boundaries.
- **Consequences:** The bot is event-driven rather than poll-loop driven. No later pipeline
  stage starts before its preceding intelligence or reconciliation fact is available. Venue
  actions remain strictly sequenced behind the intelligence heartbeat, preserving the
  `PARTIAL` and confirmation requirements of `execution_router.md` and `risk_guardrails.md`.
  The composition root coordinates existing components but does not absorb their ownership:
  it performs no GEX math, state persistence implementation, or venue-specific transaction
  construction.
- **Alternatives rejected:**
  - Let the Deribit client call the GEX engine directly: crosses Market Data into Intelligence
    ownership and makes the transport callback a hidden orchestration loop.
  - Let either FSM open sockets or invoke the withdrawal executor directly: violates the
    hierarchical FSM boundary and makes pure reducers venue-aware.
  - Start persistent WebSocket streams before boot reconciliation: risks acting on stale or
    incomplete durable state and violates `state_store.md` §3.
  - Use concurrent independent timers for intelligence and execution: permits stale facts or
    unreconciled venue outcomes to race later steps.
