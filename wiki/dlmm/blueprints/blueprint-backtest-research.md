---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/backtest_research.md
bot_commit: e532796
source_sha256: ab0f3575e60df0ce080b20f56256c53bc9c85aea443c997caecc104a181e4b8a
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/backtest_research.md` at commit `e532796`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Backtest Research — Offline Policy Simulation over Recorded Series

**Domain owner:** offline research simulation of concentrated-liquidity policies over archived data
**Status:** authored and binding (2026-09-28, [[adr-043-research-simulator-reads-archive-offline|ADR-043]])
This file fixes what the research simulator may read, what it may import, what it computes, and how its
results must be labelled.

---

## 1. Scope

This blueprint governs `src/backtest/research/`: a read-only simulator that replays recorded pool, bin, spot
and wall series through candidate **placement**, **close** and **redeploy** policies for a DLMM
concentrated-liquidity position, and reports each policy's costs and break-even.

It exists to answer, with evidence rather than judgment: **where** to deploy (the [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] σ window, or between
the put and call walls), and **when** to close and redeploy.

It does not own live placement (`range_planning.md`), live exits (`state_machine.md`), the EV gate
(`ev_policy.md`), hedge execution (`hedge_engine.md`), or the archive (`observation_archive.md`). It changes
none of them. A policy it favours becomes live behaviour only through an ADR and the owning domain's ticket.

---

## 2. What it may read

- The observation archive's day files — `pool_samples`, `bin_samples`, `spot_samples`, `run_events`, plain or
  gzipped — **offline, after the fact, read-only** ([[adr-043-research-simulator-reads-archive-offline|ADR-043]]). `observation_archive.md` §4 forbids runtime
  readers; an offline reader of closed and live day files is neither a writer nor a runtime consumer.
- TICKET N / TICKET T recon `decisions-YYYY-MM-DD.jsonl` files, read-only. Separate recon runs are **never
  joined** into one continuous series.
- Nothing else. No venue, no RPC, no network.

It writes one file: the report named by the operator (`--out`).

## 3. What it may import

- `src/intelligence/range/rangePlanner` — `targetHalfBins`, `placeWindow` (the live σ-width arithmetic, reused
  so the simulated window is the live window).
- `src/config/deployRentModel` and `src/config/strategy.config` — rent arithmetic and `MAX_BINS_PER_POSITION`.
- `src/observation/types` — record shapes.
- `src/intelligence/volatility/trailingSigma` — the [[adr-047-provisional-sigma-estimator|ADR-047]] σ arithmetic, shared with the monitors (TICKET Z).
- Nothing from `src/execution/**`, `src/decision/fsm/**`, `src/index.ts`, or any signer. An import-graph test
  enforces this. The hedge target `q* = −x` (`hedge_engine.md` §2) is **restated**, not imported, because its
  home imports the execution layer.

## 4. What it computes

- **Exact DLMM bin accounting.** Each bin is constant-sum: its liquidity `L_b = p_b·x_b + y_b` is invariant, so
  a position's composition is a function of the active bin alone (base above, quote below, the active bin
  split). Unhedged P&L against HODL is therefore exact impermanent loss for the recorded active-bin path.
- **Hedged P&L** with a discrete short re-hedged outside a band, charging taker cost and funding.
- **Cycle costs**: bin-array rent **only for arrays not yet initialised** (rent is paid once per array, ever),
  per-chunk transaction fees, and re-ratio slippage on the swapped notional.
- **Fee accrual in units of an unknown volume**, never in currency (§5).

## 5. The labelling rule — binding

**No fee volume is recorded anywhere** (`fee_observation` is null; [[adr-033-fee-yield-measurement-route|ADR-033]] rejected reserve-delta and
swap-parsing as measurement routes). The simulator therefore reports fees as `unitsOfV = Σ inRange ·
feeRate · share · Δt`, where `V` is the unknown quote volume per second through the active bin, and reports
each policy's **break-even** — the `V`, and the fee yield on capital, at which fees would cover its losses.

Every figure derived from `unitsOfV` must carry: **"units of V; not calibrated yield ([[adr-033-fee-yield-measurement-route|ADR-033]])"**. A break-even
ranks policies; it does not show any policy is profitable. Only [[adr-033-fee-yield-measurement-route|ADR-033]]'s measurement route can.

## 6. Units

σ is **per second**, and every σ identifier says so. `realizedVol1m_t`'s name (a per-second value named as if
1-minute) is the hazard this rule exists not to repeat.

## 7. Prohibitions

- Do not import execution, FSM, or signer code; do not open a socket.
- Do not bridge a gap: a seq break, a run change or a stale input ends a segment.
- Do not present break-even figures as profitability, or as fee-yield ratification.
- Do not write anywhere but the requested report.

---

## 8. [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] evidence sections (TICKET W)

The report carries two sections that exist to ratify, or refute, [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s hurdle model. Neither changes a policy
ranking, and sections A–E are byte-identical with or without them.

- **§F — model vs simulator.** Each open evaluates the model (`src/intelligence/range/hurdleMath.ts`, the same
  equations the EV domain and the monitor use) for its own range, σ (trailing 24 h at the open) and capital. The
  model's LVR and hedge-taker rates accrue over the same deployed seconds the simulator accounts exactly, and are shown
  in bps of capital per day beside the simulator's LVR-equivalent and discrete-hedge taker cost, with ratios. The
  model's expected lifespan is shown beside observed episodes, which segment ends can cut short. §F.2 gives the ratio
  per UTC day for the headline top 10.
  - **Since [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] the model is the EV gate's own** (TICKET 028). The simulator calls `rangeCostRates` with ρ̄, the
    trailing 24 h Deribit σ × `poolSpotSigmaRatio`, and `poolBurstFactor`.
  - **§F.3 is [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D2's form test** (`src/backtest/research/formTest.ts`). It gives the model the **pool's own σ
    realized over the next 24 h** (`SimParams.modelPoolSigma`), so the σ forecast is taken out. It then judges the
    median model ÷ simulator per term: within ±25% on the whole span, and within ±50% for every UTC day of at least 18 h.
    Shorter days are shown but not judged. The verdict is printed as PASS or FAIL.
- **§G — regime σ multipliers.** For each wall-covered tick, the regime is `classifyGexRegime` over the record's own
  total net GEX, spot and ZGL, keyed with spot's side of the ZGL. Non-overlapping 300 s returns give zero-mean σ per
  regime, its ratio to the σ of all returns used, the count, and a 95% interval. Nothing is written into a constant.

The shape weights these use were moved from `dlmmPosition.ts` to `src/intelligence/range/liquidityShape.ts` (TICKET W)
and are re-exported here unchanged, so the simulator still imports nothing from `src/decision/`.

## 9. The live σ chain in §H (TICKET Z, [[adr-047-provisional-sigma-estimator|ADR-047]])

- The σ arithmetic lives in `src/intelligence/volatility/trailingSigma.ts`; `research/sigma.ts` wraps it with no
  coverage or gap rule, so every earlier section is unchanged.
- `--orca-frames <dir>` and `--dlmm-frames <dir>` add a table to §H: each monitor's recorded [[adr-047-provisional-sigma-estimator|ADR-047]] estimate at hourly
  points, scored against the σ realized over the next 24 h, beside the archive's trailing 24 h σ and the placeholder on
  the same points.
- `recordedSigma.ts` keeps `observedAtMs` and `sigmaEstimate` from `tick` records and discards everything else as it
  parses ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1 A4). Offline and read-only, like the rest of the simulator.

## 10. Measured fee yield in §I (TICKET 027, [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Route 4)

- `--fee-growth <dir>` reads the fee-growth sampler's files (`feeGrowthReader.ts`) and passes them to `runPolicy` as
  `SimParams.feeGrowth`.
- **Crediting.** Whole sample intervals during which a position was open throughout are credited measured fees
  (`src/feegrowth/accrual.ts`): share = own value ÷ (bin value + own value), times the bin's LP fees from the counters.
  Partial intervals are left out. `unitsOfV` and every earlier section are unchanged.
- **§I contents:**
  - the top 10 σ-window policies, with coverage, measured bps/day, hedged break-even bps/day and the net;
  - §I.2: the top 5 by [[adr-033-fee-yield-measurement-route|ADR-033]] 3-day sub-window from the sampler's first `run_start`, with sampler coverage and the
    10th percentile of eligible windows (complete and ≥ 95% coverage);
  - the aggregate standing reconciliation.
- **Imports:** research imports `src/feegrowth/` pure modules (`accrual`, `binCounters`, `feeGrowthRecord`) only.
