---
domain: cl-market-making
tags:
- risk-management
- exit-strategy
- market-regimes
- gex
- volatility
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 7e168a5b314cf666
---
# Regime Deterioration Exit
**In one line:** A trigger for the [[cl-exit-strategy]] that initiates a defensive withdrawal from a [[cl-position]] when off-chain [[gamma-exposure-gex]] signals or other market indicators suggest a likely [[market-regime-transition]] or significant increase in risk.
## Intuition
Market conditions are not static; they shift between different "regimes" (e.g., low volatility, high volatility, trending, mean-reverting). A strategy optimized for one regime might perform poorly or become highly risky in another. This exit trigger allows the bot to proactively de-risk in anticipation of a regime change, rather than reacting after losses have already occurred.
## Mechanism / math
Defensive withdrawal is triggered by signals such as:
*   Spot price approaching the [[zero-gamma-level]].
*   Sharply rising [[volatility]].
*   Movement of the wall envelope (e.g., [[buffered-policy-envelope]]).
*   The range becoming materially asymmetric.
*   The projected [[lvr-and-impermanent-loss|LVR]] rate rising above fee production.

The strategy recommends using persistence or hysteresis to avoid unnecessary withdrawals due to noisy observations.
## Where it matters
This exit strategy provides an early warning system for systemic risk, complementing price-based and economic exit triggers. It allows the bot to adapt its risk exposure to broader market dynamics, protecting capital during periods of increased uncertainty or unfavorable market structure. It is a key component of an adaptive market-making strategy.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] defines this as "Exit trigger C: regime deterioration," emphasizing its role in reacting to off-chain GEX signals and other market indicators. The inclusion of hysteresis acknowledges the challenge of noisy signals in real-time market data.
## Related
[[cl-exit-strategy]]
[[gamma-exposure-gex]]
[[market-regimes]]
[[volatility]]
[[zero-gamma-level]]
[[lvr-and-impermanent-loss]]
[[blueprint-gex-intelligence]]
[[blueprint-risk-guardrails]]
[[market-regime-transition]]