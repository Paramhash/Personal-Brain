---
domain: cl-market-making
tags:
- volatility-forecasting
- dlmm
- ev-gate
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-pool-sigma-forecast-2026-10-01.md
ingest_hashes:
- 83c63bfb00f2f447
---
# Pool-Price Sigma
**In one line:** A volatility estimate derived from the historical price movements of a specific concentrated liquidity pool's active price.
## Intuition
Instead of relying on external market [[implied-volatility|implied volatility]] (e.g., from [[deribit|Deribit]] options), [[pool-price-sigma|pool-price sigma]] uses the actual price history observed within the [[dlmm-bins|concentrated liquidity pool]] itself to forecast its future volatility. This approach aims to capture the specific volatility characteristics of the pool's trading environment.
## Mechanism / math
[[pool-price-sigma|Pool-price sigma]] is typically calculated as a [[realized-volatility|trailing realized volatility]] over a specified historical window (e.g., 6 hours or 24 hours) using the pool's active price. The calculation involves standard deviation of logarithmic returns of the pool's price.
## Where it matters
[[pool-price-sigma|Pool-price sigma]] serves as a critical input for [[cl-market-making]] strategies, particularly for:
-   Informing the [[ev-gate]] mechanism, which evaluates the expected value of deploying liquidity.
-   Optimizing the width and placement of [[dlmm-bins]] to balance [[fee-yield]] generation against [[loss-versus-rebalancing|impermanent loss]] and [[hedge-churn-artifact|hedging costs]].
-   Potentially improving the accuracy of [[sigma-forecast-error|volatility forecasts]] specific to the pool's trading dynamics.
## Evidence and limits
An analysis comparing a 24-hour trailing [[pool-price-sigma|pool-price sigma]] against a scaled [[deribit|Deribit]] [[implied-volatility|implied sigma]] found that the [[pool-price-sigma|pool-price sigma]] resulted in a 12% lower [[root-mean-squared-error|RMSE]] when forecasting the pool's future 24-hour [[realized-volatility|realized sigma]]. However, this finding was based on limited data (approximately 3 independent 24-hour pairs), making the improvement statistically inconclusive. The decision to adopt [[pool-price-sigma|pool-price sigma]] as the primary forecast for the [[ev-gate]] (as per [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]) was deferred, pending more extensive data collection.
## Related
[[realized-volatility]]
[[implied-volatility]]
[[sigma-forecast-error]]
[[ev-gate]]
[[dlmm-bins]]
[[loss-versus-rebalancing]]
[[hedge-churn-artifact]]
[[adr-047-provisional-sigma-estimator]]
[[dlmm-2026-pool-sigma-forecast]]