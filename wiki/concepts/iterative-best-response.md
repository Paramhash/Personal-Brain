---
domain: cl-market-making
tags:
- game-theory
- cl-market-making
- strategy
- simulation
- dlmm
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-02-nash-equilibrium-cl-provider-strategies.md
ingest_hashes:
- adeae1dccc964d66
---
# Iterative Best Response
**In one line:** An algorithm used in game theory to approximate a Nash equilibrium by iteratively updating each player's strategy to their best response, assuming other players' strategies are fixed, until no player can significantly improve their payoff.
## Intuition
The iterative best response method simulates how rational players might adjust their strategies in a game. It models a process where players react sequentially to the current strategies of their opponents, always choosing the action that maximizes their own payoff given what everyone else is doing. This process continues until a stable point is reached where no player has an incentive to unilaterally change their strategy, which is an approximate [[nash-equilibrium-cl-strategies|Nash equilibrium]].
## Mechanism / math
The recommended implementation for analyzing [[nash-equilibrium-cl-strategies]] in CL market making involves the following steps:

1.  **Initialization:** Start with an initial set of strategies for all simulated providers.
2.  **Iteration:** For each provider $i$:
    *   Hold the strategies of all other providers ($s_{-i}$) fixed.
    *   Find provider $i$'s highest-payoff alternative strategy ($s_i'$) by evaluating its [[cl-payoff-function|payoff]] across a range of possible actions.
    *   If the improvement from $s_i$ to $s_i'$ exceeds a predefined tolerance, replace provider $i$'s current strategy with $s_i'$.
3.  **Convergence:** Repeat step 2 for all providers until no provider can materially improve its payoff by unilaterally changing its strategy.

Each provider's strategy includes:
*   Range
*   Capital
*   Liquidity shape
*   Hedge policy
*   Withdrawal threshold

The payoff calculation for each strategy considers:
*   Fees
*   [[loss-versus-rebalancing|LVR]]
*   Funding costs
*   [[slippage|Slippage]]
*   Rent
*   Gas fees
*   Redeployment costs
## Where it matters
[[iterative-best-response|Iterative best response]] is a practical method for simulating and analyzing [[nash-equilibrium-cl-strategies]] in complex environments like [[concentrated-liquidity]] market making. It is particularly useful as an offline research tool to validate candidate [[cl-provider-strategy|strategies]] against archived market data using a [[research-simulator|research simulator]]. This allows for testing the robustness of strategies under competitive conditions without live deployment.
## Evidence and limits
This method provides an approximation of a Nash equilibrium. It may not always converge, especially in games with complex payoff landscapes or multiple equilibria. The quality of the approximation depends on the chosen tolerance and the thoroughness of the search for each provider's best response.
## Related
[[nash-equilibrium-cl-strategies]], [[cl-provider-strategy]], [[backtesting]], [[research-simulator]], [[dlmm-2026-nash-equilibrium-cl-provider-strategies]]