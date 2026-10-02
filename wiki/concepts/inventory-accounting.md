---
domain: cl-market-making
tags:
- accounting
- inventory-control
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-00-dual-inventory-growth-policy.md
ingest_hashes:
- 8467aff3526a4679
---
# Inventory Accounting
**In one line:** A method of tracking the individual balances of each token in a portfolio, independent of their combined market value, to ensure specific growth targets for each asset are met.
## Intuition
For a market-making bot, simply tracking total equity (value in a single numeraire) is often insufficient. The bot needs specific quantities of *both* base and quote assets to operate effectively, deploy new liquidity, or manage existing positions. `[[inventory-accounting]]` provides a granular view of each asset's balance, allowing the bot to ensure that it is growing or maintaining its holdings in each required token, rather than inadvertently depleting one while overall equity rises due to price appreciation of the other.
## Mechanism / math
`[[inventory-accounting]]` tracks the change in quantity for each asset independently. For a portfolio with SOL and USDC, this involves monitoring:
$$
\Delta SOL = SOL_{close} - SOL_{start}
$$
$$
\Delta USDC = USDC_{close} - USDC_{start}
$$
The objective under a `[[dual-inventory-growth-policy]]` is to achieve $\Delta SOL > 0$ and $\Delta USDC > 0$.
## Where it matters
`[[inventory-accounting]]` is crucial for:
*   **Dual-inventory growth policies:** Directly supports the objective of growing both base and quote assets.
*   **Operational sustainability:** Ensures the bot retains sufficient quantities of each token for future deployments, rebalances, or other operational needs.
*   **Rebalancing decisions:** Informs when and how much of one asset needs to be converted into another to meet individual growth targets.
*   **Risk management:** Helps identify imbalances in asset holdings that might pose operational risks.

It complements `[[equity-accounting]]`, which provides a high-level view of total value, by offering the detailed, token-specific information necessary for strategic asset management.
## Evidence and limits
This is a practical accounting method for managing multi-asset portfolios, particularly in automated trading contexts. Its effectiveness depends on the ability to accurately track and manage individual token flows. It is a necessary component for strategies that prioritize specific asset growth over mere total value growth.
## Related
[[equity-accounting]], [[dual-inventory-growth-policy]], [[two-accounting-layers]], [[dlmm-dual-inventory-growth-policy]], [[m07-inventory-and-market-making-theory|inventory control]]