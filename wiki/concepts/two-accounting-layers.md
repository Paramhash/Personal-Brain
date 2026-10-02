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
- 713e480d00033a9c
---
# Two Accounting Layers
**In one line:** The necessity for a concentrated liquidity bot to maintain distinct `[[equity-accounting]]` and `[[inventory-accounting]]` systems to track overall value and individual asset growth targets, respectively.
## Intuition
A market-making bot operating with multiple assets (e.g., SOL and USDC) has two distinct, but related, financial objectives. First, it needs to know its total wealth or net asset value, which is best captured by `[[equity-accounting]]`. Second, it needs to ensure it maintains and grows the *quantities* of each specific asset it trades, which is the domain of `[[inventory-accounting]]`. These two perspectives are not interchangeable; an increase in total equity can occur even if one asset's quantity is depleted due to price movements. Therefore, both layers are essential for a comprehensive understanding of the bot's financial state and for implementing a `[[dual-inventory-growth-policy]]`.
## Mechanism / math
The two accounting layers are:
1.  **Equity Accounting:** Values all assets in a single numeraire (e.g., USDC).
    $$
    E_t = SOL_t \cdot P_t + USDC_t
    $$
    This layer tracks $\Delta E = E_{close} - E_{start}$.
2.  **Inventory Accounting:** Tracks the nominal quantities of each individual asset.
    $$
    (\Delta SOL, \Delta USDC) = (SOL_{close} - SOL_{start},\; USDC_{close} - USDC_{start})
    $$
    This layer tracks the change in each token balance independently.

The critical implication is that $\Delta E > 0$ does not necessarily imply $\Delta SOL > 0$ and $\Delta USDC > 0$. Both sets of metrics must be monitored and reported.
## Where it matters
The concept of `[[two-accounting-layers]]` is fundamental for:
*   **Strategic alignment:** Ensures the bot's actions align with the `[[dual-inventory-growth-policy]]` by providing the necessary data for both overall value and individual asset growth.
*   **Decision-making:** Informs the `[[decision-gate-cl-bot]]` by providing the specific asset growth metrics required for deployment and exit conditions.
*   **Performance reporting:** Allows for a nuanced understanding of the bot's performance, distinguishing between gains from price appreciation (reflected in equity) and gains from active market making (reflected in inventory growth).
*   **Risk management:** Helps identify situations where overall equity looks healthy, but underlying asset balances are becoming imbalanced or depleted.
## Evidence and limits
This is an architectural requirement for a sophisticated market-making bot with specific asset-growth objectives. It addresses the limitation of single-numeraire accounting in multi-asset trading environments. The primary challenge is ensuring consistent and accurate data flow to both accounting layers.
## Related
[[equity-accounting]], [[inventory-accounting]], [[dual-inventory-growth-policy]], [[dlmm-dual-inventory-growth-policy]], [[m07-inventory-and-market-making-theory|inventory control]]