---
domain: cl-market-making
tags:
- amm
- dex
- invariant
aliases:
- CFMM
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- d83bda8dd195c37a
---
# Constant Function Market Maker
**In one line:** An Automated Market Maker (AMM) characterized by an invariant or [[bonding-function|bonding function]] $f(x,y) = L$, where $x$ and $y$ are the reserves of two assets in the pool, and $L$ is a constant.
## Intuition
CFMMs define a curve along which the pool's reserves must always lie. Any trade moves the pool's reserves along this curve. The instantaneous exchange rate (price) offered by the CFMM is determined by the slope of this curve at the current reserve point.
## Key facts
*   **Invariant Curve:** The core of a CFMM is its [[bonding-function|bonding function]] $f(x,y)=L$, which defines the feasible set of reserves. Examples include:
    *   **Constant Product Market Maker (CPMM):** $f(x,y) = \sqrt{xy} = L$ (e.g., [[uniswap-v2]]).
    *   **Weighted Geometric Mean Market Maker:** $f(x,y) = x^\theta y^{1-\theta} = L$ (generalizes CPMM).
    *   **Range Order:** For concentrated liquidity AMMs like [[uniswap-v3]], the bonding function can be more complex, defining liquidity within specific price ranges.
*   **Price Alignment:** In the presence of [[rebalancing-arbitrage|arbitrageurs]], the CFMM's price (the negative slope of its invariant curve) is always equal to the external market price $P$ (from a [[centralized-exchange|CEX]]). Arbitrageurs ensure the pool reserves shift to the point on the curve where the slope is $-P$.
*   **LP P&L Decomposition:** The profit and loss of a CFMM [[liquidity-provider|LP]] can be decomposed into a "beta-like" market risk component and an "alpha-like" microstructural component, with the latter reflecting accrued fees minus [[loss-versus-rebalancing|LVR]] (losses to arbitrageurs).
## Where it matters
*   **Foundation of AMMs:** CFMMs are the foundational model for many decentralized exchanges.
*   **Liquidity Provision:** LPs provide capital to CFMMs, earning fees but bearing risks like [[loss-versus-rebalancing|LVR]].
*   **Market Microstructure:** The design of the [[bonding-function|bonding function]] directly impacts the CFMM's [[marginal-liquidity-amm|marginal liquidity]] and thus its exposure to [[loss-versus-rebalancing|LVR]].
## Related
[[bonding-function]], [[pool-value-function]], [[marginal-liquidity-amm]], [[rebalancing-arbitrage]], [[loss-versus-rebalancing]], [[uniswap-v2]], [[uniswap-v3]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]