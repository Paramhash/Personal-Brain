---
domain: cl-market-making
tags:
- game-theory
- cl-market-making
- strategy
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-02-nash-equilibrium-cl-provider-strategies.md
ingest_hashes:
- 582f5a8e4e64367a
---
# Nash Equilibrium in CL Strategies
**In one line:** A strategy profile for concentrated liquidity providers (CLPs) where no individual CLP can improve its payoff by unilaterally changing its strategy, given the strategies of all other CLPs.
## Intuition
In a competitive concentrated liquidity (CL) market, the optimal strategy for an individual liquidity provider (LP) is not independent but rather depends on the actions of other LPs. A Nash equilibrium describes a stable state where every LP is playing their "best response" to the strategies chosen by all other LPs, meaning no one has an incentive to deviate alone.
## Mechanism / math
A [[cl-provider-strategy|CL provider's strategy]] $s_i$ for provider $i$ is defined as a tuple:
$$
s_i = (R_i, C_i, \rho_i, H_i, \tau_i)
$$
where $R_i$ is the price range, $C_i$ is deployed capital, $\rho_i$ is the liquidity shape across bins, $H_i$ is the hedge policy, and $\tau_i$ is the withdrawal or redeployment trigger.

The [[cl-payoff-function|simplified LP payoff]] $U_i$ is:
$$
U_i = \text{fees}_i - \text{LVR}_i - \text{hedge funding}_i - \text{slippage}_i - \text{gas/rent}_i
$$
A strategy profile $s^*$ (where $s^* = (s_1^*, s_2^*, ..., s_N^*)$ for $N$ providers) is a Nash equilibrium when:
$$
U_i(s_i^*, s_{-i}^*) \geq U_i(s_i, s_{-i}^*)
$$
for every provider $i$ and every unilateral alternative strategy $s_i$, where $s_{-i}^*$ represents the strategies of all other providers.

LPs interact, meaning other providers' choices affect:
*   Fee share
*   Liquidity depth
*   Price impact
*   Arbitrage intensity
*   Probability of becoming out of range
*   Profitability of hedging
## Where it matters
Understanding Nash equilibrium is crucial for designing robust [[cl-provider-strategy|CL provider strategies]] that account for competitor behavior. It informs decisions on [[competing-range-placement|range placement]], [[capital-allocation-liquidity-shape|capital allocation across bins]], and [[coordinated-withdrawal-cl|withdrawal timing]] in a multi-LP environment. It helps LPs anticipate market reactions and avoid suboptimal outcomes from purely individualistic optimization.
## Evidence and limits
The source provides a conceptual framework for applying Nash equilibrium to CL strategies. It highlights that a Nash equilibrium does not automatically guarantee profitability for participants, only stability against unilateral deviation. The entire equilibrium could still result in negative payoffs if overall market conditions are unfavorable.
## Related
[[cl-provider-strategy]], [[cl-payoff-function]], [[competing-range-placement]], [[capital-allocation-liquidity-shape]], [[coordinated-withdrawal-cl]], [[iterative-best-response]], [[concentrated-liquidity]], [[game-theory]], [[dlmm-2026-nash-equilibrium-cl-provider-strategies]]