---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/system_index.md
bot_commit: b5fb1ab
source_sha256: 47c4d150b25e2591ea135ac7839b13fdab301da16fa4b3f53021265c684cf935
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/system_index.md` at commit `b5fb1ab`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Blueprint Index — Spatial Map

**This file is a router, not a record.** It exists for one purpose: to send an agent
holding an active ticket directly to the blueprint file that owns that ticket's domain.

It contains no history, no decisions, no ADRs, no changelog, and no rationale.
If you are looking for *why* something is the way it is, you are in the wrong file.
This index only tells you *where* things live.

---

## 0. Mandatory protocol — read before writing any module

You are **required** to cross-reference the mapped blueprint file(s) for your domain
**before** you author a new module, add a public function, define a schema, or introduce
a dependency between components.

1. Identify your ticket's domain in §2.
2. Open every blueprint file that row points to — the primary **and** any listed neighbours.
3. Confirm your intended change fits the boundaries and data-flow direction those files declare.
4. Only then write code in `/development/src/`.

Writing first and reconciling afterwards is a boundary violation, even if the code works.
The blueprints define ownership and direction of data flow; code that works but crosses a
boundary is a defect.

**If your ticket maps to no domain below, or to a blueprint that does not yet exist:**
stop. Do not improvise a new subsystem. Record the gap in
`/development/docs/status/current.md` and escalate. A missing blueprint is a design
ticket, not a licence to invent structure.

---

## 1. Status of this map

`state_machine.md`, `protocol_contract.md`, `config_contract.md`,
`data_ingestion_flow.md`, `gex_intelligence.md`, `state_store.md`,
`hedge_engine.md`, `range_planning.md`, `liquidity_position_manager.md`,
`execution_router.md`, `observability_contract.md`, `ev_policy.md`, `risk_guardrails.md`, and
`observation_archive.md`, `backtest_research.md`, and `monitor.md` are authored and binding. Every other blueprint listed below is **forward-declared**: the filename and
ownership are fixed here so that routing is stable, but the file itself is authored when
its domain's first design ticket lands. The `Status` column is authoritative — never
assume a file is readable because it is named here.

The active application architecture is fixed as four operational modules:

| Module | Owns | Source roots |
| --- | --- | --- |
| Market Data | Deribit options summaries, Solana DLMM state, Binance hedge-state feeds | `src/marketdata/deribit/`, `src/marketdata/solana/`, `src/marketdata/binance/` |
| Intelligence | Deterministic GEX profile construction and wall-to-range planning | `src/intelligence/gex/`, `src/intelligence/range/` |
| FSM Orchestration | State progression, EV gating, hedge intent, guard evaluation, and the singular composition root | `src/index.ts`, `src/decision/ev/`, `src/decision/fsm/` |
| Execution | Solana actuators and Binance hedge execution | `src/execution/solana/`, `src/execution/hedge/` |

The production source root is fixed at `/development/src/`. Supporting subtree anchors
below are also fixed for routing purposes:

| Source root | Reserved for |
| --- | --- |
| `src/types/` | Shared protocol and event contracts |
| `src/config/` | Runtime configuration and pinned dependency policy |
| `src/backtest/` | Replay, scenarios, and metrics |
| `src/observation/` | Durable read-only observation series for later calibration ([[adr-032-observation-archive-ownership-and-isolation|ADR-032]]) |

The flattened source layout is mandatory. In particular:

- no duplicated `src/src/` subtree may exist
- `jupiterSwap.ts` belongs under `src/execution/solana/`, not at the root of `src/`
- hedge execution files belong under `src/execution/hedge/`
- GEX analytics belong under `src/intelligence/gex/`
- range-planning files belong under `src/intelligence/range/`
- `src/index.ts` is the singular FSM Orchestration composition root; it wires approved
  boundaries but does not own venue clients, analytics, reducers, or durable-state internals

No active source root exists for Orca venue adapters, ONNX inference, VPIN analytics,
or model artefacts. Introducing one is a design violation unless a later ADR says otherwise.
`src/observation/` is such an exception, authorized by **[[adr-032-observation-archive-ownership-and-isolation|ADR-032]]**. `src/monitor/venue/` is another, authorized
by **[[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]**: a read-only Orca Whirlpool pool adapter for the monitor only — no trading, planning, or FSM path.

---

## 2. Domain → blueprint routing table

| If your ticket concerns… | Read this blueprint | Also cross-reference | Implementation root | Status |
| --- | --- | --- | --- | --- |
| Shared protocol schemas, event types, cross-module payload contracts | `protocol_contract.md` | `state_machine.md`, `execution_router.md` | `src/types/` | authored |
| Deribit options summaries, Solana account streams, Binance hedge-state feeds, snapshot normalization | `data_ingestion_flow.md` | `protocol_contract.md`, `state_store.md` | `src/marketdata/` | authored |
| Deterministic gamma math, Dollar GEX aggregation, walls, zero-gamma extraction | `gex_intelligence.md` | `data_ingestion_flow.md`, `protocol_contract.md` | `src/intelligence/gex/` | authored |
| Range planning from Call Wall, Put Wall, and zero-gamma context into deploy bounds | `range_planning.md` | `gex_intelligence.md`, `liquidity_position_manager.md` | `src/intelligence/range/` | authored |
| DLMM position lifecycle — deploy bounds, bin ranges, liquidity shape, rebalance triggers | `liquidity_position_manager.md` | `range_planning.md`, `execution_router.md` | `src/execution/solana/` | authored |
| Expected-value gating, projected fees, projected LVR, funding drag, execution friction | `ev_policy.md` | `gex_intelligence.md`, `risk_guardrails.md` | `src/decision/ev/` | authored |
| **State machine, transitions, guards, orchestration, collision safety** | **`state_machine.md`** | `risk_guardrails.md`, `state_store.md`, `execution_router.md` | **`src/decision/fsm/`** | **authored** |
| Hedge targets, delta-neutrality rules, Binance hedge feasibility, hedge reconciliation inputs | `hedge_engine.md` | `protocol_contract.md`, `risk_guardrails.md` | `src/execution/hedge/` | authored |
| Solana and Binance transaction construction, RPC calls, retries, idempotency, venue adapters | `execution_router.md` | `risk_guardrails.md`, `protocol_contract.md` | `src/execution/` | authored |
| Exposure caps, kill switches, circuit breakers, stale-intelligence blocks, pre-trade checks | `risk_guardrails.md` | `hedge_engine.md`, `ev_policy.md` | `src/decision/` | authored |
| In-memory/on-disk state, restart recovery, partial execution reconciliation | `state_store.md` | `data_ingestion_flow.md`, `protocol_contract.md` | `src/` | authored |
| Config keys, environment variables, secret handling, pinned dependency policy | `config_contract.md` | `protocol_contract.md` | `src/config/` | authored |
| Logging, metrics emission, replay timing, anything surfaced in production telemetry | `observability_contract.md` | `state_store.md`, `execution_router.md` | `src/backtest/` | authored |
| Durable observation history recorded for later calibration — read-only venue sampling, gap semantics, retention | `observation_archive.md` | `state_store.md`, `observability_contract.md`, `ev_policy.md`, `data_ingestion_flow.md` | `src/observation/` | authored |
| Offline research simulation of CL policies over recorded series — placement, close/redeploy, costs, break-even ([[adr-043-research-simulator-reads-archive-offline|ADR-043]]) | `backtest_research.md` | `observation_archive.md`, `range_planning.md`, `ev_policy.md`, `hedge_engine.md` | `src/backtest/research/` | authored |
| Local read-only operator monitor — live and replay display of GEX, walls, envelope, recommended window; read-only pool venue adapters, incl. Orca Whirlpool ([[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]); the Orca monitor's own frame recording and replay ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]]); operator health alarms to Discord ([[adr-048-health-alarms-to-the-operators-discord|ADR-048]]) | `monitor.md` | `gex_intelligence.md`, `range_planning.md`, `observation_archive.md`, `config_contract.md` | `src/monitor/` | authored |
| On-chain per-bin fee growth for fee-yield measurement without capital — the read-only sampler, its record, the standing reconciliation, and research §I ([[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]], Route 4) | `fee_growth.md` | `observation_archive.md`, `backtest_research.md`, `monitor.md`, `config_contract.md`, `observability_contract.md` | `src/feegrowth/` | authored |

---

## 3. Conditional routing — plain statements

- For **shared protocol schemas and cross-module payload contracts**, read `protocol_contract.md`.
- For **Deribit, Solana, or Binance intake and snapshot normalization**, read `data_ingestion_flow.md`.
- For **GEX profile construction, wall detection, or zero-gamma extraction**, read `gex_intelligence.md`.
- For **wall-to-range planning and deploy-bound derivation**, read `range_planning.md`.
- For **anything that opens, closes, widens, narrows, or rebalances a DLMM position**, read `liquidity_position_manager.md`.
- For **any state, transition, guard, or anything that changes what the bot is
  currently doing**, read `state_machine.md` — `MONITORING` is the hub and the only
  resting state; every other state is a job that must terminate back into it.
- For **EV gating, projected fee capture, LVR, funding drag, or friction budgeting**, read `ev_policy.md`.
- For **anything that sizes or adjusts a hedge**, read `hedge_engine.md`.
- For **anything that talks to a chain, an RPC endpoint, or an exchange**, read
  `execution_router.md` — no other module may hold that responsibility.
- For **any limit, cap, threshold, or halt condition**, read `risk_guardrails.md`.
- For **anything that must survive a process restart**, read `state_store.md`.
- For **any new config key or secret**, read `config_contract.md`.
- For **anything a human will read in production**, read `observability_contract.md`.
- For **a durable series recorded now to calibrate a constant later**, read
  `observation_archive.md` — it is a sibling observer, it holds no signer, and the trading process
  may never read it.

If a ticket touches **two** domains, read both blueprints and treat the stricter of the
two boundaries as binding.

---

## 4. Declared data-flow direction

Cross-referencing means checking direction, not just ownership. The top-level module flow is one-way:

```text
marketdata  →  intelligence  →  orchestration  →  execution  →  observability
```

At the finer blueprint level, the flow is still one-way:

```text
marketdata  →  state  →  intelligence  →  decision  →  risk  →  execution  →  observability

        [ observation ]        ← a sibling: reads venues read-only, writes only its own files
```

Reading against this arrow is permitted. **Writing against it is a boundary violation.**

The Observation domain sits outside the arrow entirely. It is downstream of nothing in the trading
pipeline and upstream of nothing, it writes to no other domain, and no other domain reads it at
runtime — see `observation_archive.md` §4.
In particular:

- Nothing upstream of `execution_router.md` may issue a transaction or call an RPC itself.
- `gex_intelligence.md`, `range_planning.md`, and `ev_policy.md` compute; they do not execute.
- `hedge_engine.md` and `liquidity_position_manager.md` propose actions; `risk_guardrails.md` may veto them; only `execution_router.md` performs them.
- No module reads another module's private state directly — it goes through `state_store.md`.

---

## 5. Not in this index

Deliberately excluded, so that this file stays a map:

- Historical decisions and architectural rationale — **not here**.
- Change history — **not here**.
- Ticket content, task lists, or work status — **not here**.

This index answers *where*. Nothing else.
