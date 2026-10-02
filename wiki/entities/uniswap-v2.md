---
domain: cl-market-making
tags:
- amm
- constant-product-market-maker
- dex
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- fa25d88418511276
---
# Uniswap v2
**What it is:** A decentralized exchange (DEX) protocol based on a [[constant-function-market-maker|Constant Product Market Maker (CPMM)]] model, characterized by the invariant $x \cdot y = k$.
## Key facts
*   **Invariant:** Uses the $x \cdot y = k$ invariant, where $x$ and $y$ are the quantities of the two assets in the pool.
*   **Fee Rate:** Has a fixed fee rate of 30 basis points (0.3%) on trades, which is typically reinvested directly into the pool reserves.
*   **Flash Loans:** Supports flash loans, where assets can be borrowed and returned within a single transaction for a fee, with revenues accounted for as swaps.
*   **LVR Calculation:** For Uniswap v2, the instantaneous [[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]] per dollar of pool reserves is constant and can be expressed simply as $\sigma^2 / 8$, where $\sigma$ is the instantaneous volatility.
## How it is used here
The paper uses the Uniswap v2 ETH-USDC trading pair for its empirical analysis, covering the period from August 1, 2021, to July 31, 2022. It analyzes LP Profit & Loss (P&L) decomposition, demonstrating that over 99.991% of its LP return variance is driven by market risk. The protocol's fixed fee rate and LVR characteristics are leveraged in the empirical methodology.
## Related
[[uniswap-v3]], [[constant-function-market-maker]], [[loss-versus-rebalancing]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]