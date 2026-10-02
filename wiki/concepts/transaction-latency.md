---
domain: cl-market-making
tags:
- operational-risk
- execution-risk
- blockchain
- solana
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 465ff95bd2e5adcc
---
# Transaction Latency
**In one line:** The delay between the initiation of a transaction (e.g., sending an order) and its final confirmation or completion on a blockchain network or trading venue.
## Intuition
In high-frequency trading and automated market making, speed is critical. Any delay in transaction processing can mean the market moves against the bot before its order is confirmed, leading to [[slippage]] or missed opportunities. On blockchains, latency can be variable due to network load.
## Mechanism / math
[[transaction-latency]] is a factor that widens the "execution buffer" in the [[boundary-threat-exit]] strategy:
$$
d(P_t, B) < \text{execution buffer}
$$
The buffer increases with latency, requiring the bot to initiate withdrawals earlier to ensure safe execution before a [[market-boundaries-cl]] is crossed.
## Where it matters
For a Solana-based CL market-making bot, [[transaction-latency]] directly impacts the effectiveness of its risk management, particularly its ability to react to sudden market movements or to safely exit positions. High latency can increase [[execution-risk]] and the potential for [[slippage]].
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly lists "Solana transaction latency" as a factor that should widen the "execution buffer" for the [[boundary-threat-exit]] trigger. This acknowledges its practical impact on the bot's ability to manage risk in real-time.
## Related
[[boundary-threat-exit]]
[[network-congestion]]
[[slippage]]
[[sol-execution-reserve]]
[[adr-027-socket-stability-and-boot-validation]]