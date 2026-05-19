---
tags: ["statistics", "forecasting", "evaluation_metrics", "econometrics"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# Root Mean Square Forecast Error (RMSFE)

## Definition
The [[../concepts/root_mean_square_forecast_error.md|Root Mean Square Forecast Error]] (RMSFE) is a widely used metric to evaluate the accuracy of forecasts. It measures the average magnitude of the errors between predicted values and observed values. The RMSFE is the square root of the average of the squared differences between forecast values and actual values.

## Formula
The RMSFE is calculated as:
$$	ext{RMSFE} = \sqrt{rac{1}{T}\sum_{t=1}^{T}(Y_t - \hat{Y}_t)^2}$$
Where:
*   $T$: The number of observations in the forecast period.
*   $Y_t$: The actual observed value at time $t$.
*   $\hat{Y}_t$: The forecasted value at time $t$.

## Characteristics
*   **Units:** The RMSFE is expressed in the same units as the forecasted variable, making it easily interpretable.
*   **Sensitivity to Large Errors:** Because errors are squared, the RMSFE gives a relatively high weight to large errors. This means it is particularly useful when large errors are undesirable.
*   **Comparison:** It is commonly used to compare the performance of different forecasting models. A lower RMSFE indicates a more accurate forecast.

## Application in Finance
In financial forecasting, such as predicting the [[../concepts/equity_risk_premium.md|equity risk premium]], RMSFE is a standard metric. For instance, [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]] uses RMSFE to evaluate the out-of-sample forecasting performance of different [[../concepts/regime_switching_models.md|regime switching models]]. The study found that the model incorporating the [[../concepts/horizon_spread_financial.md|horizon spread]] from [[../concepts/option_implied_equity_risk_premium.md|option-implied equity risk premia]] yielded the lowest RMSFE, indicating superior forecasting accuracy.

## Related Concepts
*   [[../concepts/forecasting.md|Forecasting]]
*   [[../concepts/mean_squared_error.md|Mean Squared Error (MSE)]]
*   [[../concepts/equity_risk_premium.md|Equity Risk Premium]]
*   [[../concepts/regime_switching_models.md|Regime Switching Models]]
*   [[../concepts/horizon_spread_financial.md|Horizon Spread (Financial)]]

---