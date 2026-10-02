---
domain: cl-market-making
tags:
- simulation
- inventory-control
- backtesting
- performance-metrics
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
ingest_hashes:
- d56ac36da892d0ff
---
# Simulated Base Inventory
**In one line:** A metric used in [[dlmm-simulator|simulations]] and [[backtesting]] to track the theoretical base asset inventory of a [[cl-position|concentrated liquidity position]], primarily for estimating [[hedge-drag]] and [[hedge-churn]].
## Intuition
In a simulated environment, a [[cl-market-making|concentrated liquidity market maker]]'s holdings of the base asset (e.g., SOL in a SOL/USDC pool) fluctuate as price moves and liquidity is rebalanced or repositioned. Tracking this simulated inventory is essential for understanding the strategy's exposure and the costs associated with managing that exposure.
## Mechanism / math
The `simulatedBaseInventory` metric quantifies the theoretical amount of the base asset held by the LP within the simulated liquidity range. It changes due to:
1.  **Price Drift:** As the market price moves within the deployed range, the proportion of base and quote assets in the liquidity position changes.
2.  **Range Repositioning:** When the entire liquidity range is withdrawn and redeployed at new bounds, the simulated inventory is re-marked to reflect the new theoretical holdings.
A key distinction, highlighted by the source, is that if a simulation sums inventory changes from both within-bounds price drift and discrete bounds-change jumps, it can lead to an inflated [[hedge-churn-artifact]].
## Where it matters
Accurate tracking of [[simulated-base-inventory]] is critical for:
*   **Performance Evaluation:** Correctly assessing the [[hedge-drag]] and [[hedge-churn]] of a [[cl-provider-strategy]].
*   **Risk Management:** Understanding the theoretical [[inventory-accounting|inventory]] exposure over time.
*   **Strategy Optimization:** Identifying whether high turnover is due to frequent hedging or costly repositioning.
## Evidence and limits
The `[[dlmm-2026-call-wall-oscillates]]` finding demonstrated that a significant portion (95.2%) of apparent [[hedge-churn]] in a simulation was an artifact of how `simulatedBaseInventory` was calculated. The simulation treated range repositioning (due to [[call-wall-oscillation]]) as instantaneous inventory jumps, summing them with continuous hedging. This led to a simulated annual turnover of 212% of position value, whereas the actual "within-bounds drift" was only ~10%. This underscores the importance of a [[dlmm-simulator|simulation]] having a robust [[cl-rebalancing-condition|reposition model]] to avoid misrepresenting strategy costs.
## Related
[[hedge-churn]], [[hedge-drag]], [[dlmm-simulator]], [[inventory-accounting]], [[cl-position]], [[call-wall-oscillation]], [[hedge-churn-artifact]], [[backtesting]]