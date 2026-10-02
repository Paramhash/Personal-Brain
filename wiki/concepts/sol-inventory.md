---
domain: cl-market-making
tags:
- inventory-control
- solana
- asset-management
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 6db5f62a687b7cb2
---
# SOL Inventory
**In one line:** The amount of SOL (Solana's native token) held by a market-making bot, serving both as operational capital for network interactions and as a volatile asset component of its overall equity.
## Intuition
SOL is crucial for a bot operating on the Solana blockchain, as it's required for transaction fees (gas) and account rent. However, it's also a volatile asset, meaning its value fluctuates against stablecoins like USDC. Therefore, managing [[sol-inventory]] involves balancing operational necessity with exposure to price risk.
## Mechanism / math
The total [[sol-inventory]] (`SOL_wallet`) is conceptually divided into:
*   [[sol-rent-reserve]]: A fixed amount reserved for maintaining on-chain accounts.
*   [[sol-execution-reserve]]: A buffer for transaction fees.
*   `SOL_free`: The remaining SOL available for deployment into a [[cl-position]].

The bot's overall equity ($E_t$) is calculated as:
$$
E_t = SOL_t \cdot P_t + USDC_t
$$
where $P_t$ is the price of SOL in USDC.
## Where it matters
Effective management of [[sol-inventory]] is critical for the operational continuity and risk management of a Solana-based CL market-making bot. It directly impacts the bot's ability to execute trades, maintain its on-chain presence, and influences the [[cl-hedge-target]] to mitigate directional exposure. Insufficient SOL can lead to operational failure, while excessive unhedged SOL exposes the bot to significant price risk.
## Evidence and limits
The source document defines this as a core component of the [[warehouse-manager-cl-inventory-strategy]], emphasizing the need for hard minimum constraints (`SOL_t >= SOL_min`) to prevent operational issues. The strategy acknowledges that a CL position changes the composition of inventory as price moves, necessitating careful reconciliation.
## Related
[[usdc-inventory]]
[[sol-rent-reserve]]
[[sol-execution-reserve]]
[[cl-position]]
[[cl-hedge-target]]
[[inventory-accounting]]
[[equity-accounting]]
[[adr-030-deployment-sol-reserve]]