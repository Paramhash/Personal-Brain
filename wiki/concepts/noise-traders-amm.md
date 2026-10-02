---
domain: cl-market-making
tags:
- dex-market-structure
- fee-economics
- liquidity-provision
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 32dd2b59147720f7
---
# Noise Traders (AMM)
**In one line:** A population of Decentralized Exchange (DEX)-specific traders who interact with Automated Market Maker (AMM) pools for idiosyncratic reasons, contributing trading fees to [[liquidity-provider|LPs]].
## Intuition
In the context of AMMs, noise traders are distinct from [[rebalancing-arbitrage|arbitrageurs]]. They trade based on their own needs or preferences, rather than exploiting price discrepancies between the AMM and external markets. Their trades generate fees, which are a source of revenue for [[liquidity-provider|LPs]]. Without noise traders, the equilibrium amount of AMM liquidity would be zero, as there would be no fee income to offset adverse selection losses.
## Key facts
*   **Motivation:** Noise traders trade for "totally idiosyncratic reasons" and may prefer AMMs over [[centralized-exchange|CEXs]] due to factors like:
    *   Inability or unwillingness to satisfy Know-Your-Customer (KYC) requirements on CEXs.
    *   Lack of trust in centralized custody of assets.
    *   Jurisdictional restrictions preventing CEX access.
    *   Value of atomically combining DEX trades with other smart contract operations.
*   **Fee Generation:** Their trades contribute fees to the AMM pool, which are a component of the "alpha-like" returns for LPs.
*   **Price Impact:** While noise traders' trades can initially move AMM pool prices, these effects are immediately offset by [[rebalancing-arbitrage|arbitrageurs]] who bring the AMM price back to the CEX price.
## Where it matters
*   **LP Profitability:** Fees from noise traders are a crucial revenue stream for [[liquidity-provider|LPs]], helping to offset losses from adverse selection (quantified by [[loss-versus-rebalancing|LVR]]).
*   **Market Microstructure:** The presence and behavior of noise traders are fundamental to the economic models of liquidity provision in decentralized exchanges.
## Related
[[rebalancing-arbitrage]], [[alpha-like-component-lp-returns]], [[liquidity-provider]], [[centralized-exchange]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]