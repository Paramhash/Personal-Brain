---
tags: ["statistics", "metrics", "machine-learning", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Root Mean Squared Error (RMSE)

Root Mean Squared Error (RMSE) is a frequently used measure of the differences between values predicted by a model or an estimator and the values observed. It is the square root of the mean of the squared errors.

The formula for RMSE is:
$$RMSE = \sqrt{\frac{1}{N} \sum_{i=1}^{N} (y_i - \hat{y}_i)^2}$$
Where:
*   $N$ is the number of observations.
*   $y_i$ is the observed value.
*   $\hat{y}_i$ is the predicted value.

Key characteristics of RMSE:
*   **Units:** RMSE has the same units as the dependent variable, making it easily interpretable.
*   **Sensitivity to Large Errors:** Because errors are squared before they are averaged, RMSE gives a relatively high weight to large errors. This means it is particularly useful when large errors are undesirable.
*   **Common Use:** Widely used in regression analysis, forecasting, and model calibration.

In quantitative finance, RMSE is a standard metric for evaluating the goodness-of-fit of pricing models. For instance, when calibrating a [Regime-Switching Option Pricing Model](../concepts/regime-switching-option-pricing-model.md) to market data, as described in [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), the objective function often involves minimizing the RMSE between the model's theoretical option prices and the actual market option prices. This helps ensure the model accurately reflects current market conditions.