---
domain: "derivatives"
tags: [nonlinear-filtering, stochastic-control, estimation-theory, hidden-markov-model]
created: 2024-07-30
reviewed: false
source_origin: "090770552.pdf"
---
# Wonham Filter

## Definition
The Wonham filter is a mathematical tool used in stochastic control and estimation theory for problems involving partially observable Markov processes. Specifically, it provides a way to compute the conditional probability distribution of an unobservable (hidden) finite-state [[Markov Chain]] given continuous observations of a related process. It transforms a problem with partial information into a problem with complete information by estimating the hidden state.

## Context from Source
In "Trend Following Trading under a Regime Switching Model" by Dai, Zhang, and Zhu (2010), the [[Wonham Filter]] plays a crucial role in making the [[Regime Switching Model (Financial)]] tractable for optimal trading decisions.
- **Unobservable Market Regimes**: The paper models stock price dynamics where the market's underlying regime (bull or bear) is an unobservable [[Markov Chain]]. This means traders cannot directly know if the market is currently in an uptrend or downtrend.
- **Converting to Observable Problem**: The Wonham filter is applied to convert this partially observable problem into a completely observable one. It calculates $p_r = P(a_r = 1 | S_r)$, which is the conditional probability of the market being in a bull regime ($a_r=1$) given the observed stock prices up to time $r$.
- **Stochastic Differential Equation (SDE)**: The paper shows that this conditional probability $p_r$ satisfies a specific [[Stochastic Differential Equation (SDE)]], which can then be used to track the likelihood of being in a bull market over time.
- **Informing Trading Decisions**: This estimated conditional probability $p_r$ then becomes the key state variable for determining optimal buying and selling thresholds in the [[Trend Following Trading]] strategy.

By using the Wonham filter, the authors are able to bridge the gap between theoretical models with hidden states and practical trading strategies that must rely on observable market data.

## Related Concepts
- [[Regime Switching Model (Financial)]]
- [[Markov Chain]]
- [[Stochastic Differential Equation (SDE)]]
- [[Trend Following Trading]]
- [[Optimal Stopping Time (Finance)]]

## Related Research
- [[Optimal Trend Following Strategy under Regime Switching]]
---