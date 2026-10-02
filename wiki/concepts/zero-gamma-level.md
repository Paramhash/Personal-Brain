---
domain: derivatives
tags:
- gex
- market-regimes
- options-greeks
- market-microstructure
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 1cd7b245f262f582
---
# Zero-Gamma Level
**In one line:** A price level where the aggregate [[gamma-exposure-gex|gamma exposure]] of market participants (e.g., options dealers) is zero, often indicating a potential shift in market dynamics.
## Intuition
Options dealers typically hedge their [[option-greeks]], including gamma. When the market's aggregate gamma is positive, dealers tend to buy into falling prices and sell into rising prices, creating a dampening effect on volatility. When aggregate gamma is negative, dealers do the opposite, potentially exacerbating price movements. The [[zero-gamma-level]] is a critical inflection point where this hedging behavior can reverse, leading to increased volatility or a change in market direction.
## Mechanism / math
The [[zero-gamma-level]] is used as a signal in the [[regime-deterioration-exit]] strategy for a CL market-making bot. If the spot price approaches this level, it is considered an indicator of heightened risk for a [[market-regime-transition]].
## Where it matters
Understanding the [[zero-gamma-level]] is important for anticipating potential changes in market behavior, especially in options-driven markets. For market makers, approaching this level can signal a need to de-risk or adjust strategies, as the market's sensitivity to price changes may increase.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] includes "spot approaches the zero-gamma level" as a trigger for the [[regime-deterioration-exit]]. This highlights its use as an early warning signal for potential market instability. The accuracy and predictive power of the [[zero-gamma-level]] depend on the quality of [[gamma-exposure-gex]] data and the assumptions about dealer hedging behavior.
## Related
[[gamma-exposure-gex]]
[[gamma-exposure-gex]]
[[market-regimes]]
[[regime-deterioration-exit]]
[[volatility]]
[[option-greeks]]
[[blueprint-gex-intelligence]]