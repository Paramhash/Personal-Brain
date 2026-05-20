---
tags: ["options", "pricing-models", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Black-Scholes Model

The Black-Scholes Model (or Black-Scholes-Merton model) is a mathematical model for the pricing of European-style options. Developed by Fischer Black, Myron Scholes, and Robert Merton, it is one of the most fundamental concepts in modern financial theory.

The model makes several key assumptions:
*   The underlying asset follows a [Geometric Brownian Motion](../concepts/geometric-brownian-motion.md) with constant drift and volatility.
*   The risk-free interest rate is constant.
*   There are no dividends paid during the option's life.
*   There are no transaction costs or taxes.
*   Options can only be exercised at expiration (European style).

The Black-Scholes formula calculates the theoretical price of an option by considering:
*   The current price of the underlying asset.
*   The option's strike price.
*   The time to expiration.
*   The risk-free interest rate.
*   The volatility of the underlying asset.

While highly influential, its assumption of constant volatility is often violated in real markets, leading to phenomena like the [Implied Volatility Surface (IVS)](../concepts/implied-volatility-surface.md) and the development of more complex models like the [Regime-Switching Option Pricing Model](../concepts/regime-switching-option-pricing-model.md) to better capture market dynamics, as discussed in [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md).