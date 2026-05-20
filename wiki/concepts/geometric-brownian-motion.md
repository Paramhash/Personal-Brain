---
tags: ["stochastic-processes", "quantitative-finance", "modeling"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Geometric Brownian Motion (GBM)

Geometric Brownian Motion (GBM) is a continuous-time stochastic process in which the logarithm of the randomly varying quantity follows a Brownian motion (also known as a Wiener process). It is widely used in mathematical finance to model the price movements of financial assets, particularly stocks, because it ensures that prices remain positive and that returns are normally distributed.

The stochastic differential equation for GBM is typically given by:
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$
Where:
*   $S_t$ is the asset price at time $t$.
*   $\mu$ is the drift coefficient (expected return).
*   $\sigma$ is the volatility coefficient.
*   $dW_t$ is a Wiener process (standard Brownian motion).

Key characteristics of GBM:
*   **Positive Prices:** Asset prices modeled by GBM will always be positive.
*   **Log-Normal Distribution:** The asset price at any future time $t$ follows a log-normal distribution.
*   **Constant Volatility:** In its basic form, GBM assumes constant volatility, which is a simplification often relaxed in more advanced models.

GBM is a foundational component of many option pricing models, including the [Black-Scholes Model](../concepts/black-scholes-model.md). It is also used as the underlying asset movement model within each regime in a [Regime-Switching Option Pricing Model](../concepts/regime-switching-option-pricing-model.md), as mentioned in the context of [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md).