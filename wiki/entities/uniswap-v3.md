---
domain: cl-market-making
tags:
- amm
- concentrated-liquidity
- dex
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 5bd238c6a5ff6dd9
---
# Uniswap v3
**What it is:** A decentralized exchange (DEX) protocol that introduced "concentrated liquidity," allowing [[liquidity-provider|LPs]] to allocate capital within specific price ranges rather than across the entire price curve.
## Key facts
*   **Concentrated Liquidity:** LPs can specify a price range for their liquidity, effectively creating individual "range orders." This allows for greater capital efficiency compared to [[uniswap-v2|Uniswap v2]]'s full-range liquidity.
*   **Aggregated Liquidity:** A Uniswap v3 pool aggregates liquidity across a set of these individual range orders.
*   **LVR Applicability:** The concept of [[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]] applies to general concentrated liquidity AMMs like Uniswap v3, provided they have a locally-smooth demand curve. The instantaneous LVR per dollar of pool reserves can be arbitrarily high if the liquidity range is sufficiently narrow, consistent with the idea of concentrated liquidity.
## How it is used here
The paper references Uniswap v3 as an example of a concentrated liquidity AMM where the [[loss-versus-rebalancing|LVR]] framework is applicable. It notes that the LVR calculation for Uniswap v3 (modeled as aggregated range orders) can be performed using the same principles as for [[constant-function-market-maker|CFMMs]] with a locally-smooth demand curve.
## Related
[[uniswap-v2]], [[concentrated-liquidity]], [[loss-versus-rebalancing]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]