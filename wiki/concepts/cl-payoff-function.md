---
domain: cl-market-making
tags:
- cl-market-making
- fee-economics
- lvr
- strategy
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-02-nash-equilibrium-cl-provider-strategies.md
ingest_hashes:
- 16741270a723ec8c
---
# CL Provider Payoff Function
**In one line:** A simplified mathematical representation of the net economic benefit (or loss) for a concentrated liquidity provider (CLP) over a given period, considering various costs and revenues.
## Intuition
Concentrated liquidity providers (CLPs) aim to maximize their profits. The payoff function quantifies the primary financial components that contribute to an LP's overall return, balancing the revenue generated (fees) against the various costs and risks incurred (LVR, hedging, transaction costs).
## Mechanism / math
The simplified payoff $U_i$ for provider $i$ is expressed as:
$$
U_i = \text{fees}_i - \text{LVR}_i - \text{hedge funding}_i - \text{slippage}_i - \text{gas/rent}_i
$$
Where:
*   $\text{fees}_i$: The total fees earned by provider $i$ from trades within their active liquidity range.
*   $\text{LVR}_i$: The [[loss-versus-rebalancing|Loss-Versus-Rebalancing]] incurred by provider $i$, representing the opportunity cost or loss compared to a passive holding strategy.
*   $\text{hedge funding}_i$: The costs associated with maintaining a [[hedge-policy|hedging position]] to neutralize inventory delta, including funding rates for perpetual futures.
*   $\text{slippage}_i$: Costs arising from price impact during trades or rebalances, particularly in illiquid markets.
*   $\text{gas/rent}_i$: Transaction costs, such as blockchain gas fees for on-chain operations or protocol rent.
## Where it matters
This payoff function is a core component for evaluating the effectiveness of different [[cl-provider-strategy|CL provider strategies]], especially in the context of [[nash-equilibrium-cl-strategies|game-theoretic analysis]]. It is also critical for [[economic-hurdle-rate-cl|hurdle rate calculations]] and overall profitability assessment for [[concentrated-liquidity]] positions. By breaking down the components, LPs can identify key drivers of profit and loss.
## Evidence and limits
The source presents this as a simplified model for analytical purposes. Actual payoffs in real-world CL environments can be more complex, potentially involving opportunity costs, capital efficiency metrics, and specific protocol mechanics not explicitly captured in this formula.
## Related
[[nash-equilibrium-cl-strategies]], [[cl-provider-strategy]], [[loss-versus-rebalancing]], [[fee-economics]], [[slippage]], [[network-congestion|gas/rent]], [[hedge-policy]], [[economic-hurdle-rate-cl]], [[dlmm-2026-nash-equilibrium-cl-provider-strategies]]