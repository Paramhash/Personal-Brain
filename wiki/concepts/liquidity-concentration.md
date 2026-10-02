---
domain: cl-market-making
tags:
- concentrated-liquidity
- market-microstructure
- slippage
- risk-management
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 6a350cfc3d44bb24
---
# Liquidity Concentration
**In one line:** The degree to which a market's available liquidity is focused at specific price points or within narrow ranges, particularly characteristic of concentrated liquidity AMMs.
## Intuition
In traditional AMMs, liquidity is spread evenly across all prices. In concentrated liquidity AMMs like Uniswap v3 or Meteora DLMM, liquidity providers can choose specific price ranges. This allows for greater capital efficiency within those ranges but means that outside those ranges, liquidity can be sparse. High [[liquidity-concentration]] around the current price can lead to lower [[slippage]] for small trades, but also means that large trades or rapid price movements can quickly exhaust available liquidity, leading to higher [[slippage]] or even price dislocations.
## Mechanism / math
[[liquidity-concentration]] is a factor that widens the "execution buffer" in the [[boundary-threat-exit]] strategy:
$$
d(P_t, B) < \text{execution buffer}
$$
When liquidity is highly concentrated, a larger buffer is needed because even small price movements can quickly push the market out of the concentrated range, making it harder to exit a [[cl-position]] without significant price impact.
## Where it matters
Understanding and managing [[liquidity-concentration]] is fundamental for [[cl-market-making]]. It influences optimal range selection, expected fee generation, and the risk of [[impermanent-loss]]. For exit strategies, it dictates how much lead time is needed to safely unwind a position.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] includes "liquidity concentration" as a factor that should widen the "execution buffer" for the [[boundary-threat-exit]] trigger. This acknowledges that the structure of liquidity itself impacts the safety of position management.
## Related
[[concentrated-liquidity]]
[[slippage]]
[[boundary-threat-exit]]
[[cl-position]]
[[m02-concentrated-liquidity-math]]