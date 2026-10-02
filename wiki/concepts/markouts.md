---
domain: cl-market-making
tags:
- performance-metrics
- trade-execution
- lp-profitability
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 1411ec599c352be7
---
# Markouts
**In one line:** An industry practice used to evaluate [[constant-function-market-maker|CFMM]] [[liquidity-provider|LP]] Profit & Loss (P&L) by comparing the price of each trade to a future price, typically at a fixed time offset (e.g., 10 minutes) from a [[centralized-exchange|CEX]] or the CFMM itself.
## Intuition
Markouts, also known as "realized spread" in microstructure literature, aim to attribute profits to trades by assessing how favorable the trade price was relative to where the market settles shortly after the trade. It provides a way to measure the immediate impact and profitability of individual trades or a series of trades.
## Mechanism / math
The core idea is to calculate the difference between the execution price of a trade and a "marking price" observed at a later time. For example, if an LP facilitates a trade at price $P_{trade}$, and the market price 10 minutes later is $P_{mark}$, the markout profit/loss for that trade would be related to $(P_{mark} - P_{trade})$.

The paper notes a close relationship between markouts and delta-hedging: the P&L of delta-hedged LPing, when rebalanced at discrete periods, is exactly equivalent to markout profits, marked to CEX prices at the end of discrete periods of the same frequency. The main difference lies in whether the marking price is a fixed offset in the future or the ending price of the interval the trade occurred in.
## Where it matters
*   **LP Profitability Assessment:** Used by industry participants to gauge the profitability of providing liquidity, particularly in concentrated liquidity AMMs like [[uniswap-v3]].
*   **Microfoundation:** Delta-hedged LPing can be considered a microfoundation for markout-style analysis, providing a theoretical link between hedging strategies and realized spread metrics.
## Related
[[delta_hedging]], [[liquidity-provider]], [[constant-function-market-maker]], [[centralized-exchange]], [[uniswap-v3]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]