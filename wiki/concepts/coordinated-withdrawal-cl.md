---
domain: cl-market-making
tags:
- game-theory
- cl-market-making
- strategy
- market-timing
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-02-nash-equilibrium-cl-provider-strategies.md
ingest_hashes:
- 831fc7fe577d6b4e
---
# Coordinated Withdrawal in CL
**In one line:** A game-theoretic scenario where concentrated liquidity providers (CLPs) decide whether to remain deployed or withdraw liquidity, with the optimal choice potentially depending on the expected actions of other CLPs, especially during anticipated market regime shifts.
## Intuition
When a significant market event or [[market-regime-transition|regime shift]] is anticipated, LPs face a critical decision: stay deployed to earn potential future fees or withdraw to avoid expected [[loss-versus-rebalancing|LVR]] and other costs. This decision is not isolated; if many LPs withdraw, the remaining liquidity becomes thin, making it riskier for those who stay. This interdependence can lead to "coordination games" where the best action for one LP depends on what others are expected to do.
## Mechanism / math
Providers choose between remaining deployed and continuing to earn fees, or withdrawing early to avoid expected LVR and potentially redeploying later.

Suppose provider $i$ withdraws at time $t$. Its payoff is:
$$
U_i^{\text{withdraw}} = F_i^{\text{accrued}} - K_i^{\text{exit}} + V_i^{\text{redeploy}}
$$
Where:
*   $F_i^{\text{accrued}}$: Fees accrued up to withdrawal.
*   $K_i^{\text{exit}}$: Costs associated with exiting the position.
*   $V_i^{\text{redeploy}}$: Expected value from redeploying capital after withdrawal.

Remaining deployed yields:
$$
U_i^{\text{stay}} = F_i^{\text{future}} - \operatorname{LVR}_i^{\text{future}} - \operatorname{hedge/funding}_i
$$
Where:
*   $F_i^{\text{future}}$: Expected future fees.
*   $\operatorname{LVR}_i^{\text{future}}$: Expected future [[loss-versus-rebalancing|LVR]].
*   $\operatorname{hedge/funding}_i$: Expected future hedging and funding costs.

The withdrawal threshold is met when the expected costs of staying outweigh the expected benefits:
$$
\mathbb{E}[\operatorname{LVR}_i^{\text{future}} + \operatorname{funding}_i + K_i^{\text{exit}}] > \mathbb{E}[F_i^{\text{future}} + V_i^{\text{redeploy}}]
$$
## Why Multiple Equilibria Are Possible
This scenario can be a coordination game:
*   **If most LPs stay:** Liquidity remains deep, and fee income might justify staying, creating a stable equilibrium.
*   **If most LPs withdraw:** Remaining liquidity becomes thin and highly exposed to toxic arbitrage, making withdrawal more attractive for those still deployed. This can lead to a "run" dynamic and a stable defensive equilibrium where everyone withdraws.

This means an LP's optimal strategy may depend not only on market conditions but also on the expected behavior of other providers.
## Practical Policy
A CL provider could implement a two-stage trigger for withdrawal:
1.  **Private trigger:** Withdraw when its own expected net payoff (considering LVR, fees, costs) turns negative.
2.  **Market trigger:** Withdraw earlier when off-chain signals like [[gamma-exposure-gex|GEX]], volatility, or velocity imply that other LPs are likely to withdraw, anticipating a collective shift in liquidity. This avoids waiting for the on-chain price to fully move through the range.
## Where it matters
This concept is crucial for developing robust [[cl-exit-strategy|LP exit strategies]] and managing risk during periods of high [[market-regime-transition|market regime transition]] probability. It underscores the importance of monitoring competitor behavior and market-wide signals like [[gamma-exposure-gex|GEX]] to make timely and strategic withdrawal decisions.
## Related
[[nash-equilibrium-cl-strategies]], [[cl-provider-strategy]], [[cl-exit-strategy]], [[market-regime-transition]], [[gamma-exposure-gex]], [[loss-versus-rebalancing]], [[dlmm-2026-nash-equilibrium-cl-provider-strategies]]