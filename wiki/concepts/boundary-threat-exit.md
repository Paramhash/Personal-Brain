---
domain: cl-market-making
tags:
- risk-management
- exit-strategy
- volatility
- transaction-costs
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 72d9809d620497e6
---
# Boundary Threat Exit
**In one line:** A trigger for the [[cl-exit-strategy]] that initiates withdrawal from a [[cl-position]] when the projected price path indicates it could cross a [[market-boundaries-cl]] before the bot can safely execute a withdrawal.
## Intuition
Proactive risk management means not waiting until a position is already in trouble. This exit trigger anticipates potential boundary breaches, allowing the bot to withdraw gracefully and avoid forced liquidations or significant losses that could occur if it waits too long, especially in fast-moving or illiquid markets.
## Mechanism / math
Withdrawal is triggered when the distance `d(P_t, B)` between the current price ($P_t$) and a boundary ($B$, either lower or upper) is less than an "execution buffer."
This `execution buffer` is dynamic and widens with:
*   [[volatility]]
*   Solana [[transaction-latency]]
*   Expected price velocity
*   [[network-congestion]]
*   [[liquidity-concentration]]
## Where it matters
This is a critical safety mechanism within the [[cl-exit-strategy]]. It prevents the bot from being caught in a rapidly deteriorating market, where it might be unable to exit its [[cl-position]] without incurring substantial [[slippage]] or even liquidation. The dynamic buffer ensures adaptability to varying market and network conditions.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] defines this as "Exit trigger A: boundary threat," emphasizing the need to withdraw "before the position reaches a dangerous boundary, not exactly at the boundary." The factors influencing the buffer are explicitly listed.
## Related
[[cl-exit-strategy]]
[[market-boundaries-cl]]
[[volatility]]
[[transaction-latency]]
[[network-congestion]]
[[liquidity-concentration]]
[[slippage]]
[[blueprint-risk-guardrails]]
[[adr-041-wall-buffer-and-proximity-exit-are-one-policy]]