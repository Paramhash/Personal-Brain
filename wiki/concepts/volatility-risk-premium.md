---
tags: [options trading, volatility, risk premium, quantitative finance, IV, RV]
created: 2023-10-27
reviewed: false
source_origin: "usefulness of hmm for 7DTE to 1DTE options trades.md"
---
The **Volatility Risk Premium (VRP)** is a key concept in options trading, representing the difference between implied volatility (IV) and realized volatility (RV). It is often expressed as $VRP = IV - RV$.

*   **Implied Volatility (IV):** The market's forward-looking expectation of future volatility, derived from options prices.
*   **Realized Volatility (RV):** The historical, actual volatility of an underlying asset over a specific period.

A positive VRP indicates that the market is pricing in higher future volatility than what has been observed historically. This premium exists because options sellers demand compensation for the risk of future price swings.

In the context of [[../concepts/hidden-markov-models-for-options-trading.md|Hidden Markov Models for options trading]], the VRP serves as a critical emission input. When an HMM detects that the gap between forward-looking IV and trailing RV is expanding, especially within a low-volatility market state, it can signal an opportune moment to harvest premium by selling options. This is because the market is overstating the actual expected move, providing a statistical edge for premium sellers.