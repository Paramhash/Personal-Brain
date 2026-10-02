---
domain: cl-market-making
tags:
- market-risk
- lp-returns
- portfolio-management
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 0bf150b29f9705c7
---
# Beta-like Component (LP Returns)
**In one line:** The component of Automated Market Maker (AMM) [[liquidity-provider|LP]] returns that reflects the market risk exposure of the underlying assets held by the AMM, analogous to a mutual fund's exposure to market factors.
## Intuition
An AMM providing liquidity holds a portfolio of assets (e.g., ETH and USDC). As the price of the risky asset (ETH) changes, the value of this portfolio changes, generating profits or losses. This exposure to the directional movements of the underlying asset's price is the "beta-like" component. It is not unique to the AMM and can be replicated by a simple trading strategy.
## Mechanism / math
The total LP Profit & Loss (P&L) can be decomposed as:
$$LP P\&L_t = \text{Beta-like Component} + \text{Alpha-like Component}$$
The beta-like component is captured by the profits of the [[rebalancing-strategy]], which continuously matches the AMM's risky asset holdings but trades at [[centralized-exchange|CEX]] prices.
$$ \text{Beta-like Component}_t = \int_0^t x^*(P_s) dP_s $$
where $x^*(P_s)$ are the AMM's risky asset holdings at price $P_s$.
## Where it matters
*   **Dominant Risk Factor:** This component typically accounts for the vast majority of variance in raw AMM LP returns, often overwhelming the "alpha-like" microstructural component.
*   **Hedging:** To accurately assess an AMM's market-making performance, this market risk exposure must be hedged out. The [[rebalancing-strategy]] serves as the theoretical basis for this hedging.
*   **Empirical Bias:** Failing to remove this component in empirical studies can lead to misleading conclusions, as any observed effects are likely to be driven by general market movements rather than AMM-specific microstructural factors.
## Evidence and limits
*   **Empirical Significance:** For the [[uniswap-v2]] ETH-USDC pool, the beta-like component drives over 99.991% of the variance in unhedged LP P&L.
*   **Replicability:** This component can be replicated by trading the underlying asset on a CEX, making it a "mechanical" part of LP returns rather than a unique feature of the AMM.
## Related
[[rebalancing-strategy]], [[alpha-like-component-lp-returns]], [[market-risk]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]