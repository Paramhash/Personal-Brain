---
domain: cl-market-making
tags:
- lp-returns
- adverse-selection
- performance-metrics
aliases:
- IL
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 587838d742f069af
---
# Impermanent Loss
**In one line:** A common, but often problematic, metric in Automated Market Maker (AMM) contexts, typically defined as the difference between the current value of an AMM's reserves and the value of a static portfolio holding the same assets as the AMM at some fixed point in the past.
## Intuition
The term "impermanent loss" colloquially refers to the potential for a [[liquidity-provider|LP]]'s portfolio value to be less than if they had simply held (HODL) their initial assets, especially when prices diverge. The "impermanence" implies that if prices revert to the initial state, the loss might disappear.
## Mechanism / math
The paper defines "one-interval" impermanent loss as equivalent to [[loss-versus-holding|Loss-Versus-Holding (LVH)]], where the benchmark is a static portfolio of initial holdings $x^*(P_0)$.
$$IL_t = LVH_t = (P_t x^*(P_0) + y^*(P_0)) - (P_t x^*(P_t) + y^*(P_t))$$
This metric is always non-negative.
## Problems and limits
The paper highlights several critical issues with using "impermanent loss" as a robust metric for AMM LP performance:
1.  **Non-Additivity:** It does not aggregate cleanly over time. $IL_{t_1,t_2} + IL_{t_2,t_3} \neq IL_{t_1,t_3}$. This means losses can appear and disappear depending on the measurement interval, making cumulative assessment difficult.
2.  **Path-Independence:** It depends only on the initial and final prices, not on the price path taken. This is economically problematic as actual adverse selection costs should depend on volatility and price movements.
3.  **Arbitrary Start Point:** Its value and even sign can be manipulated by the arbitrary choice of the fixed start point for the benchmark portfolio.
4.  **Conflation of Market Risk:** The "one-interval" impermanent loss (equivalent to [[loss-versus-holding|LVH]]) fails to fully remove [[market-risk]] from returns. It combines microstructural forces with predictable exposure to risky asset prices, with the latter often being orders of magnitude larger. For [[uniswap-v2]] ETH-USDC, this market risk component drives over 99.991% of the variance.

**Recommendation:** The paper recommends against using "one-interval" impermanent loss. Instead, it suggests using [[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]] or "hedged LP returns" (which is equivalent to a "many-interval" IL with frequently updated benchmarks) for empirical analysis, as these metrics cleanly separate market risk from microstructural effects.
## Related
[[loss-versus-rebalancing]], [[loss-versus-holding]], [[liquidity-provider]], [[hodl-benchmark]], [[market-risk]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]