---
tags: ["options", "volatility", "market-data", "pricing"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Implied Volatility Surface (IVS)

The Implied Volatility Surface (IVS) is a three-dimensional plot that shows the implied volatility of an option as a function of its strike price and time to expiration. It is derived by inverting an option pricing model (like [Black-Scholes Model](../concepts/black-scholes-model.md)) using actual market prices.

Key characteristics of the IVS include:

*   **Volatility Smile/Skew:** For a given expiration, implied volatility often varies across strike prices, forming a "smile" or "skew." This phenomenon contradicts the constant volatility assumption of the Black-Scholes model and reflects market expectations of future price movements and tail risks.
    *   [ATM Volatility](../concepts/atm-volatility.md)
    *   [Skew (Options)](../concepts/options-skew.md)
    *   [Smile Curvature](../concepts/smile-curvature.md)
*   **Term Structure of Volatility:** For a given strike (e.g., ATM), implied volatility varies across different expirations, reflecting how market expectations of future volatility change over time.

The IVS is a rich source of information about market sentiment and expectations. In the context of [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), features extracted from the IVS (such as ATM Volatility, Skew, and Smile Curvature) can serve as observable inputs for a [Hidden Markov Model (HMM)](../concepts/hidden-markov-model.md) to infer underlying market regimes.