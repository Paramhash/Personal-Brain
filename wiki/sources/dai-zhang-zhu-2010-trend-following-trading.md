---
domain: "derivatives"
tags: [trend-following, regime-switching, optimal-stopping, financial-mathematics, stock-trading, market-models]
created: 2024-07-30
reviewed: false
source_origin: "090770552.pdf"
---
# Trend Following Trading under a Regime Switching Model

## Authors
- M. Dai
- Q. Zhang
- Q. J. Zhu

## Publication
- **Journal**: SIAM J. Financial Mathematics
- **Volume**: 1
- **Pages**: 780-810
- **Year**: 2010
- **DOI**: 10.1137/090770552

## Abstract
This paper investigates the optimality of a trend following trading rule. The core idea is to identify and capitalize on bull markets at their early stages, ride the trend, and liquidate positions at the first sign of a bear market. The authors mathematically characterize bull and bear market phases using conditional probabilities of the bull market given up-to-date stock prices. Optimal buying and selling times are determined by a sequence of stopping times, which are derived from two threshold curves. Numerical experiments are conducted to validate the theoretical results and demonstrate the strategy's performance in a marketplace.

## Key Takeaways
- **Theoretical Justification**: Provides a rigorous mathematical framework for trend following strategies using optimal stopping theory and a finite horizon regime switching model.
- **Regime Switching Model**: Stock price dynamics are modeled as a geometric Brownian motion with a drift that switches between bull and bear market regimes, represented by an unobservable Markov chain.
- **Wonham Filter Application**: The [[Wonham Filter]] is employed to estimate the conditional probability of being in a bull market, transforming the unobservable market trend problem into a completely observable one.
- **Optimal Trading Rules**: The strategy is characterized by two time-dependent thresholds for the conditional probability of a bull regime, signaling optimal buy and sell points.
- **Mathematical Tools**: Derivation involves dynamic programming, variational inequalities, and the solution of a double obstacle problem.
- **Empirical Validation**: Numerical experiments using simulated data and historical market data (NASDAQ, SP500, DJIA indices) demonstrate that the proposed trend following strategy significantly outperforms the traditional buy-and-hold strategy and is robust to parameter perturbations and transaction costs.
- **Transaction Costs**: The model incorporates fixed percentage transaction costs, showing that increasing costs expand the no-trading region and reduce trading frequency.

## Related Concepts
- [[Trend Following Trading]]
- [[Regime Switching Model (Financial)]]
- [[Optimal Stopping Time (Finance)]]
- [[Wonham Filter]]
- [[Dynamic Programming (Finance)]]
- [[Double Obstacle Problem (Finance)]]
- [[Geometric Brownian Motion]]
- [[Transaction Costs (Finance)]]

## Related Entities
- [[M. Dai]]
- [[Q. Zhang]]
- [[Q. J. Zhu]]
- [[NASDAQ]]
- [[S&P 500]]
- [[Dow Jones Industrial Average (DJIA)]]
---