---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/POOL_SIGMA_FORECAST_2026-10-01.md
bot_commit: 574c920
source_sha256: 11e89c335e2a99017a096886bb667a111b17eb0a6195d7d60b50e9e49c35536f
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/POOL_SIGMA_FORECAST_2026-10-01.md` at commit `574c920`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Pool-price σ vs Deribit σ × 0.88 as the gate's forecast — [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D5 follow-up — 2026-10-01

**Verdict: deferred to 2026-10-18 by dispatcher decision.** On this data, a trailing σ on the pool's own price
forecasts the pool's realized σ somewhat better than today's input. The evidence is too thin to justify an [[adr-047-provisional-sigma-estimator|ADR-047]]
amendment and a new σ chain in the root and both monitors.

## Question

[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D5 ratified σ_pool = `PlanningSigma` × `poolSpotSigmaRatio` (0.88), where `PlanningSigma` is the [[adr-047-provisional-sigma-estimator|ADR-047]]
chain over Deribit spot. Its alternative is an estimator on the pool's own price. Which better predicts what LVR and
hedge turnover respond to: the pool's σ realized over the next 24 h?

## Method

- **Script:** `docs/operations/ev_gate_calibration/pool_sigma_forecast.js`, read-only.
- **Data:** the archive plus the soak run, with the pool's active price at the 30 s cadence.
- **Points:** hourly forecast points t, each with at least 80% coverage on both the trailing and the forward window.
- **Target:** the pool's σ realized over [t, t + 24 h].
- **Score:** mean and RMSE of ln(forecast ÷ realized).

## Results (72 hourly points, about 3 independent 24 h pairs)

| estimator (known at t) | mean ln(f/r) | geometric f/r | RMSE ln |
|---|---:|---:|---:|
| A. Deribit 24 h × 0.88 (the gate today) | −0.074 | 0.929 | 0.240 |
| **B. pool 24 h** (D5's alternative) | −0.068 | 0.935 | **0.210** |
| C. pool 6 h | −0.056 | 0.946 | 0.256 |
| D. Deribit 6 h × 0.88 | −0.093 | 0.911 | 0.315 |

## Reading

- **B beats A by about 12% in RMSE** (σ² error roughly 48% → 42%). Both run about 7% low.
- **The overlapping windows mean only about 3 independent pairs,** which cannot separate that gain from noise.
- **Most of the error is the forecast itself,** carrying yesterday's level into today (report §H; TICKET 028 Part 0).
  It is not the choice of source: the fixed ratio adds only about ±5% (0.82–0.91 per UTC day).
- **The cost of switching:**
  - an [[adr-047-provisional-sigma-estimator|ADR-047]] amendment;
  - a pool-price σ chain in the root and in both monitors;
  - tests;
  - another monitor restart, which resets their in-memory σ warm-up.

## Decision and trigger

- **D5 stays as ratified:** σ_pool = `PlanningSigma` × 0.88.
- **Re-run `pool_sigma_forecast.js` when the archive run ends (2026-10-18 14:30Z),** which gives about 18 independent
  pairs.
- **Draft the [[adr-047-provisional-sigma-estimator|ADR-047]] amendment** (a pool-price chain) **only if** B still beats A clearly. Proposed bar: RMSE lower by
  at least 15%, with the gap holding across the seven [[adr-033-fee-yield-measurement-route|ADR-033]] sub-windows.
