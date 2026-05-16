---
tags: [trading, options, volatility, arbitrage, gex]
created: 2023-10-27
reviewed: false
source_origin: "Strategies to benefit from divergences between the GEX profiles of individual stocks in the S&P500 and the index..md"
---
# The Dispersion Trade Strategy

The Dispersion Trade is a [[../concepts/gex-divergence-strategies.md|GEX Divergence Strategy]] that capitalizes on a **Dispersion Regime**, a market state where index-level gamma is positive (suppressing index volatility) but individual stock gamma is deeply negative (leading to exploding component-level volatility). This strategy is a form of "volatility arbitrage."

## The Divergence

*   **Index-Level Gamma:** Positive, leading to suppressed volatility and range-bound movement for the [[../entities/sp500-index.md|S&P 500 Index]].
*   **Component-Level Gamma:** Deeply negative for many individual stocks, causing their volatility to explode and leading to violent movements.

This divergence indicates a breakdown in correlation, where the index appears calm, but its underlying components are moving wildly and independently.

## The Strategy

1.  **Sell Straddles on the S&P 500:** This position profits if the [[../entities/sp500-index.md|S&P 500]] remains relatively range-bound, benefiting from the suppressed index volatility and time decay.
2.  **Buy Straddles on High-Divergence Stocks:** Use the premium generated from selling index straddles to buy straddles on individual stocks that show the greatest negative gamma divergence. This position profits if these individual stocks experience large movements in either direction.

## The Benefit

You profit if the [[../entities/sp500-index.md|S&P 500 Index]] stays flat or moves within a narrow range, while individual stocks move violently in opposite directions. This strategy effectively arbitrages the difference between implied volatility at the index level and the aggregate implied volatility of its components, benefiting from a breakdown in correlation. It is a favorite of institutional quant desks due to its sophisticated approach to volatility.

## Dispersion Regime

A **Dispersion Regime** is a market environment characterized by low index volatility but high individual stock volatility. This often occurs when market participants are hedging at the index level (e.g., via ETFs), which suppresses index-level gamma, while individual stock-specific news or fundamental shifts cause significant movements in their respective GEX profiles.

## Related Concepts

*   [[../concepts/gex-divergence-strategies.md|GEX Divergence Strategies]]
*   [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]]
*   [[../entities/sp500-index.md|S&P 500 Index]]

---