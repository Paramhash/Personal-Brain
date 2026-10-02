---
domain: cl-market-making
tags:
- game-theory
- cl-market-making
- liquidity-concentration
- strategy
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-02-nash-equilibrium-cl-provider-strategies.md
ingest_hashes:
- e37d8e39e8bfb509
---
# Capital Allocation and Liquidity Shape in CL
**In one line:** The strategic decision by a concentrated liquidity provider (CLP) on how much capital to deploy and how to distribute that capital across different price bins within their chosen range.
## Intuition
Beyond simply choosing a price range, LPs must decide *where* within that range to concentrate their capital. This involves a trade-off: placing more liquidity in actively traded bins can yield higher fees, but also exposes the LP to greater adverse selection and competition from other providers. The "liquidity shape" describes this distribution.
## Mechanism / math
Let $L_i(b)$ be provider $i$'s liquidity in bin $b$. A provider faces:
*   Higher fee capture from bins near active trading flow.
*   Higher adverse-selection exposure in bins where informed arbitrage is strongest.
*   Diminishing fee returns as more providers crowd the same bins.

A simplified payoff for this game is:
$$
U_i = \sum_b F_i(b, L_i(b), L_{-i}(b)) - \sum_b \operatorname{LVR}_i(b) - K_i
$$
Where:
*   $F_i(b, L_i(b), L_{-i}(b))$: Fees earned by provider $i$ in bin $b$, dependent on its own liquidity $L_i(b)$ and the liquidity of all other providers $L_{-i}(b)$.
*   $\operatorname{LVR}_i(b)$: [[loss-versus-rebalancing|LVR]] incurred in bin $b$.
*   $K_i$: Total costs for provider $i$.

The equilibrium condition for an actively funded bin is approximately:
$$
\frac{\partial \text{fees}_i}{\partial L_i(b)} = \frac{\partial \text{LVR}_i}{\partial L_i(b)} + \frac{\partial \text{cost}_i}{\partial L_i(b)}
$$
This implies that liquidity should move to bins where the marginal fee return is greater than the marginal risk and operating cost.
## Practical Provider Policies
This framework suggests three useful policies for shaping liquidity:
*   **Flow-seeking:** Concentrate liquidity in bins where expected trading volume is high.
*   **Risk-aware:** Reduce liquidity in bins associated with high volatility or negative-gamma regimes, which increase adverse selection.
*   **Competition-aware:** Avoid bins where other providers have already created excessive depth, leading to diluted fee shares.
## Where it matters
This concept is crucial for optimizing [[cl-position|LP positions]] to maximize fee generation while effectively managing [[loss-versus-rebalancing]] and adverse selection. Market signals like [[gamma-exposure-gex|GEX walls]] can be strategically useful, indicating where future flow, arbitrage, or volatility concentration might make liquidity more or less valuable.
## Evidence and limits
The source proposes this as a use case for offline simulation, allowing for iterative allocation of liquidity among simulated providers. The marginal conditions are theoretical approximations.
## Related
[[nash-equilibrium-cl-strategies]], [[cl-provider-strategy]], [[liquidity-concentration]], [[bin-based-cl-dlmm]], [[fee-economics]], [[loss-versus-rebalancing]], [[gamma-exposure-gex]], [[dlmm-2026-nash-equilibrium-cl-provider-strategies]]