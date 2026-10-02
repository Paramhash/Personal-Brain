---
domain: cl-market-making
tags:
- accounting
- valuation
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-00-dual-inventory-growth-policy.md
ingest_hashes:
- bab5a537231bce58
---
# Equity Accounting
**In one line:** A method of valuing a portfolio by converting all assets into a single numeraire, typically used to track overall portfolio value.
## Intuition
Equity accounting provides a consolidated view of the total value of a portfolio at any given time. By converting all diverse assets (e.g., different cryptocurrencies, fiat) into a common unit of account (the numeraire), it allows for a straightforward assessment of overall wealth and profit/loss. This is useful for high-level performance tracking and reporting.
## Mechanism / math
For a portfolio holding SOL and USDC, with USDC as the numeraire, equity ($E_t$) at time $t$ is calculated as:
$$
E_t = SOL_t \cdot P_t + USDC_t
$$
where $SOL_t$ is the quantity of SOL, $USDC_t$ is the quantity of USDC, and $P_t$ is the price of SOL in USDC at time $t$.

The change in equity ($\Delta E$) over a period is:
$$
\Delta E = E_{close} - E_{start}
$$
## Where it matters
`[[equity-accounting]]` is fundamental for:
*   **Overall performance tracking:** Provides a single metric for total portfolio value.
*   **Profit/Loss calculation:** Easily determines if the portfolio has gained or lost value in numeraire terms.
*   **High-level reporting:** Simplifies communication of financial performance.

However, for strategies like the `[[dual-inventory-growth-policy]]` in concentrated liquidity market making, `[[equity-accounting]]` alone is insufficient. An increase in total equity can mask a decrease in the quantity of one of the underlying assets due to price movements, which may be detrimental to the bot's operational goals. Therefore, it must be complemented by `[[inventory-accounting]]`.
## Evidence and limits
This is a standard financial accounting concept. Its limit in the context of a CL bot is that it does not provide granular insight into the individual growth or depletion of specific token balances, which is crucial for maintaining operational capacity in a multi-asset environment.
## Related
[[inventory-accounting]], [[dual-inventory-growth-policy]], [[two-accounting-layers]], [[dlmm-dual-inventory-growth-policy]]