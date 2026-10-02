---
domain: cl-market-making
tags:
- volatility-forecasting
- risk-management
- ev-gate
- backtesting
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-calibration-2026-10-01.md
ingest_hashes:
- 4f111967598d52e0
- a8137d764ba043eb
updated: '2026-10-02'
sources:
- dlmm-ev-gate-calibration-2026-10-01.md
- dlmm-pool-sigma-forecast-2026-10-01.md
---
# Sigma forecast error
**In one line:** The discrepancy between a forecasted volatility ($\sigma$) and the volatility that is actually realized over a subsequent period.
## Intuition
Volatility is notoriously difficult to predict accurately. Any quantitative model that relies on a forecast of future volatility, such as those estimating [[loss-versus-rebalancing|LVR]] or [[hedge-drag]] for [[cl-market-making]], will be sensitive to the precision of that forecast. Errors in the volatility forecast will propagate as errors in the model's output, leading to potentially inaccurate cost or profit estimations.
## Mechanism / math
The [[dlmm-2026-ev-gate-calibration|EV gate calibration]] effort demonstrated the impact of [[sigma-forecast-error]] by comparing model performance using a "trailing $\sigma$" (a historical, lagged forecast) versus an "oracle $\sigma$" (the true [[realized-volatility]] over the next 24 hours).
*   When using trailing $\sigma$, the ratio of the model's output to the simulator's output tracked the day's volatility inversely (i.e., the ratio was low on volatile days and high on calm days). This inverse tracking is a clear indicator of [[sigma-forecast-error]].
*   With oracle $\sigma$, this inverse tracking largely disappeared, confirming that the forecast error was a primary driver of the per-day spread in the model's accuracy.
## Where it matters
[[sigma-forecast-error]] directly impacts the day-to-day accuracy and reliability of the [[ev-gate]]'s cost estimations. A significant error can lead to suboptimal decisions regarding liquidity deployment and rebalancing, even if the underlying cost model's form is otherwise correct. For instance, an underestimated $\sigma$ might lead to deploying liquidity into a range that is too narrow for the actual volatility, increasing [[impermanent-loss]].
## Evidence and limits
The source explicitly states that the "per-day spread" in LVR and hedge ratios observed during calibration was "mostly $\sigma$ forecast error, not model error." This finding led to a recommendation to split the [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D2 test into separate evaluations for the model's form and the $\sigma$ estimator's performance (referencing [[adr-047-provisional-sigma-estimator]]). It also highlighted that the [[ev-gate]] must forecast the *pool's* $\sigma$, not just the spot market's, as the spot-based estimator was found to overstate the pool's actual volatility.
## Related
[[ev-gate-calibration]]
[[realized-volatility]]
[[implied-volatility]]
[[volatility-forecasting]]
[[ev-gate]]
[[loss-versus-rebalancing]]
[[hedge-drag]]
[[adr-047-provisional-sigma-estimator]]

## Update from dlmm-pool-sigma-forecast-2026-10-01.md (2026-10-02)

# Sigma Forecast Error
**In one line:** The quantitative difference between a forecasted volatility (sigma) and the actual [[realized-volatility|realized volatility]] over a future period.
## Intuition
Volatility forecasting is inherently challenging. The sigma forecast error measures how accurately a model predicts future price fluctuations, which is crucial for risk management and capital allocation in [[cl-market-making]] strategies. A smaller error indicates a more reliable forecast.
## Mechanism / math
The error is often quantified using metrics such as the mean and [[root-mean-squared-error|RMSE]] of the natural logarithm of the forecast-to-realized ratio.
$$ \text{Mean Error} = \mathbb{E}[\ln(\text{forecast} / \text{realized})] $$
$$ \text{RMSE} = \sqrt{\mathbb{E}[(\ln(\text{forecast} / \text{realized}))^2]} $$
A negative mean error indicates a tendency to underestimate volatility, while a positive one indicates overestimation. RMSE provides a measure of the typical magnitude of the error.
## Where it matters
Accurate volatility forecasts are critical for:
-   Determining optimal [[dlmm-bins]] deployment and range widths in [[concentrated-liquidity|concentrated liquidity]] pools.
-   Managing exposure to [[loss-versus-rebalancing|loss-versus-rebalancing (LVR)]] and minimizing [[hedge-churn-artifact|hedge churn]].
-   Informing the [[ev-gate]] mechanism, which uses volatility forecasts to evaluate the profitability of deploying liquidity.
## Evidence and limits
A comparison between a scaled [[deribit|Deribit]] [[implied-volatility|implied sigma]] and a [[pool-price-sigma|trailing pool price sigma]] showed that the latter had a 12% lower RMSE (0.210 vs 0.240) in forecasting 24-hour realized pool sigma. However, this improvement was not statistically significant due to limited independent data points (approximately 3 independent 24-hour pairs). The majority of the forecast error was attributed to the inherent difficulty of predicting future volatility, rather than the specific source of the forecast.
## Related
[[realized-volatility]]
[[implied-volatility]]
[[pool-price-sigma]]
[[ev-gate]]
[[loss-versus-rebalancing]]
[[hedge-churn-artifact]]
[[dlmm-2026-pool-sigma-forecast]]
