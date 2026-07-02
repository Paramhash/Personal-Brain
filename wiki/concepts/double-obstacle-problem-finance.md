---
domain: "derivatives"
tags: [variational-inequalities, optimal-control, free-boundary-problems, financial-mathematics]
created: 2024-07-30
reviewed: false
source_origin: "090770552.pdf"
---
# Double Obstacle Problem (Finance)

## Definition
In mathematics, particularly in the study of partial differential equations and variational inequalities, a double obstacle problem involves finding a function that lies between two given "obstacle" functions. In finance, this type of problem often arises in optimal stopping or optimal control contexts, where decisions (like buying or selling an asset) are constrained by upper and lower bounds, or where the value function is bounded by certain thresholds. The solution typically involves identifying "free boundaries" that separate regions where the function is active (i.e., touching an obstacle) from regions where it satisfies a standard PDE.

## Context from Source
In "Trend Following Trading under a Regime Switching Model" by Dai, Zhang, and Zhu (2010), the [[Double Obstacle Problem (Finance)]] emerges as a crucial component in determining the optimal trading thresholds for a [[Trend Following Trading]] strategy.
- **Value Functions**: The authors define two optimal value functions, $V_0(S, p, t)$ and $V_1(S, p, t)$, corresponding to starting with a flat position (no stock) or a long position (one share of stock), respectively. These functions represent the maximum discounted expected return.
- **Variational Inequalities**: Using a dynamic programming approach, these value functions are shown to satisfy a system of two variational inequalities.
- **Difference Function**: A key insight is that the difference between these two value functions, $Z(p, t) = U_1(p, t) - U_0(p, t)$ (where $U_i = V_i/S$ are scaled value functions), satisfies a double obstacle problem. The "obstacles" are related to the transaction costs of buying and selling.
- **Threshold Determination**: The solution to this double obstacle problem yields the optimal time-dependent threshold curves for the conditional probability of being in a bull market ($p_t$). These thresholds define the "buying region" (BR), "selling region" (SR), and "no-trading region" (NT).

The conversion of the optimal stopping problem into a double obstacle problem simplifies the analysis and allows for the determination of the critical probabilities at which trading decisions should be made.

## Related Concepts
- [[Trend Following Trading]]
- [[Optimal Stopping Time (Finance)]]
- [[Regime Switching Model (Financial)]]
- [[Dynamic Programming (Finance)]]
- [[Variational Inequality (Mathematics)]]
- [[Free Boundary Problem]]
- [[Transaction Costs (Finance)]]

## Related Research
- [[Optimal Trend Following Strategy under Regime Switching]]
---