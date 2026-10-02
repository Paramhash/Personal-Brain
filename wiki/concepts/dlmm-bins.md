---
domain: cl-market-making
tags:
- dlmm
- concentrated-liquidity
- uniswap-v3
- meteora
aliases:
- DLMM bins
- concentrated liquidity bins
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-calibration-2026-10-01.md
ingest_hashes:
- a32be602cc3106e4
---
# DLMM Bins
**In one line:** Discrete price ranges within a Dynamic Liquidity Market Maker (DLMM) where liquidity providers can concentrate their capital.
## Intuition
Unlike traditional [[constant-function-market-maker|CFMMs]] like [[uniswap-v2]] that distribute liquidity uniformly across all prices, DLMMs (and [[uniswap-v3]]) allow LPs to specify narrow price ranges, or "bins," where their capital is active. This enables capital efficiency by ensuring liquidity is only deployed where it is most likely to be traded.
## Mechanism / math
DLMMs, such as Meteora's, use a system of discrete price bins. LPs deposit assets into specific bins, defining the price range within which their liquidity will be used for swaps. When the market price moves into a bin where an LP has provided liquidity, that liquidity becomes active. When the price moves out of that bin, the liquidity becomes inactive.

Key characteristics:
*   **Concentration:** LPs can concentrate their capital around the current market price, earning more fees on less capital.
*   **Dynamic Adjustment:** Bins can be dynamically adjusted or rebalanced by LPs in response to market movements or changes in their strategy.
*   **Constant-sum within bins:** Within a single bin, the liquidity typically behaves like a constant-sum market maker, meaning the inventory of the two assets changes linearly as trades occur.
*   **LVR accrual:** [[loss-versus-rebalancing|LVR]] accrues only at bin crossings, as inventory conversion (and thus the opportunity for arbitrageurs to rebalance) primarily happens when the price moves from one bin to another.
## Where it matters
DLMM bins are fundamental to the design and operation of concentrated liquidity AMMs. They enable:
*   **Capital Efficiency:** LPs can achieve higher capital efficiency compared to full-range AMMs.
*   **Customization:** LPs can implement diverse strategies by choosing specific price ranges.
*   **Active Management:** Requires more active management from LPs to adjust their positions as prices move.
*   **Fee Generation:** Fees are generated when trades occur within an LP's active bins.
## Related
[[concentrated-liquidity]]
[[uniswap-v3]]
[[meteora]]
[[cl-market-making]]
[[loss-versus-rebalancing]]
[[pool-value-function]]
[[marginal-liquidity-amm]]