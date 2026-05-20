---
tags: ["options", "volatility", "market-metrics"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Smile Curvature

Smile Curvature, in the context of options, refers to the convexity of the [Implied Volatility Surface (IVS)](../concepts/implied-volatility-surface.md) across different strike prices for a given expiration. It measures how pronounced the "smile" shape is, specifically how much higher the implied volatilities of out-of-the-money (OTM) options are compared to at-the-money (ATM) options.

It can be quantified as the average of OTM Put and Call IVs minus the [ATM Volatility](../concepts/atm-volatility.md).

*   **High Curvature:** Indicates that OTM options (both puts and calls) have significantly higher implied volatilities than ATM options. This suggests the market is pricing in a higher probability of extreme price movements (fat tails or "jump risk") in either direction, implying higher expected kurtosis in the underlying asset's return distribution.
*   **Low Curvature:** Implies that implied volatilities are relatively flat across strikes, suggesting less expectation of extreme moves.

Smile Curvature is a crucial feature for characterizing market regimes. As discussed in [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), it is extracted alongside [ATM Volatility](../concepts/atm-volatility.md) and [Skew (Options)](../concepts/options-skew.md) to serve as an observable input for [Hidden Markov Models](../concepts/hidden-markov-model.md), helping to identify periods of heightened or subdued jump risk.