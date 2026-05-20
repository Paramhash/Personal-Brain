---
tags: ["options", "volatility", "market-metrics", "risk-management"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Skew (Options)

Options Skew, often referred to as the "volatility skew" or "volatility smile," describes the phenomenon where implied volatilities for options with the same expiration but different strike prices are not equal. Specifically, it refers to the difference in implied volatility between out-of-the-money (OTM) puts and OTM calls.

A common way to measure skew is the difference between the implied volatility of a 25-delta OTM put and a 25-delta OTM call.

*   **Negative Skew (or "Smirk"):** This is the most common pattern in equity markets, where OTM puts have higher implied volatility than OTM calls. This reflects the market's demand for downside protection and its pricing of "tail risk" (large, sudden drops in the underlying asset).
*   **Positive Skew:** Less common, but can occur in commodities or currencies, where OTM calls have higher implied volatility than OTM puts, reflecting a market expectation of large upward moves.
*   **Flat Skew:** Implied volatilities are relatively similar across strikes.

Skew is a critical feature of the [Implied Volatility Surface (IVS)](../concepts/implied-volatility-surface.md) and provides insights into the market's perception of asymmetric tail risks. In the context of [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), skew is used as an observable feature to help identify underlying market regimes, such as a calm bull market (steep put skew) or indiscriminate selling panic (flat skew).