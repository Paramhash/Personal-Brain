---
domain: "derivatives"
tags: [stochastic-models, market-dynamics, financial-modeling, hidden-markov-model]
created: 2024-07-30
reviewed: false
source_origin: "090770552.pdf"
---
# Regime Switching Model (Financial)

## Definition
A regime switching model in finance is a class of statistical models that allows the parameters of a financial time series (e.g., asset prices, volatility) to change over time, switching between a finite number of distinct "regimes" or states. These regimes typically represent different underlying market conditions, such as bull markets, bear markets, high volatility, or low volatility. The transitions between these regimes are often governed by an unobservable [[Markov Chain]].

## Context from Source
In "Trend Following Trading under a Regime Switching Model" by Dai, Zhang, and Zhu (2010), a regime switching model is central to defining an optimal [[Trend Following Trading]] strategy.
- **Market Dynamics**: The stock price dynamics are modeled as a [[Geometric Brownian Motion]] where the drift (expected return rate) switches between two regimes: a bull market (up trend) and a bear market (down trend).
- **Unobservable Regimes**: The exact switching times between these market trends are not directly observable in real markets. This unobservable nature is a key challenge addressed by the model.
- **Conditional Probability**: To handle the unobservable regimes, the authors use the [[Wonham Filter]] to estimate the conditional probability of the market being in a specific regime (e.g., a bull market) given the available historical stock prices. This conditional probability then serves as the basis for making trading decisions.
- **Thresholds**: The optimal buying and selling times are determined by comparing this conditional probability against two time-dependent threshold curves, which are derived from solving a [[Double Obstacle Problem (Finance)]].

This approach provides a theoretical justification for trend following by explicitly modeling the changing market environment and deriving optimal actions based on the likelihood of current market conditions.

## Related Concepts
- [[Trend Following Trading]]
- [[Optimal Stopping Time (Finance)]]
- [[Wonham Filter]]
- [[Markov Chain]]
- [[Geometric Brownian Motion]]
- [[Double Obstacle Problem (Finance)]]
- [[Bull Market]]
- [[Bear Market]]

## Related Research
- [[Optimal Trend Following Strategy under Regime Switching]]
---