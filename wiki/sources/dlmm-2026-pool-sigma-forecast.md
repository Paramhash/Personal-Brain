---
domain: cl-market-making
tags:
- dlmm
- volatility-forecasting
- ev-gate
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-pool-sigma-forecast-2026-10-01.md
ingest_hashes:
- b30330ad66a0d1c1
---
# Pool-price σ vs Deribit σ × 0.88 as the gate's forecast (DLMM, 2026)
**Type:** article
## Claim
This internal finding evaluates whether a trailing [[pool-price-sigma|sigma]] derived from a concentrated liquidity pool's own active price is a better forecast for its future 24-hour [[realized-volatility|realized sigma]] than the current method, which uses [[deribit|Deribit]] spot [[implied-volatility|sigma]] scaled by 0.88. While the pool's own sigma shows a slightly lower [[sigma-forecast-error|RMSE]], the evidence is insufficient to justify an immediate change due to limited independent data.
## Method and data
The analysis used a read-only script (`docs/operations/ev_gate_calibration/pool_sigma_forecast.js`) on an archive of pool data, including the pool's active price at a 30-second cadence. Hourly forecast points were generated, requiring at least 80% coverage on both trailing and forward windows. The target was the pool's [[realized-volatility|realized sigma]] over the subsequent 24 hours. Forecast accuracy was scored using the mean and [[root-mean-squared-error|RMSE]] of the natural logarithm of the forecast-to-realized ratio ($$\ln(\text{forecast} / \text{realized})$$).
## Key results
Based on 72 hourly points (approximately 3 independent 24-hour pairs):
-   **Deribit 24h × 0.88 (current method):** Mean $$\ln(f/r)$$ = -0.074, geometric f/r = 0.929, RMSE $$\ln$$ = 0.240.
-   **Pool 24h (alternative):** Mean $$\ln(f/r)$$ = -0.068, geometric f/r = 0.935, RMSE $$\ln$$ = **0.210**.
-   The pool's 24h trailing sigma (B) showed about a 12% improvement in RMSE over the scaled Deribit sigma (A), reducing the squared error from approximately 48% to 42%. Both estimators consistently underestimated realized sigma by about 7%.
-   The majority of the forecast error stems from the inherent challenge of predicting future volatility (carrying yesterday's level into today), rather than the choice of volatility source.
## Assumptions and limits
The primary limitation is the small number of independent data points (approximately 3 independent 24-hour pairs), which means the observed improvement in RMSE for the pool's own sigma is not statistically significant and could be due to noise. The decision to switch was deferred, pending more data (approximately 18 independent pairs) from a longer archive run.
## Concepts introduced or used
[[sigma-forecast-error]]
[[pool-price-sigma]]
[[realized-volatility]]
[[implied-volatility]]
[[ev-gate]]
[[dlmm-bins]]
[[loss-versus-rebalancing]]
[[hedge-churn-artifact]]
[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]
[[adr-047-provisional-sigma-estimator]]
[[adr-033-fee-yield-measurement-route]]
[[deribit]]