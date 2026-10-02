---
domain: cl-market-making
tags:
- amm-mechanics
- liquidity
- lvr
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-amm-and-loss-versus-rebalancing.pdf
ingest_hashes:
- 578ebb28ede1d4f6
---
# Marginal Liquidity (AMM)
**In one line:** The second derivative of the [[pool-value-function|AMM's pool value function]], $V''(P) = x^{*'}(P)$, which quantifies how much the [[constant-function-market-maker|CFMM]] trades of the risky asset in response to a given price movement.
## Intuition
This metric reflects the "steepness" or "flatness" of the AMM's [[bonding-function|invariant curve]] at a given price point. A higher marginal liquidity means the AMM's reserves of the risky asset change more significantly for a small price change, implying it offers more liquidity at that price. It is directly related to the curvature of the bonding function: "flatter" or more linear bonding curves correspond to higher marginal liquidity.
## Mechanism / math
The marginal liquidity is formally defined as $V''(P)$, which is also equal to $x^{*'}(P)$, the derivative of the optimal risky asset holdings with respect to price.
For a sufficiently smooth [[constant-function-market-maker|CFMM]] bonding function $f(x,y)=L$, the marginal liquidity can be expressed in terms of its derivatives:
$$ \frac{dx}{dP} = \frac{\frac{\partial f}{\partial y}}{\lambda \left( \frac{\partial^2 f}{\partial x^2} + P^2 \frac{\partial^2 f}{\partial y^2} - 2P \frac{\partial^2 f}{\partial x \partial y} \right)} $$
where $\lambda$ is the Lagrange multiplier from the [[pool-value-function|pool value optimization problem]].
## Where it matters
*   **Loss-Versus-Rebalancing (LVR):** Marginal liquidity is a key determinant of [[loss-versus-rebalancing|LVR]]. The instantaneous LVR is directly proportional to the absolute value of marginal liquidity: $l(\sigma, P) = \frac{\sigma^2 P^2}{2} |x^{*'}(P)|$. Higher marginal liquidity leads to greater LVR, as the AMM trades more aggressively and thus incurs more [[slippage]] losses to [[rebalancing-arbitrage|arbitrageurs]].
*   **AMM Design:** Understanding marginal liquidity is crucial for designing AMM [[bonding-function|bonding functions]] that control the trade-off between liquidity provision and adverse selection costs. For example, [[uniswap-v3]]'s concentrated liquidity mechanism effectively allows for varying marginal liquidity across different price ranges.
## Related
[[pool-value-function]], [[loss-versus-rebalancing]], [[constant-function-market-maker]], [[bonding-function]], [[slippage]], [[rebalancing-arbitrage]], [[uniswap-v3]], [[milionis-2026-automated-market-making-and-loss-versus-rebalancing]]