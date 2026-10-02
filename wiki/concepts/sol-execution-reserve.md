---
domain: cl-market-making
tags:
- solana
- operational-risk
- capital-management
- transaction-costs
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- d92e672edd34ff64
---
# SOL Execution Reserve
**In one line:** A dedicated portion of a Solana-based market-making bot's [[sol-inventory]] reserved for covering transaction fees (gas) and other operational costs on the blockchain.
## Intuition
Executing transactions on a blockchain, such as deploying liquidity, rebalancing positions, or adjusting hedges, incurs gas fees paid in the native token (SOL). These fees can fluctuate with network activity. The [[sol-execution-reserve]] ensures the bot can always afford to execute necessary operations, even during periods of high [[network-congestion]] or unexpected market events, preventing operational paralysis.
## Mechanism / math
Similar to the [[sol-rent-reserve]], the [[sol-execution-reserve]] is subtracted from the total [[sol-inventory]] (`SOL_wallet`) to determine the `SOL_free` amount available for deployment:
$$
SOL_{free} = SOL_{wallet} - SOL_{rent\ reserve} - SOL_{execution\ reserve}
$$
This reserve is considered "untouched" and is a hard constraint for the [[cl-entry-strategy]].
## Where it matters
This reserve is vital for the bot's ability to react to market conditions and manage its positions dynamically. Without it, the bot might be unable to rebalance, withdraw, or adjust hedges, leading to increased [[impermanent-loss]] or other risks. It directly impacts the bot's responsiveness and overall risk management.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly lists the preservation of the "Rent and execution reserves" as a prerequisite for entering a position, underscoring its importance for operational continuity. The strategy also includes "gas" as a cost in the [[economic-hurdle-rate-cl]].
## Related
[[sol-inventory]]
[[sol-rent-reserve]]
[[cl-entry-strategy]]
[[cl-closing-procedure]]
[[cl-success-metrics]]
[[transaction-latency]]
[[network-congestion]]