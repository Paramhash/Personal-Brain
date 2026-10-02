---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-052
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/052-ev-gate-prices-range-dependent-lvr-and-hedge-cost.md
bot_commit: 8a2bf46
source_sha256: 21c61e768c1b911f85772de0dc79333cd5113634013caa4221159f34752494f0
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/052-ev-gate-prices-range-dependent-lvr-and-hedge-cost.md` at commit `8a2bf46`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] — The EV Gate Prices Range-Dependent LVR and the Hedge's Taker Cost (the Ratifying ADR Under [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §5)

- **Date:** 2026-10-01 (revised 2026-10-01 14:50Z to TICKET 028 Part 0's findings)
- **Status:** **Active. Ratified by the dispatcher 2026-10-01 15:33Z, with D1–D5 as recommended:**
  - D1: ρ̄ + the pool's σ + the pool's burst factor;
  - D2: two tests, the form test here and the σ forecast under [[adr-047-provisional-sigma-estimator|ADR-047]];
  - D3: `m_regime = 1` until measured;
  - D4: the monitors and research first, the root only through [[adr-035-promotion-workflow|ADR-035]];
  - D5: σ_pool = `PlanningSigma` × 0.88.

  Implementation is TICKET 028 (Part 0 done; Part 0b at sub-window 2's close; Parts 1–6 now unblocked).
- **Would amend:**
  - `ev_policy.md` §3 (the canonical payload gains `projected_hedge_drag_quote`, and `projected_lvr_quote` becomes
    range-dependent);
  - `evCalculator.ts`'s `placeholderProjectedLvrQuote`, which loses `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER`;
  - [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]], whose `hurdle_model` LVR and hedge terms become the gate's, with ρ̄ and the pool factors ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] then
    becomes this ADR's history, per its §8).
- **Leaves unchanged:**
  - the §4 inequality `net_ev ≥ 1.5·(swap_slippage + gas_fees)`, textually;
  - the fee input ([[adr-033-fee-yield-measurement-route|ADR-033]]/050; [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Amendment 1 keeps a Route 4 value out until this ships);
  - funding ([[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]]) and rent ([[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]]);
  - [[adr-047-provisional-sigma-estimator|ADR-047]]'s σ estimator itself (the gate scales its output; see D5);
  - the hedge band `epsilonBase` and the hedge engine.
- **Evidence:**
  - `todo/findings/EV_GATE_VS_SIMULATOR_2026-10-01.md` (the gap);
  - `todo/findings/EV_GATE_CALIBRATION_2026-10-01.md` (TICKET 028 Part 0, both passes);
  - the scripts in `docs/operations/ev_gate_calibration/`;
  - research report §F and §I (`todo/research/CL_POLICY_REPORT_2026-10-01.md`).

## Context

**The gate's cost side is about an order of magnitude low for the ranges the planner actually places.**
- **The live state** (2026-10-01T13:50Z, 202-bin window, 50 SOL, placeholder σ):
  - **the gate:** LVR 3.8 bps/day, no hedge cost, hurdle 62.5;
  - **[[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s model:** LVR 183, hedge 191, hurdle 443;
  - **the research simulator:** a hedged break-even of about 270–330 bps/day.
- **LVR:** the gate uses full-range LVR, `σ²/8`, times a constant 1.8. Its effective value density is 0.45 at any
  width; the live window's is about 22. The constant's own doc comment says it should be derived from the range.
- **The hedge:** `net_ev` has no hedge term. At 30 s checks the 0.0625 SOL band is far below the per-check inventory
  move, so almost every check trades. At 5 bps taker that costs about 110–190 bps/day in the simulator.
- **This was known when [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] was decided** (its register entry: "3.81 bps/day at any width, against ≈105"). [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]
  kept the gate unchanged by design and set §5 as the path to change it: the model must agree with the simulator, the
  regime multipliers must be measured, and `ev_policy.md` must be amended.
- **Why it now needs deciding: the fee side is about to become real.**
  - Route 4 measures 80–141 bps/day (§I), and [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] D1 lets it ratify the fee input.
  - A ratified fee near 100 bps/day against today's 62.5 bps/day hurdle makes the gate **pass** positions the simulator
    nets at −150 to −240 bps/day.
  - [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Amendment 1 (**Active**, ratified 2026-10-01 14:38Z) holds Route 4's value out of the gate until this ADR is
    implemented.

### What calibration found (TICKET 028 Part 0)

[[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s model, run against the simulator's exact accounting, overstated both terms by about 2×. Three measured
corrections remove the gap; none is fitted to the simulator.

| Curve, model ÷ simulator | LVR | hedge |
|---|---:|---:|
| ρ(0), Deribit σ ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] as built) | 1.58 | 2.07 |
| ρ̄, realized Deribit σ | 1.28 | 1.50 |
| ρ̄, realized **pool** σ | **0.98** | 1.31 |
| ρ̄, realized pool σ, **burst factor 0.739** | 0.98 | **0.97** |

1. **ρ̄, not ρ(0).** ρ(0) is the density at the range's centre, where Curve is densest. The life-averaged density ρ̄
   weights each bin by the time driftless price is expected to spend there before leaving the range. It is 0.71 × ρ(0)
   for the live Curve window, 1.00 for Spot and 3.88 for BidAsk. With ρ̄, the three shapes converge.
2. **The pool's σ, not Deribit's.** The simulated position moves with the pool, whose 30 s σ is 0.882× Deribit spot's
   (0.82–0.91 per UTC day).
3. **The pool's burst factor.** The pool's active bin is unchanged in 50.6% of 30 s checks, so its mean absolute move is
   0.739× a Gaussian's of the same variance (0.60–0.81 per day; 0.76–0.81 since 09-28). The hedge model's per-check
   move `s_Δ·√(2/π)` assumes a Gaussian, so it overstates turnover by 1/0.739.

Also found:
- **The hedge band is not the cause.** A band-aware turnover moved the hedge ratio by only 0.01–0.04, because at ρ̄ the
  0.0625 SOL band is about 0.13 of the per-check move.
- **Out-of-range accrual is negligible:** the median in-range share is 100%.
- **The per-day spread is mostly σ forecast error.** With the trailing 24 h σ, the ratio runs low on volatile days and
  high on calm ones. With the realized pool σ and both factors, every UTC day falls within ±50%.

## Decision

1. **Range-dependent LVR.**
   - `projected_lvr_quote = 1e4⁻¹ · LVR_bps_day · V · horizon/day`, with `LVR_bps_day = 1e4·½·σ_pool,d²·ρ̄`.
   - ρ̄ is the life-averaged density of the planned range: the shape's value weights averaged over the occupation
     density of driftless Brownian motion started at the active bin and killed at the range edges. It is computed in
     closed form from the planned bins, the bin step and the shape (`dlmmStrategyType`).
   - `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER` is removed.
2. **A hedge-drag term.**
   - `projected_hedge_drag_quote` uses [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §3.2's turnover with ρ̄ and σ_pool, times the pool's burst factor and the
     taker fee, over the same horizon:
     `turnover ≈ b · s² / max(ε, s_Δ·√(π/2))`, where `b` = `PLACEHOLDER_POOL_BURST_FACTOR`.
   - It is subtracted **inside** `net_ev`, as a carry cost alongside LVR and funding:
     `net_ev = fees − LVR − hedge_drag − funding − rent`.
   - §4's right-hand side is unchanged, for the reason `ev_policy.md` gives for rent: adding to it would be the
     redefinition §6 forbids.
3. **The pool's σ.** Both terms use σ_pool, taken from the per-tick `PlanningSigma` as D5 decides.
4. **Fail closed.** If the planned range, the pool snapshot or σ is unavailable, or the active bin is outside the
   planned range, both terms take the value that refuses, as funding does under [[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]]. They never become zero.
5. **Labelled until ratified.** These stay UNRATIFIED placeholders in `strategy.config.ts`:
   - the taker fee (5 bps);
   - the hedge check interval;
   - `PLACEHOLDER_POOL_SPOT_SIGMA_RATIO` (0.88);
   - `PLACEHOLDER_POOL_BURST_FACTOR` (0.74).

   This ADR ratifies the **structure** and the calibration method, not those constants.

## Decision points for the dispatcher

- **D1 — The model's inputs.**
  - **Recommended:** three measured inputs, none fitted to the simulator:
    - ρ̄ (the closed form above);
    - the pool's σ (D5);
    - the pool's burst factor on hedge turnover.

    Part 0 shows this predicts the simulator to within 2–3% for Curve.
  - **Alternative:** ρ(0) times one factor per term, fitted to the simulator. That is simpler, but it is a fit, and it
    would not follow a change of shape or width.
- **D2 — Tolerance, as two tests.**
  - **Form test (this ADR):** model ÷ simulator using the **realized pool σ**, for the σ-window policies, within ±25% on
    the median for LVR and hedge drag separately, with no UTC day outside ±50%. Part 0 passes it on the whole span and
    per day. Part 0b re-runs it per sub-window at sub-window 2's close.
  - **σ-forecast test ([[adr-047-provisional-sigma-estimator|ADR-047]]'s):** how well the trailing σ predicts the realized σ is [[adr-047-provisional-sigma-estimator|ADR-047]]'s evidence (report §H),
    judged there. A single test that used the forecast σ would fail the model for the estimator's errors.
- **D3 — Regime multipliers ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §5.2).**
  - **Recommended:** ratify with `m_regime = 1` now. Measure the multipliers once 21 days of archive and TICKET T records
    exist (from 2026-10-18), and amend if they differ from 1 beyond their sampling error.
  - **Alternative:** wait for the measurement, which delays this ADR past Route 4's earliest ratification on
    2026-10-21.
- **D4 — Deploy order.**
  - **Recommended:** TICKET 028 ships to the monitors' display and to research first. The root reaches `/production/`
    only through [[adr-035-promotion-workflow|ADR-035]].
  - **Consequence:** on the live window at the placeholder σ, the gate's hurdle rises from 62.5 to about 250 bps/day.
    It will FAIL at §I's measured 80–141 bps/day. That is the intended outcome, not a regression.
- **D5 — The source of the pool's σ (new).**
  - **Recommended for TICKET 028:** σ_pool = `PlanningSigma` × `PLACEHOLDER_POOL_SPOT_SIGMA_RATIO` (0.88, measured by
    Part 0). It needs no new series, and [[adr-047-provisional-sigma-estimator|ADR-047]]'s estimator is unchanged.
  - **Alternative:** a σ estimator on the pool's own price. It is more direct, but it needs an [[adr-047-provisional-sigma-estimator|ADR-047]] amendment and a
    pool-price series in the root, so it would be a follow-up ticket.

## What this does not decide

- **Whether the strategy should change.** A σ×1 window roughly halves both costs (§F), and a wider hedge band or a
  slower check trades less at the cost of delta risk. Those are strategy decisions, for a separate ADR if wanted.
- **The fee value.** That stays [[adr-033-fee-yield-measurement-route|ADR-033]]/050's path, and [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Amendment 1's lock applies until this ships.

## Consequences

- **The gate becomes conservative where it was permissive:** for narrow ranges it refuses unless fees are high.
- **The hurdle panel converges:** `Hurdle(gate)` and `Hurdle(model)` become one number.
- **Capital-dependence enters the gate:** hedge drag grows with `V`, because the band is fixed in SOL.
- **Two pool properties become placeholders to watch.** If the pool's microstructure changes (more arbitrage, a
  different bin step), the σ ratio and the burst factor change with it. Part 0b and later re-runs track them.
- **Every test that pins `net_ev` changes.** TICKET 028 must restate them.

## Alternatives considered

- **Keep the gate and rely on the fee placeholder.** Rejected: [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] D1 retires the placeholder.
- **A separate pre-trade gate on `hurdle_model`.** Rejected: [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §8 says that needs `ev_policy.md` §6 amended, and
  two gates that disagree is worse than one correct one.
- **Put hedge drag on §4's right-hand side.** Rejected: it is a carry cost that scales with time and capital, not an
  execution friction, and §6 forbids redefining the inequality.
- **Fit one factor per term to the simulator (D1's alternative).** Not recommended: the measured inputs already agree,
  and a fit would hide a change in the pool's behaviour instead of showing it.
- **A band-aware turnover.** Tested and dropped: at the live ε it changes the hedge term by under 3%.

## Reversed by

- Live hedge-engine logs showing turnover outside D2's form tolerance of the model;
- Route 3 (real-position) evidence contradicting the calibrated LVR;
- the pool's σ ratio or burst factor moving outside their measured ranges for a full [[adr-033-fee-yield-measurement-route|ADR-033]] sub-window (σ ratio
  0.82–0.91; burst factor 0.60–0.81), which reopens D1;
- a strategy ADR that changes the hedge mechanism.

## Implementation note — 2026-10-01 16:00Z (TICKET 028 Parts 1–6)

**Built:**
- **Blueprints:**
  - `ev_policy.md` §3 (the new field), §3b (the formula, the inputs, the calibration, and the no-plan rule), §4, §6 and
    §7;
  - `config_contract.md` §5;
  - `backtest_research.md` §8 (§F.3);
  - `monitor.md` (the Hurdle panel).
- **Shared math:**
  - `liquidityShape.lifeAveragedDensity` (ρ̄, closed form);
  - `hurdleMath.rangeCostRates`, the single formula for the gate, [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s model and the simulator's §F;
  - `hedgeTurnoverBasePerDay` and `hedgeTakerBpsDay` gain the burst factor.
- **The gate:**
  - `evCalculator.ts`: `placeholderProjectedLvrQuote` is range-dependent, and the new
    `placeholderProjectedHedgeDragQuote` sits inside `net_ev`;
  - `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER` is removed;
  - `projected_hedge_drag_quote` is added to `EvDecisionPayload` and its zod schema.
- **The code and displays that read the gate:**
  - `hurdleRate.ts`: the model uses `rangeCostRates`, and the gate inversion adds hedge drag;
  - `hurdleMain.ts` and `monitor/hurdleView.ts` pass the pool factors;
  - the research simulator uses `rangeCostRates` and takes `SimParams.modelPoolSigma`;
  - new: `research/formTest.ts`, which writes report §F.3.

**Departures and readings recorded here:**
1. **Constant names.** The pool factors are `poolSpotSigmaRatio` (0.88) and `poolBurstFactor` (0.74) in
   `strategy.config.ts`, not `PLACEHOLDER_POOL_*`. `config_contract.md` §5 permits no placeholder values in that file,
   so they follow the [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] form: an ADR-recorded value that is explicitly unratified.
2. **No plan is zero** (Decision 4). By the dispatcher's decision of 2026-10-01, `deployBinRange === null` gives zero
   LVR and hedge drag, as §3a does for rent. Refusing there would withdraw a held position whenever the GEX signal
   was missing, because the macro reducer exits on a failed gate. A plan that exists but cannot be priced still refuses
   (`UNKNOWN_RANGE_COST`). The "σ unavailable" case cannot occur, because σ falls back to the placeholder.
3. **Where the hedge constants live.** The taker fee and check interval moved from `hurdleRate.ts` to `evCalculator.ts`,
   which `hurdleRate.ts` re-exports, so the gate does not import its own display layer.
4. **The regime multiplier is a named constant,** `GATE_REGIME_SIGMA_MULTIPLIER = 1` (D3). `rangeCostRates` takes it as
   an input, so measuring the multipliers will change a value, not the structure.

**Evidence:**
- **Unit tests:** 1145/1145 (+19). New:
  - E60–E65: the no-plan zero; unpriceable refusals; finite sentinels; narrower costs more; gate = model; the live
    window fails at 10, 80 and 141 bps/day;
  - H50–H55: ρ̄ ratios; the σ ratio; the burst factor; narrowing; nulls; model = `rangeCostRates`;
  - F01–F13: the form test.

  Restated: E04 (nine fields), E12, E13, E24 and Z61. Z61's LVR ratio now carries the window's ρ̄ as well as σ².
- **Report §F.3** (`CL_POLICY_REPORT_2026-10-01.md`, regenerated with the shipped code): **PASS**. LVR 0.98 and hedge
  drag 0.98. The judged days were 0.79–1.37 on LVR and 0.75–1.06 on hedge.
- **`npm run hurdle`** on the 2026-10-01 15:58Z live window (50 SOL, placeholder σ):
  - the gate charges LVR 101.19 and hedge drag 88.54 bps/day, identical to the model's to four decimals;
  - the gate hurdle is 234.1 bps/day, against 62.5 before, and 176.4 at σ 1.1e-4;
  - Gate FAIL.

**Not done:**
- Part 0b (re-run at 2026-10-03 14:30Z).
- The browser suite: it stages assets into the running monitors' `dist-monitor-live/`, so it waits for approval.
- The monitors' restart, which needs approval.
- The root's promotion, only through [[adr-035-promotion-workflow|ADR-035]].
- [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Amendment 1 stays in force until that promotion.

## D5 follow-up — 2026-10-01 16:40Z: the pool-price σ estimator is deferred

- **Evidence** (`todo/findings/POOL_SIGMA_FORECAST_2026-10-01.md`): as a forecast of the pool's realized 24 h σ, a
  trailing 24 h σ on the pool's own price scored RMSE 0.210 in ln, against 0.240 for D5's Deribit 24 h × 0.88. That is
  only about 3 independent pairs.
- **Decision (dispatcher):** D5 stays as ratified. The alternative is re-examined when the archive run ends
  (2026-10-18 14:30Z), by re-running `docs/operations/ev_gate_calibration/pool_sigma_forecast.js`. An [[adr-047-provisional-sigma-estimator|ADR-047]]
  amendment is drafted only if the pool σ still wins clearly; the proposed bar is RMSE at least 15% lower, holding
  across the [[adr-033-fee-yield-measurement-route|ADR-033]] sub-windows.
