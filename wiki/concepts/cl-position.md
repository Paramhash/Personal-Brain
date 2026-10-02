---
domain: cl-market-making
tags:
- concentrated-liquidity
- lp-strategy
- inventory-management
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 0558fdc593f8bdd2
---
# CL Position
**In one line:** A temporary deployment of surplus [[sol-inventory]] and [[usdc-inventory]] into a concentrated liquidity pool, managed actively to earn fees while mitigating risks.
## Intuition
A [[cl-position]] is the primary mechanism for a market-making bot to generate yield in a concentrated liquidity Automated Market Maker (AMM). Instead of providing liquidity across the entire price range, capital is concentrated within a specific, narrower range, aiming to capture more fees for the deployed capital. However, this concentration also increases exposure to [[impermanent-loss]] and requires active management.
## Mechanism / math
A [[cl-position]] is defined by its [[market-boundaries-cl]] (lower and upper price limits) and the specific [[sigma-derived-deployed-window]] where liquidity is actually placed. It is subject to:
*   **Entry:** Governed by the [[cl-entry-strategy]], ensuring reserves are safe and economic conditions are met.
*   **Monitoring:** Continuously tracked via [[cl-position-monitoring]] for price, volatility, GEX, fees, and hedge error.
*   **Hedging:** The [[sol-inventory]] component is typically hedged using a [[cl-hedge-target]] of `q_t^* = -x_t`.
*   **Rebalancing:** Triggered by the [[cl-rebalancing-condition]] when hedge deviation exceeds a threshold.
*   **Exit:** Initiated by the [[cl-exit-strategy]] based on boundary threats, negative economics, or [[regime-deterioration-exit]].
## Where it matters
The [[cl-position]] is the core profit-generating component of the bot. Its effective management is crucial for the bot's profitability and risk control. Decisions regarding range width, entry timing, rebalancing frequency, and exit triggers directly impact the fees earned, the realized [[impermanent-loss]], and the overall equity of the bot.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] treats the [[cl-position]] as a "temporary deployment of surplus inventory to earn fees." It acknowledges that such a position changes the composition of inventory as price moves, necessitating careful management and reconciliation. The strategy aims to ensure that the expected fee edge justifies the inherent risks.
## Related
[[concentrated-liquidity]]
[[cl-market-making]]
[[lvr-and-impermanent-loss]]
[[fee-economics]]
[[m02-concentrated-liquidity-math]]
[[m03-bin-based-cl-dlmm]]
[[blueprint-liquidity-position-manager]]