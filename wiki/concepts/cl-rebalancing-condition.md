---
domain: cl-market-making
tags:
- hedging
- inventory-control
- decision-making
- transaction-costs
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- deffe49b596e15bf
---
# CL Rebalancing Condition
**In one line:** The specific criteria that trigger an adjustment to the bot's hedging position or its concentrated liquidity range, aimed at maintaining the desired risk profile and capital efficiency.
## Intuition
Continuous market fluctuations can cause the bot's actual hedge position to deviate from its [[cl-hedge-target]], or its liquidity range to become suboptimal. Rebalancing is necessary to correct these deviations, but it incurs [[transaction_costs_in_options|transaction costs]]. Therefore, rebalancing should only occur when the deviation is significant enough to warrant the cost.
## Mechanism / math
The bot should rebalance when:
$$
|q_t^* - q_t| > \epsilon_{base}
$$
where $q_t^*$ is the [[cl-hedge-target]], $q_t$ is the current hedge position, and $\epsilon_{base}$ is a predefined threshold. This condition must also be met while collateral remains sufficient.
The source notes this execution logic is defined in `binanceHedge.ts:60`.
## Where it matters
This condition optimizes the trade-off between maintaining a precise hedge/liquidity profile and minimizing [[transaction_costs_in_options|transaction costs]]. It prevents excessive, costly rebalances due to minor market noise while ensuring that the bot's risk exposure remains within acceptable limits. It is a key part of the [[cl-position-monitoring]] and active management phase.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly states this condition, emphasizing that the bot "should not rebalance simply because price moves" but rather when the deviation from the target exceeds a defined epsilon. This highlights the importance of a cost-benefit analysis for rebalancing actions.
## Related
[[cl-hedge-target]]
[[cl-position-monitoring]]
[[transaction_costs_in_options]]
[[hedging-lp-exposure]]
[[blueprint-hedge-engine]]