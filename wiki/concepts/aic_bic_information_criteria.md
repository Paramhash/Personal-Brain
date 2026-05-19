---
tags: ["statistics", "modeling", "model_selection", "econometrics"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# AIC and BIC Information Criteria

## Definition
The [[../concepts/aic_bic_information_criteria.md|Akaike Information Criterion (AIC)]] and [[../concepts/aic_bic_information_criteria.md|Bayesian Information Criterion (BIC)]] are widely used metrics for model selection. They provide a means to compare different statistical models fitted to the same data, balancing the goodness of fit with the complexity of the model. Both criteria penalize models with more parameters to prevent overfitting.

## Akaike Information Criterion (AIC)
*   **Formula:** $AIC = 2k - 2\ln(\hat{L})$
    *   $k$: The number of parameters in the model.
    *   $\hat{L}$: The maximum likelihood estimate for the likelihood function of the model.
*   **Purpose:** AIC estimates the relative amount of information lost by a given model. It aims to select the model that best predicts future data.
*   **Interpretation:** Lower AIC values generally indicate a better model.

## Bayesian Information Criterion (BIC)
*   **Formula:** $BIC = k\ln(n) - 2\ln(\hat{L})$
    *   $k$: The number of parameters in the model.
    *   $n$: The number of observations (sample size).
    *   $\hat{L}$: The maximum likelihood estimate for the likelihood function of the model.
*   **Purpose:** BIC provides a stronger penalty for the number of parameters than AIC, especially for large datasets. It aims to select the true model among the set of candidates.
*   **Interpretation:** Lower BIC values generally indicate a better model.

## Comparison and Use
*   **Penalty for Complexity:** BIC penalizes model complexity more heavily than AIC, particularly when the sample size ($n$) is large. This often leads BIC to select simpler models than AIC.
*   **Asymptotic Properties:** BIC is asymptotically consistent, meaning that with enough data, it will select the true model if it is among the candidate models. AIC is not asymptotically consistent but is efficient in selecting the model that minimizes the mean squared error of prediction.
*   **Application:** In the context of [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]], both AIC and BIC are used to compare the performance of different [[../concepts/regime_switching_models.md|regime switching models]] (e.g., using [[../concepts/horizon_spread_financial.md|horizon spread]], stock returns, or conditional volatility as indicators). The model with the lowest AIC and BIC is considered preferred, indicating a better balance between fit and parsimony.

## Related Concepts
*   [[../concepts/model_selection.md|Model Selection]]
*   [[../concepts/maximum_likelihood_estimation.md|Maximum Likelihood Estimation]]
*   [[../concepts/regime_switching_models.md|Regime Switching Models]]
*   [[../concepts/hidden_markov_model.md|Hidden Markov Model]]

---