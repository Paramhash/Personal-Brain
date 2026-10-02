---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-047
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/047-provisional-sigma-estimator.md
bot_commit: ab766fb
source_sha256: 57561bca134ddaef201874723a61b485e020c025f9f561e996510d856d9586be
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/047-provisional-sigma-estimator.md` at commit `ab766fb`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-047-provisional-sigma-estimator|ADR-047]] — A Provisional σ Estimator: Trailing 24 h σ of 300 s Returns, Replacing the 1.4e-4/s Placeholder

- **Date:** 2026-09-30
- **Status:** **Active. Accepted by the dispatcher 2026-09-30**, ahead of the planned 2026-10-18 review, on the evidence
  below (one 3-day sub-window, about 3 independent forecast pairs). The review criteria below become **reversal**
  criteria, checked on 2026-10-18: failing them reverts σ to the placeholder, or to a fixed measured level.
- **Owns:** the σ input to both the [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] width and the EV/hurdle LVR term; `ev_policy.md` §2,
  `range_planner.md` §2b.
- **Touches:** [[adr-033-fee-yield-measurement-route|ADR-033]] (the σ axis of the surface), [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] (σ-derived width), [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] (hurdle LVR and regime
  multipliers).

## Context

**Every live σ is the placeholder today.** `src/index.ts` and `evCalculator.placeholderProjectedLvrQuote` both use
`realizedVol1m_t` when it is set and `PLACEHOLDER_SIGMA_1S_STDDEV = 1.4e-4` otherwise. No producer sets
`realizedVol1m_t`: `liveAdapters.ts` and `hurdleMain.ts` pass `null`. The width and the EV gate therefore agree, but on
an assumed 80% annualised σ.

**The archive now measures σ.** Sub-window 1 of the 21-day run (2026-09-27 14:30Z → 2026-09-30 14:30Z) finished at
97.55% pool / 97.51% spot coverage, above the [[adr-033-fee-yield-measurement-route|ADR-033]] 95% bar. From `sigma_surface.js` at 14:32Z:

| source | σ per second | vs placeholder |
| --- | ---: | ---: |
| 5 s returns | 1.074e-4 | 0.77× |
| 60 s returns | 1.184e-4 | 0.85× |
| 300 s returns | 1.168e-4 | 0.83× |
| per UTC day (5 s), range | 8.9e-5 – 1.17e-4 | 0.63–0.84× |

The variance ratio (60 s: 1.21, 300 s: 1.18 against 5 s) says 5 s returns understate σ through microstructure noise.
300 s is the shortest horizon clear of it, and it is what `research/sigma.ts` already uses.

**A measured level is not a forecast.** The width and LVR need σ over the *next* position life, not the last. The §H
check in `CL_POLICY_REPORT_2026-09-30.md` scores trailing estimators at each hour against σ realized over the next 24 h:

| estimator | pairs | mean ln(forecast/realized) | geometric ratio | RMSE of ln ratio |
| --- | ---: | ---: | ---: | ---: |
| trailing 1 h | 43 | −0.115 | 0.891 | 0.407 |
| trailing 6 h | 43 | −0.006 | 0.994 | 0.331 |
| trailing 24 h | 43 | +0.011 | 1.011 | 0.336 |
| placeholder 1.4e-4 | 43 | +0.223 | 1.249 | 0.279 |

43 hourly pairs over overlapping 24 h windows are **about 3 independent observations**.

## What the evidence says, and does not

1. **The placeholder is biased high by about 25%.** LVR is quadratic in σ, so the gate charges about 56% more LVR than
   the measured σ supports, and the width is about 25% wider than [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] intends.
2. **Trailing 6 h and 24 h are close to unbiased** (within ±1.1% geometric).
3. **The placeholder has the lowest RMSE.** Over three calm days, a constant near the level beats any trailing
   estimate on scatter. That is a statement about this sub-window's stability, not evidence the constant tracks a regime
   change. It cannot, by construction.
4. **1 h is worse on both bias and scatter** and is rejected.
5. **Nothing here separates 6 h from 24 h.** 24 h is preferred for stability: it moves the width less often, and it
   spans one full UTC day, so it does not carry an intraday session pattern into the next day.

## Decision (proposed)

1. **Estimator:** σ per second = standard deviation of non-overlapping 300 s log returns of off-chain spot over the
   trailing 24 h, divided by √300. Same code as `research/sigma.ts` `trailingSigmaPerSecond` (`returnHorizonS 300`),
   moved to a module both the root and research can import.
2. **Coverage rule:** use it only if at least 80% of the 288 return slots are present (the §H `minCoverage`) and no gap
   exceeds 30 minutes.
3. **Fallback chain:** trailing 24 h → trailing 6 h (same coverage rule) → the placeholder 1.4e-4. The frame and the
   decision record carry which link supplied σ.
4. **One σ for both consumers.** It is delivered as `realizedVol1m_t` (to be renamed `sigmaPerSecond_t`), so the width
   and the EV/hurdle LVR keep reading the same number, as `src/index.ts` requires today.
5. **[[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] regime multipliers apply on top**, unchanged and still unratified.
6. **Not a ratification of the placeholder's replacement value.** The placeholder remains the fallback and the
   documented conservative bound.

## Consequences

- At today's σ (≈1.17e-4), LVR in the gate falls from 3.81 to about 2.65 bps/day, and y* with K = 3.57 from 7.38 to
  6.22 bps/day. The deploy width narrows by about 17%.
- **The system becomes less conservative on calm days, and self-adjusts on volatile ones.** The placeholder stops
  covering y* at σ ≈ 1.82e-4 (1.30×). A trailing estimator follows σ past that point; the constant does not.
- The trailing window lags a regime break by hours. The [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] ZGL-proximity multiplier (×1.25 measured, n = 20) is
  the only fast adjustment.

## Review criteria (2026-10-18)

Accept only if, over all seven sub-windows (≥95% coverage):

- trailing 24 h stays within ±10% geometric bias in each sub-window, and
- its RMSE is no more than 0.10 above the placeholder's overall, and it beats the placeholder in any sub-window whose
  realized σ differs from 1.4e-4 by more than 25%.

Otherwise keep the placeholder, and reconsider a level fixed from the measured archive (about 1.2e-4).

## Alternatives considered

- **Keep the placeholder.** Lowest scatter so far, but biased high and blind to a regime change.
- **Fix a new constant at the measured level (≈1.17e-4).** Removes the bias today, keeps the blindness. It is the
  fallback if the review fails.
- **Implied volatility from Deribit.** Already on the wire, forward-looking, but carries a variance risk premium and
  prices a different horizon; it needs its own calibration against realized σ. Deferred.
- **EWMA / GARCH.** More parameters than three days can fit.

## Acceptance note — 2026-09-30

- Accepted by the dispatcher on 2026-09-30, before the review date. The 2026-10-18 check still runs, over all seven
  sub-windows and the live-chain table in research §H. It now decides whether to **keep** the estimator, not whether
  to adopt it.
- **Implementation:**
  - TICKET Z Part A (deployed 2026-09-30) computes, shows and records the chain in both monitors.
  - TICKET Z Part B is now unblocked: the root and the monitors consume σ, with the `STRATEGY_SIGMA_SOURCE` override
    as the kill switch. It reaches `/production/` only through the [[adr-035-promotion-workflow|ADR-035]] promotion path.

## Implementation note — 2026-09-30 (TICKET Z Part B)

- **Deviation from Decision §4, by dispatcher decision 2026-09-30.** σ is **not** delivered through the macro FSM's
  `realizedVol1m_t`.
  - That field also feeds `isStableSnapshot`, which compares it with `redeployRealizedVolCap1m = 0.0035`, a
    1-minute-scaled cap.
  - A per-second σ of about 1.2e-4 would always pass that cap, which would open redeploy streaks that are closed
    today.
  - Instead, the root computes a `PlanningSigma` once per tick and passes it to the planner and to the EV gate's LVR.
    The macro FSM keeps reading `realizedVol1m_t`, which is still `null`.
  - The units of `redeployRealizedVolCap1m` need their own decision before anything feeds that input.
- **Where σ goes.** `TickResult.sigma` and the structured TICK log (`sigma_per_second`, `sigma_source`) carry the σ
  used. The gate, the logged plan and the deploy re-plan in one tick all use it.
- **Kill switch.** `SIGMA_SOURCE=placeholder` ([[adr-026-devnet-tolerance-and-timeout-adjustments|ADR-026]]) reproduces the pre-ADR-047 EV payload and plan byte for byte
  (test Z60), and leaves the macro FSM unchanged (Z62).
- **Frozen feed.** A flat series (σ = 0, which the planner refuses) is treated as no data and falls through the chain.
- **Hurdle CLI.** `--sigma` only. `--sigma-from-archive` was dropped: it would make `src/decision/` import
  `src/backtest/`, against the declared data flow.
- **Not affected.** TICKET T (`dist-recon/`) keeps the placeholder. The root reaches `/production/` only by [[adr-035-promotion-workflow|ADR-035]]
  promotion.
