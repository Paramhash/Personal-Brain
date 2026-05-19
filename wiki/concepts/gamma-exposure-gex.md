yaml
---
tags: ["GEX", "gamma-exposure", "microstructure", "option-greeks", "market-indicators"]
created: 2023-10-27
reviewed: false
source_origin: "maopm_horizon_spread_blueprint.md"
---
```
# Gamma Exposure (GEX)

**Gamma Exposure (GEX)** is a high-frequency microstructure indicator that quantifies the sensitivity of market makers' delta hedging requirements to changes in the underlying asset's price. It reflects the aggregate gamma position of market participants, particularly dealers, and can be used to predict immediate localized price acceleration or pinning effects.

A high positive GEX suggests that market makers are collectively long gamma, meaning they will buy into falling prices and sell into rising prices to maintain a delta-neutral position. This tends to dampen volatility and "pin" prices. Conversely, a negative GEX indicates market makers are short gamma, leading them to sell into falling prices and buy into rising prices, which can exacerbate price movements and increase volatility.

In the context of a [Multi-Agent Option Pricing & Market-Making (MAOPM)](../concepts/multi-agent-option-pricing-market-making-maopm.md) architecture, [GEX](../concepts/maopm-architecture-horizon-spread-gex-fusion.md) Z-scores are utilized by Microstructure Execution Agents to map local dealer positioning and manage intra-day liquidity provisioning, order-book profiling, and inventory rebalancing. It complements macro signals like the [Option-Implied Horizon Spread](../concepts/option-implied-horizon-spread.md) by providing real-time insights into immediate market dynamics.

---