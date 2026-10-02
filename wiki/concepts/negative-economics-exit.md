---
domain: cl-market-making
tags:
- profitability
- exit-strategy
- cost-analysis
- capital-efficiency
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- f0ea87332e2a2395
---
# Negative Economics Exit
**In one line:** A trigger for the [[cl-exit-strategy]] that initiates withdrawal from a [[cl-position]] when the projected fees over the remaining horizon no longer cover the projected [[lvr-and-impermanent-loss|LVR]], funding costs, and exit/redeployment costs.
## Intuition
A [[cl-position]] might not be hitting its price boundaries but could still be economically unprofitable due to high opportunity costs (LVR), funding expenses, or the costs associated with unwinding and redeploying capital. This exit trigger ensures that the bot does not hold onto "zombie" positions that are draining value, even if they appear technically "safe" from a price perspective.
## Mechanism / math
Withdrawal is triggered when:
$$
\text{projected fees over remaining horizon} < \text{projected LVR} + \text{funding} + \text{exit/redeployment costs}
$$
This condition compares the expected future revenue from the position against its total expected future costs, including the opportunity cost of LVR.
## Where it matters
This exit strategy is crucial for maintaining capital efficiency and maximizing overall profitability. It allows the bot to reallocate capital from underperforming positions to potentially more lucrative opportunities, rather than passively holding onto positions that are no longer economically justified. It complements price-based exit triggers by focusing on the financial viability of the position.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] defines this as "Exit trigger B: negative economics," explicitly stating its purpose to prevent the bot from keeping a position open "merely because it has not yet crossed a price boundary." The effectiveness depends on accurate projections of future fees, LVR, and costs.
## Related
[[cl-exit-strategy]]
[[lvr-and-impermanent-loss]]
[[fee-economics]]
[[economic-hurdle-rate-cl]]
[[cl-position]]
[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]