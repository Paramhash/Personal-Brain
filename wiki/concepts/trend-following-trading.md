---
domain: "derivatives"
tags: [trading-strategy, market-timing, momentum, financial-mathematics]
created: 2024-07-30
reviewed: false
source_origin: "090770552.pdf"
---
# Trend Following Trading

## Definition
Trend following trading is a speculative trading strategy that attempts to profit by analyzing the momentum of an asset's price in a particular direction. The core idea is to identify and exploit established trends: buying when prices are trending upwards (bull market) and selling (or shorting) when prices are trending downwards (bear market). Traders aim to "ride the trend" for as long as it persists and exit positions when the trend shows signs of reversal.

## Context from Source
In the paper "Trend Following Trading under a Regime Switching Model" by Dai, Zhang, and Zhu (2010), trend following is theoretically justified as an optimal trading strategy. The authors model market dynamics using a [[Regime Switching Model (Financial)]] where the market alternates between bull and bear phases.

The optimal trend following strategy is characterized by:
- **Identifying Regimes**: Using a [[Wonham Filter]], the conditional probability of the market being in a bull regime is estimated from observable stock prices.
- **Threshold-Based Decisions**: Optimal buying and selling decisions are made when this conditional probability crosses specific time-dependent thresholds. Buying occurs when the probability crosses an upper threshold from below, signaling an entry into a bull market. Selling occurs when it crosses a lower threshold from above, indicating a shift to a bear market.
- **Optimal Stopping**: The problem is formulated as an [[Optimal Stopping Time (Finance)]] problem to maximize the discounted expected return, taking into account [[Transaction Costs (Finance)]].

Numerical experiments and historical market tests on indices like [[NASDAQ]], [[S&P 500]], and [[Dow Jones Industrial Average (DJIA)]] demonstrate that this theoretically derived trend following strategy significantly outperforms a simple buy-and-hold strategy and exhibits robustness to parameter changes.

## Related Concepts
- [[Regime Switching Model (Financial)]]
- [[Optimal Stopping Time (Finance)]]
- [[Wonham Filter]]
- [[Bull Market]]
- [[Bear Market]]
- [[Transaction Costs (Finance)]]
- [[Buy and Hold Strategy]]

## Related Research
- [[Optimal Trend Following Strategy under Regime Switching]]
---