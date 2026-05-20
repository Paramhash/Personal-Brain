---
tags: ["options trading", "market microstructure", "gamma exposure", "volatility"]
created: 2023-10-27
reviewed: false
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
---
# Gamma Exposure (GEX) Profile

Gamma Exposure (GEX) measures the sensitivity of an option's delta to changes in the underlying asset's price. In simpler terms, it indicates how much the delta of an option will change for a one-point move in the underlying.

A GEX profile typically refers to the aggregate gamma exposure across all outstanding options for a given underlying asset, often visualized across different strike prices and maturities. It provides critical insights into potential market maker hedging activities and their likely impact on future price movements and volatility.

## Interpretation:

*   **Positive GEX:** Suggests that market makers are collectively long gamma. In this scenario, market makers will tend to buy into price dips and sell into price rallies to maintain a delta-neutral position. This hedging behavior can act as a dampening force on volatility, creating "sticky" price levels or ranges.
*   **Negative GEX:** Suggests that market makers are collectively short gamma. Here, market makers will tend to sell into price dips and buy into price rallies. This can exacerbate price movements, leading to increased volatility and potentially accelerating trends or breakdowns.

## Application in the Structural Triad:

In the [[../concepts/structural-triad-systematic-options-trading.md|Structural Triad for Advanced Systematic Options Trading]], the GEX profile helps assess the potential impact of market maker hedging on future price movements and volatility. Understanding these dynamics allows systematic traders to anticipate market behavior, identify potential support/resistance levels, and make tactical adjustments to their options strategies.

## Further Research:

Investigate methodologies for calculating and interpreting aggregate GEX profiles, including considerations for different option types, maturities, and underlying assets. Explore the correlation between GEX levels and subsequent market volatility or directional moves.

---