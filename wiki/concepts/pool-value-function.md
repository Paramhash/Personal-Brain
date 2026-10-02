---
domain: cl-market-making
tags:
- amm-mechanics
- lp-returns
- valuation
aliases:
- V(P)
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 551365e3669cff42
---
# Pool Value Function
**In one line:** A function $V(P)$ that measures the monetary value of an Automated Market Maker's (AMM) reserves at a given risky asset price $P$, assuming [[rebalancing-arbitrage|arbitrageurs]] have optimized their trades to align the AMM's price with the [[centralized-exchange|CEX]] price.
## Intuition
The presence of arbitrageurs ensures that the AMM's internal price is always aligned with the external market price. Therefore, the total value of the assets held by the AMM pool at any given time is solely determined by the current market price of the risky asset. The pool value function formalizes this relationship.
## Mechanism / math
The pool value function $V(P)$ is defined as the solution to the optimization problem:
$$V(P) = \min_{(x,y) \in \mathbb{R}^2} Px + y$$
$$ \text{subject to } f(x,y) = L $$
where $x$ is the quantity of the risky asset, $y$ is the quantity of the numéraire, $P$ is the price of the risky asset, $f(x,y)=L$ is the [[constant-function-market-maker|CFMM]]'s [[bonding-function|invariant curve]], and $L$ is a constant.

Key properties of the pool value function:
1.  $V(P) \ge 0$ for all $P \ge 0$.
2.  The first derivative $V'(P) = x^*(P)$, where $x^*(P)$ is the optimal holding of the risky asset at price $P$. This means the slope of the pool value function equals the reserves in the risky asset.
3.  The second derivative $V''(P) = x^{*'}(P) \le 0$. This implies the pool value function is concave and its second derivative represents the [[marginal-liquidity-amm|marginal liquidity]] available at price $P$.
## Where it matters
*   **LP P&L Calculation:** The change in the pool's value ($V_t - V_0$) is a core component of the total LP Profit & Loss.
*   **LVR Derivation:** The pool value function is central to the derivation of [[loss-versus-rebalancing|Loss-Versus-Rebalancing (LVR)]], as its second derivative directly relates to the instantaneous LVR.
*   **AMM Characterization:** Its properties, particularly concavity and the relationship between its derivatives and asset holdings/marginal liquidity, provide insights into the economic behavior of CFMMs.
## Evidence and limits
*   **General Applicability:** The concept applies to a broad class of CFMMs, including [[uniswap-v2]] (constant product) and [[uniswap-v3]] (range orders), although the smoothness requirements for its derivatives may not hold for all AMM types (e.g., linear market makers).
*   **Option Analogy:** The concavity of $V(P)$ implies that an AMM LP position is essentially equivalent to giving away a bundle of European options, as options also have concave payoff functions.
## Related
[[constant-function-market-maker]], [[bonding-function]], [[marginal-liquidity-amm]], [[loss-versus-rebalancing]], [[rebalancing-arbitrage]], [[liquidity-provider]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]