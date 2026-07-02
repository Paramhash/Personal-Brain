---
domain: "derivatives"
tags: [stochastic-control, decision-theory, options-pricing, financial-mathematics]
created: 2024-07-30
reviewed: false
source_origin: "090770552.pdf"
---
# Optimal Stopping Time (Finance)

## Definition
In the context of stochastic control theory, an optimal stopping time is a rule or strategy that specifies the best moment to stop a stochastic process to maximize an expected reward or minimize an expected cost. In finance, this concept is widely applied to problems such as determining the optimal time to buy or sell an asset, exercise an American option, or liquidate a portfolio. The decision to stop is based on the current state of the process and the expected future evolution.

## Context from Source
The paper "Trend Following Trading under a Regime Switching Model" by Dai, Zhang, and Zhu (2010) frames the problem of optimal [[Trend Following Trading]] as an optimal stopping time problem.
- **Maximizing Reward**: The objective is to maximize a discounted expected return from trading a single share of stock, considering [[Transaction Costs (Finance)]].
- **Sequence of Stopping Times**: The model involves not just a single stopping time but a sequence of stopping times for both buying ($\tau_n$) and selling ($\upsilon_n$) operations, representing multiple trades over a finite horizon.
- **Unobservable Regimes**: A key challenge is that the underlying market regime (bull or bear) is unobservable. This is addressed by using the [[Wonham Filter]] to estimate the conditional probability of being in a bull market.
- **Thresholds**: The optimal buying and selling times are determined by comparing this conditional probability against two time-dependent threshold curves. These thresholds are derived from solving a system of variational inequalities, which leads to a [[Double Obstacle Problem (Finance)]].

The application of optimal stopping theory allows for a rigorous mathematical justification of trend following strategies, providing concrete rules for when to enter and exit positions based on market conditions and expected future returns.

## Related Concepts
- [[Trend Following Trading]]
- [[Regime Switching Model (Financial)]]
- [[Wonham Filter]]
- [[Dynamic Programming (Finance)]]
- [[Double Obstacle Problem (Finance)]]
- [[Transaction Costs (Finance)]]

## Related Research
- [[Optimal Trend Following Strategy under Regime Switching]]
---