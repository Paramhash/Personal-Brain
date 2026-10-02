---
domain: cl-market-making
tags:
- profitability
- cost-analysis
- risk-management
- decision-making
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 52bdb92ddd5403ef
---
# Economic Hurdle Rate CL
**In one line:** The minimum expected fee income required for a [[cl-position]] to be deployed, ensuring that all associated costs and a [[risk-premium]] are covered.
## Intuition
Not every opportunity to deploy liquidity is profitable after accounting for all costs. The [[economic-hurdle-rate-cl]] acts as a financial filter, ensuring that the bot only engages in market-making activities that are genuinely expected to add value to its equity, considering both explicit and implicit costs.
## Mechanism / math
The entry condition for a [[cl-position]] is that expected fees must exceed this hurdle rate:
$$
\text{Expected fees} > \text{LVR} + \text{hedge funding} + \text{rent} + \text{gas} + \text{slippage} + \text{risk premium}
$$
The components of the hurdle rate include:
*   [[lvr-and-impermanent-loss|LVR]]: Loss-Versus-Rebalancing, an opportunity cost.
*   Hedge funding: Costs associated with maintaining hedging positions (e.g., perpetual futures funding rates).
*   Rent: Solana account rent (covered by [[sol-rent-reserve]]).
*   Gas: Solana transaction fees (covered by [[sol-execution-reserve]]).
*   [[slippage]]: Cost incurred during trade execution.
*   [[risk-premium]]: Compensation for the inherent risks of the position.
## Where it matters
This hurdle rate is a critical component of the [[cl-entry-strategy]] and serves as a [[decision-gate-cl-bot]]. By incorporating a comprehensive set of costs, it ensures that capital is allocated efficiently and only to positions with a positive expected value, contributing to the bot's overall profitability and sustainability.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly defines this hurdle model as the entry condition, referencing `hurdleRate.ts:120` in the repository. This indicates its direct implementation in the bot's logic. The accuracy of the hurdle rate depends on reliable estimations of its various components, especially projected LVR and expected fees.
## Related
[[cl-entry-strategy]]
[[lvr-and-impermanent-loss]]
[[fee-economics]]
[[risk-premium]]
[[slippage]]
[[sol-rent-reserve]]
[[sol-execution-reserve]]
[[adr-031-funding-drag-numeraire-and-unknown-cost-policy]]
[[adr-046-real-time-hurdle-rate-restates-the-ev-gate]]
[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]