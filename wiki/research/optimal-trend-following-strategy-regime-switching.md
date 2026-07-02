---
domain: "derivatives"
tags: [trend-following, regime-switching, optimal-stopping, financial-mathematics, market-timing, unobservable-states]
created: 2024-07-30
reviewed: false
source_origin: "090770552.pdf"
---
# Optimal Trend Following Strategy under Regime Switching

## Research Question
How can an optimal trend following trading rule be theoretically justified and practically implemented under a market regime switching model where the underlying market regimes (e.g., bull or bear) are unobservable? What are the optimal conditions for buying and selling, and how does such a strategy perform against traditional methods?

## Key Findings from Source
The paper "Trend Following Trading under a Regime Switching Model" by Dai, Zhang, and Zhu (2010) addresses this question by:
1.  **Theoretical Justification**: Providing a rigorous mathematical justification for [[Trend Following Trading]] as an [[Optimal Stopping Time (Finance)]] problem within a finite horizon [[Regime Switching Model (Financial)]].
2.  **Unobservable Regimes**: Acknowledging that market regimes (bull/bear) are unobservable, the authors employ the [[Wonham Filter]] to estimate the conditional probability of being in a bull market given historical stock prices. This transforms the problem into a fully observable one.
3.  **Optimal Thresholds**: The optimal buying and selling decisions are determined by two time-dependent threshold curves for this conditional probability. These thresholds are derived by solving a system of variational inequalities, which simplifies to a [[Double Obstacle Problem (Finance)]].
4.  **Strategy Characterization**: The optimal strategy involves buying when the conditional probability of a bull market crosses an upper threshold from below and selling when it crosses a lower threshold from above.
5.  **Robustness and Performance**:
    *   Numerical simulations demonstrate that the strategy significantly outperforms a simple buy-and-hold strategy.
    *   Tests on historical data for [[NASDAQ]], [[S&P 500]], and [[Dow Jones Industrial Average (DJIA)]] indices confirm this outperformance.
    *   The strategy is shown to be robust to perturbations in model parameters and effective even with transaction costs, although higher costs reduce trading frequency.
6.  **Practical Implementation**: The conditional probability can be obtained directly from actual historical stock price data through a differential equation, making the strategy implementable.

## Methods
-   **Stochastic Control Theory**: Framing the trading problem as an optimal stopping problem.
-   **Regime Switching Models**: Modeling market dynamics with unobservable bull and bear phases.
-   **Nonlinear Filtering**: Utilizing the Wonham filter to estimate hidden market states.
-   **Dynamic Programming**: Deriving value functions and associated Hamilton-Jacobi-Bellman (HJB) equations.
-   **Variational Inequalities & Double Obstacle Problems**: Solving for optimal trading thresholds.
-   **Numerical Methods**: Penalization method with finite difference discretization for solving the double obstacle problem.
-   **Empirical Analysis**: Conducting simulations and backtesting on historical market data.

## Related Concepts
- [[Trend Following Trading]]
- [[Regime Switching Model (Financial)]]
- [[Optimal Stopping Time (Finance)]]
- [[Wonham Filter]]
- [[Double Obstacle Problem (Finance)]]
- [[Transaction Costs (Finance)]]
- [[Dynamic Programming (Finance)]]

## Related Entities
- [[M. Dai]]
- [[Q. Zhang]]
- [[Q. J. Zhu]]
- [[NASDAQ]]
- [[S&P 500]]
- [[Dow Jones Industrial Average (DJIA)]]
---