---
domain: cl-market-making
tags:
- lp-hedging
- market-risk
- inventory-control
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 562ed785d90275a3
---
# Rebalancing Strategy
**In one line:** A self-financing trading strategy that continuously and frictionlessly rebalances its risky asset holdings to match those of an Automated Market Maker (AMM), but executes all trades at [[centralized-exchange|CEX]] prices.
## Intuition
The rebalancing strategy is designed to perfectly replicate the market risk exposure of an AMM [[liquidity-provider|LP]] position. By matching the AMM's risky asset holdings and trading at fair market prices (CEX prices), it isolates the profits and losses solely attributable to directional price movements of the underlying asset, effectively capturing the "beta-like" component of LP returns.
## Mechanism / math
A trading strategy is defined by holdings in the risky asset ($x_t$) and numéraire ($y_t$). For the rebalancing strategy, $x_t = x^*(P_t)$, where $x^*(P_t)$ are the AMM's optimal risky asset holdings at price $P_t$.

The monetary value of the rebalancing strategy at time $t$, $R_t$, starting from an initial value $V_0$ (equal to the CFMM's initial value), is given by:
$$R_t - V_0 = \int_0^t x^*(P_s) dP_s, \quad \forall t \ge 0$$
This integral represents the cumulative profits from trading the risky asset at CEX prices.
The strategy is self-financing and, under the risk-neutral measure, is a Q-martingale, meaning it breaks even in expectation. It only generates expected returns to the extent that the underlying risky asset has non-zero risk premia.
## Where it matters
*   **Market Risk Isolation:** It serves as a benchmark to separate the "beta-like" market risk component from the "alpha-like" microstructural component of AMM LP returns.
*   **Denoising LP P&L:** Subtracting the rebalancing strategy's profits from raw LP P&L effectively "denoises" the LP returns, removing the overwhelming influence of market price movements. This allows researchers to focus on the AMM's intrinsic market-making performance.
*   **Projection:** The rebalancing strategy corresponds to the quadratic-variation-minimizing projection of AMM profits onto the risky asset's price path, analogous to how stock betas are calculated.
## Evidence and limits
*   **Empirical Impact:** For the [[uniswap-v2]] ETH-USDC pool, subtracting the rebalancing strategy's profits reduces the variance of LP returns by four orders of magnitude, demonstrating its effectiveness in isolating market risk.
*   **Frictionless Assumption:** The model assumes frictionless trading at CEX prices. In practice, implementing such a strategy would incur transaction costs (spreads, fees, margin costs for short positions), which are not accounted for in the theoretical decomposition.
*   **Frequency Sensitivity:** The effectiveness of discrete approximations to the continuous-time rebalancing strategy depends on the rebalancing frequency. Higher frequencies (e.g., 1 minute) lead to better approximations and lower residual variance.
## Related
[[loss-versus-rebalancing]], [[alpha-like-component-lp-returns]], [[beta-like-component-lp-returns]], [[delta_hedging]], [[centralized-exchange]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]