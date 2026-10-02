---
domain: cl-market-making
tags: [curriculum, volatility-forecasting]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 6
status: not-started
prerequisites: []
bot_links: [adr-047-provisional-sigma-estimator, finding-pool-sigma-forecast-2026-10-01, finding-ev-gate-calibration-2026-10-01, cl-policy-report-2026-10-01]
---

# M6 — Volatility estimation and forecasting

Part of [[00-cl-mm-timing-moc|the curriculum]].

## Learning objectives
- Estimate realized volatility from returns at a chosen sampling interval, and test whether the interval matters
  (variance ratio, microstructure noise).
- Forecast tomorrow's volatility (trailing windows, EWMA, GARCH, HAR-RV), and score forecasts with a loss that is
  robust to a noisy proxy.
- Explain why an LP's costs need the **pool's** σ, not the reference market's.

## Concepts to cover
`realized-volatility-estimators`, `har-rv`, `variance-ratio-test`, `microstructure-noise`, `volatility-forecast-evaluation`.

## Existing vault notes to connect
[[realized-volatility]], [[realized-vol-intraday]], [[garch_model]], [[parkinson-volatility-estimator]],
[[volatility-clustering]], [[stochastic_volatility_models]].

## Where it shows up in the bot
- The σ the bot plans and prices with: a trailing 24 h → 6 h → placeholder chain over Deribit spot,
  [[adr-047-provisional-sigma-estimator|ADR-047]].
- The pool's σ is 0.88× Deribit's at 30 s, and its moves are bursty:
  [[finding-ev-gate-calibration-2026-10-01|EV gate calibration]].
- Does a pool-price estimator forecast better? Not yet shown on about 3 independent pairs:
  [[finding-pool-sigma-forecast-2026-10-01|pool σ forecast]].
- Forecast skill, scored daily: [[cl-policy-report-2026-10-01|CL policy report]] §H.

## Self-test
> [!question]- LVR is proportional to σ². If the forecast σ is 10% too high, how wrong is the LVR cost?
> About 21% too high: $1.1^2 = 1.21$. Volatility errors are amplified in the cost.

> [!question]- Why did the bot's model-to-simulator ratio run high on calm days and low on volatile days?
> The trailing 24 h σ carries yesterday's volatility into today. After a volatile day it overstates a calm day's σ (the ratio runs high); after a calm day it understates a volatile one (the ratio runs low).

> [!question]- Why compute the pool's own σ rather than use Deribit's for an LP's costs?
> The LP's loss and inventory moves follow the pool's price path. That path moved only 0.88× as much as Deribit spot at the 30 s cadence, because the pool lags and moves in bursts.

## Open questions
- (Add questions here after a quiz.)
