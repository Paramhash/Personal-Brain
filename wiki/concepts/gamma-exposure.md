---
tags: [options trading, market microstructure, gamma, quantitative finance, GEX, market makers]
created: 2023-10-27
reviewed: false
source_origin: "usefulness of hmm for 7DTE to 1DTE options trades.md"
---
**Gamma Exposure (GEX)**, often referring to total market maker GEX, is a critical derivatives-market variable that reflects the aggregate gamma position of market makers in the options market. Gamma measures the rate of change of an option's delta with respect to a change in the underlying asset's price.

The sign and magnitude of GEX have significant implications for market stability and liquidity:

*   **Positive GEX:** When total market maker GEX is deeply positive, it acts as a stabilizing buffer. Market makers, who are typically short gamma, become long gamma overall. To remain delta-neutral, they must buy the underlying asset when prices fall and sell when prices rise. This hedging behavior dampens volatility, creating a mean-reverting effect.
*   **Negative GEX:** When GEX flips negative, market makers become short gamma overall. To hedge, they must sell the underlying asset when prices fall and buy when prices rise. This behavior exacerbates price movements, leading to violent liquidity vacuums and accelerating trends.

In the context of [[../concepts/hidden-markov-models-for-options-trading.md|Hidden Markov Models for options trading]], GEX is a powerful emission input. An HMM can be trained to detect the exact transition into a negative GEX regime, often *before* the price chart displays any clear directional signals. This early detection allows traders to anticipate potential shifts from stable, mean-reverting environments to explosive, trending ones, which is crucial for managing short-term options positions.