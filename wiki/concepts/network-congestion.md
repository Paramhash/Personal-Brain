---
domain: cl-market-making
tags:
- operational-risk
- blockchain
- solana
- execution-risk
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 1361e11549e671f0
---
# Network Congestion
**In one line:** A state where a blockchain network experiences high demand for transaction processing, leading to slower confirmation times, increased [[transaction-latency]], and potentially higher transaction fees.
## Intuition
Just like a highway during rush hour, a blockchain can become congested when too many users try to send transactions simultaneously. This slows down the network and makes it more expensive to get transactions processed quickly. For a trading bot, this can be disastrous, as time-sensitive operations might be delayed or fail.
## Mechanism / math
[[network-congestion]] is a factor that widens the "execution buffer" in the [[boundary-threat-exit]] strategy:
$$
d(P_t, B) < \text{execution buffer}
$$
Increased congestion necessitates a larger buffer, meaning the bot must initiate withdrawals even earlier to account for potential delays in transaction finality.
## Where it matters
For a Solana-based CL market-making bot, [[network-congestion]] is a significant operational risk. It can impair the bot's ability to rebalance, adjust hedges, or exit positions in a timely manner, potentially leading to increased [[impermanent-loss]], [[slippage]], or even forced liquidation. Managing this risk is crucial for the bot's resilience.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly includes "network congestion" as a factor that should widen the "execution buffer" for the [[boundary-threat-exit]] trigger. This acknowledges its direct impact on the bot's ability to safely manage its positions.
## Related
[[transaction-latency]]
[[boundary-threat-exit]]
[[sol-execution-reserve]]
[[slippage]]
[[adr-027-socket-stability-and-boot-validation]]