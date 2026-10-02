---
domain: cl-market-making
tags:
- transaction-costs
- market-microstructure
- execution-risk
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- cd2c982f0cc4e3a2
---
# Slippage
**In one line:** The difference between the expected price of a trade and the actual price at which the trade is executed.
## Intuition
In fast-moving markets or when executing large orders, the price can change between the time an order is placed and when it is filled. This difference, or slippage, represents an additional, often hidden, cost of trading. For market makers, it directly impacts profitability, especially when frequently rebalancing or exiting positions.
## Mechanism / math
[[slippage]] is a component included in the [[economic-hurdle-rate-cl]] calculation:
$$
\text{Expected fees} > \text{LVR} + \text{hedge funding} + \text{rent} + \text{gas} + \text{slippage} + \text{risk premium}
$$
It can be influenced by factors such as market liquidity, order size, and [[volatility]].
## Where it matters
For automated market-making bots, minimizing [[slippage]] is crucial for maintaining profitability, particularly in strategies involving frequent rebalancing or large capital deployments/withdrawals. It's a key consideration in the design of execution algorithms and the selection of trading venues.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly includes "slippage" as a cost in the [[economic-hurdle-rate-cl]], indicating that it is a recognized and accounted-for expense in the bot's operational model. The magnitude of slippage can be difficult to predict accurately, especially under extreme market conditions.
## Related
[[economic-hurdle-rate-cl]]
[[transaction_costs_in_options]]
[[liquidity-concentration]]
[[volatility]]
[[cl-rebalancing-condition]]