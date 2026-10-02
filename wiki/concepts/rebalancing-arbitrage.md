---
domain: cl-market-making
tags:
- arbitrage
- dex-market-structure
- adverse-selection
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 3d7e1f480d9fbc52
---
# Rebalancing Arbitrage
**In one line:** Arbitrage activity where traders exploit price discrepancies between an Automated Market Maker (AMM) and a [[centralized-exchange|CEX]] that arise due to movements in the CEX price, effectively "sniping" the AMM's stale quotes.
## Intuition
AMMs, particularly [[constant-function-market-maker|CFMMs]], update their prices based on trades. When the external market price (on a CEX) moves, the AMM's internal price becomes "stale" relative to the CEX. Arbitrageurs profit by trading with the AMM at its outdated price and immediately unwinding the trade on the CEX at the new market price. This activity drives the AMM's reserves and price back into alignment with the CEX.
## Mechanism / math
Arbitrageurs continuously monitor the AMM pool and the CEX. When the CEX price $P_t$ changes, they identify a profitable trade with the AMM. They maximize their immediate profit by moving the AMM's reserves to the point on its [[bonding-function|invariant curve]] where the slope (representing the AMM's marginal price) equals the CEX price.

The cumulative profits of rebalancing arbitrageurs over a time interval $[0, T]$ are shown to be equal to [[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]]. This implies that LVR quantifies the losses incurred by [[liquidity-provider|LPs]] due to this arbitrage activity.
## Where it matters
*   **Adverse Selection:** Rebalancing arbitrage is a primary source of adverse selection losses for AMM [[liquidity-provider|LPs]]. These losses are a key component of the "alpha-like" returns.
*   **Price Alignment:** Arbitrageurs play a crucial role in keeping AMM prices aligned with external market prices, ensuring that the AMM remains an efficient trading venue.
*   **AMM Design:** Understanding rebalancing arbitrage is vital for designing AMMs that can mitigate these losses, for example, through mechanisms like frequent batch auctions or oracle-based pricing.
## Evidence and limits
*   **Quantification:** The paper quantifies these losses through [[loss-versus-rebalancing|LVR]], showing its dependence on price volatility and the AMM's [[marginal-liquidity-amm|marginal liquidity]].
*   **Frictions:** The model assumes frictionless arbitrage. In reality, arbitrageurs face costs like transaction fees (including "gas" fees on blockchains) and competition (e.g., "gas races"), which can reduce their profits and potentially redirect some of these profits to block miners (MEV).
## Related
[[noise-traders-amm]], [[loss-versus-rebalancing]], [[centralized-exchange]], [[slippage]], [[constant-function-market-maker]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]