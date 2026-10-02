---
domain: cl-market-making
tags:
- simulation
- hedge-drag
- inventory-control
- backtesting
- performance-metrics
- hedging
- transaction-costs
- slippage
- rebalancing
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
ingest_hashes:
- 5d6bd817dec8e13e
- 51ea99c845085a3c
updated: '2026-10-02'
sources:
- dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
- dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
---
# Hedge Churn Artifact
**In one line:** An inflated measure of simulated [[hedge-churn]] that arises when a simulation incorrectly aggregates inventory changes due to range repositioning with those due to continuous hedging within a stable range.
## Intuition
In [[cl-market-making]], a liquidity provider's inventory changes for two main reasons: continuous rebalancing (hedging) as price moves within a fixed range, and discrete repositioning events when the entire liquidity range is adjusted or moved. If a simulation sums these distinct types of inventory changes, it can significantly overestimate the true cost of hedging.
## Mechanism / math
The artifact occurs when a simulation's `simulatedBaseInventory` metric (or similar) does not differentiate between:
1.  **Within-bounds drift:** Inventory changes resulting from price movements and subsequent hedging *within an unchanged liquidity range*.
2.  **Bounds-change jumps:** Instantaneous inventory adjustments that occur when the deployed liquidity range is withdrawn and redeployed at new bounds.
If these two components are summed, the "bounds-change jumps" (which are operational costs, not continuous hedging costs) disproportionately inflate the reported [[hedge-churn]].
## Where it matters
This artifact distorts the true [[hedge-drag]] and overall cost of a [[cl-provider-strategy]] in [[dlmm-simulator|simulations]] and [[backtesting]]. An overestimated churn figure can lead to:
*   Incorrect evaluation of strategy profitability.
*   Misguided optimization efforts (e.g., focusing on reducing "hedging" when the real problem is range stability).
*   Unjustified condemnation of a strategy based on misleading performance metrics.
## Evidence and limits
The `[[dlmm-2026-call-wall-oscillates]]` finding revealed that 95.2% of the apparent [[hedge-churn]] in a 11.13-hour simulation run was due to [[call-wall-oscillation]] causing frequent range repositioning, not continuous hedging. The "bounds-change jumps" accounted for 639.70 SOL turnover (201% of position/year), while "within-bounds drift" was only 32.05 SOL (10% of position/year). This highlights the critical need for [[dlmm-simulator|simulations]] to have a proper [[cl-rebalancing-condition|reposition model]] that separates these costs.
## Related
[[hedge-churn]], [[hedge-drag]], [[simulated-base-inventory]], [[dlmm-simulator]], [[inventory-accounting]], [[cl-position]], [[call-wall-oscillation]]

## Update from dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md (2026-10-02)

# Hedge Churn Artifact
**In one line:** An undesirable side effect of frequent or excessive rebalancing of a concentrated liquidity position, leading to increased transaction costs, [[slippage]], and potential [[hedge-drag]] that erodes profitability.
## Intuition
When a concentrated liquidity position's inventory shifts due to price movements, a market maker often needs to rebalance their external hedge to maintain a desired [[cl-hedge-target|hedge target]]. If the liquidity range is too narrow, or if price volatility is high, these inventory shifts can be frequent and large, leading to many small or large hedge trades. Each hedge trade incurs [[transaction-costs|transaction costs]] (fees, [[slippage]]), and the cumulative effect of these costs is "hedge churn." It's an artifact because it's a cost that doesn't directly contribute to profit but is a necessary evil of maintaining a hedged position.
## Mechanism / math
Hedge churn is primarily driven by:
1.  **Frequency of Rebalancing:** How often the LP's inventory crosses a threshold that triggers a hedge adjustment.
2.  **Magnitude of Rebalancing:** The size of the hedge trades required.
3.  **Transaction Costs:** The fees and [[slippage]] incurred per trade.

A narrower [[sigma-derived-deployed-window|deployed liquidity window]] means that for the same price path, the LP's inventory will traverse its full base-to-quote range faster. This leads to proportionally harder swings in the [[simulated-base-inventory]], triggering more frequent or larger hedge adjustments.

**Impact of Range Width:**
The relationship between deployed range width and hedge churn is inverse. A narrower range implies that a given price movement will cause a larger proportional change in the LP's inventory, necessitating more aggressive or frequent hedging.

**Measurement Inaccuracy:**
[[dlmm-2026-planner-deploys-wall-envelope|F-022]] revealed that previous [[hedge-churn-artifact|hedge churn]] measurements were significantly understated (by a factor of ~4.64x) because the [[range-planning|planner]] was deploying the full [[wall-envelope]] instead of the narrower [[sigma-derived-deployed-window]]. This meant the [[simulated-base-inventory]] model assumed a wider position, leading to lower simulated inventory swings for the same price path. Consequently, the "honest expectation is therefore that real hedge churn is higher than measured, not lower."
## Where it matters
*   **Profitability:** High hedge churn can significantly erode the [[fee-yield]] earned by a concentrated liquidity position, potentially turning a profitable strategy into a losing one.
*   **Strategy Optimization:** Understanding and minimizing hedge churn is crucial for optimizing [[cl-provider-strategy|CL provider strategies]], particularly in determining optimal [[range-planning|range widths]] and rebalancing thresholds.
*   **Risk Management:** Excessive churn can indicate a miscalibrated strategy or an environment where the costs of hedging outweigh the benefits of maintaining a hedged position.
## Evidence and limits
[[dlmm-2026-planner-deploys-wall-envelope|F-022]] provided direct evidence of how an incorrect assumption about deployed range width (deploying the [[wall-envelope]] instead of the [[sigma-derived-deployed-window]]) led to a material understatement of hedge churn. The finding estimated that earlier churn figures understated inventory sensitivity by about 4.64x. This highlights the importance of accurate [[range-planning]] and the direct link between liquidity concentration and hedging costs.
## Related
[[cl-hedge-target]]
[[hedge-drag]]
[[transaction-costs]]
[[slippage]]
[[rebalancing-strategy]]
[[range-planning]]
[[sigma-derived-deployed-window]]
[[wall-envelope]]
[[simulated-base-inventory]]
[[dlmm-2026-planner-deploys-wall-envelope]]

---
