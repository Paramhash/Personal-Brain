---
domain: cl-market-making
tags:
- impermanent-loss
- lp-returns
- performance-metrics
aliases:
- LVH
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 150f67e1b9313957
---
# Loss-Versus-Holding
**In one line:** A loss metric that evaluates an Automated Market Maker (AMM) [[liquidity-provider|LP]]'s Profit & Loss (P&L) against a static [[hodl-benchmark|buy-and-hold portfolio]] of the initial asset mix, often colloquially referred to as "[[impermanent-loss|impermanent loss]]" in industry practice.
## Mechanism / math
Loss-Versus-Holding (LVH) at time $t$ is defined as the difference between the monetary value of a static buy-and-hold portfolio (holding the initial risky asset position $x^*(P_0)$) and the current value of the AMM pool $V_t$:
$$LVH_t = R_t(x^{HODL}) - V_t = (P_t x^*(P_0) + y^*(P_0)) - (P_t x^*(P_t) + y^*(P_t))$$
where $R_t(x^{HODL})$ is the value of the buy-and-hold strategy, and $V_t$ is the [[pool-value-function|pool value function]] at time $t$.
LVH is always non-negative, meaning it can be viewed as a "cost."
## Problems with Loss-Versus-Holding
*   **Non-Additivity (Fails Cumulation Property):** LVH does not aggregate cleanly over time. For example, $LVH_{t_1,t_2} + LVH_{t_2,t_3} \neq LVH_{t_1,t_3}$. This means that positive losses can accrue in individual sub-intervals, but the total loss over a longer period might be zero if prices revert to their starting point. This makes it difficult to unambiguously assess cumulative performance.
*   **Path-Independence:** LVH depends only on the initial and final prices ($P_0$ and $P_T$), not on the path of prices between them. This is economically problematic because adverse selection costs should naturally depend on price volatility.
*   **Arbitrary Start Point:** The magnitude and even the sign of incremental profit/loss can depend on the arbitrarily chosen reference (start) point for the static portfolio.
*   **Conflation of Market Risk:** LVH benchmarks against fixed holdings, meaning it accrues [[market-risk]] as the AMM's holdings diverge from the benchmark over time. This conflates the "beta-like" market risk component with the "alpha-like" microstructural component, making it difficult to isolate the AMM's market-making performance. The market risk component can be orders of magnitude larger than the microstructural signal.
## Where it matters
*   **Misleading Metric:** Due to its significant limitations, LVH is generally not recommended for empirical analysis of AMM LP returns, especially when the goal is to understand microstructural effects.
*   **Contrast with LVR:** [[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]] addresses these issues by being additive, path-dependent, and cleanly separating market risk.
## Related
[[impermanent-loss]], [[loss-versus-rebalancing]], [[hodl-benchmark]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]