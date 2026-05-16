---
tags: ["finance", "trading", "strategies", "technical-analysis", "momentum", "mean-reversion"]
created: 2024-05-15
reviewed: false
source_origin: "/raw/tradingagent.md"
---
# Traditional Trading Strategies

## Description
**Traditional Trading Strategies** are established methods and algorithms used in financial markets to make investment decisions. These strategies often serve as benchmarks for evaluating the performance of new or advanced algorithmic trading systems, including those powered by [Large Language Models (LLMs)](../concepts/llms-in-finance.md). They typically fall into categories such as trend-following, mean reversion, or passive investment.

## Common Baseline Strategies
The following strategies are frequently used as baselines in financial trading research, as seen in the evaluation of the [TradingAgents](../entities/tradingagents.md) framework:

### 1. Buy and Hold
*   **Description**: A passive investment strategy where an investor purchases assets (e.g., stocks) and holds them for a long period, regardless of market fluctuations. The expectation is that the market will appreciate over time.
*   **Characteristics**: Minimal transaction costs, no active trading decisions.

### 2. MACD (Moving Average Convergence Divergence)
*   **Description**: A trend-following momentum indicator that shows the relationship between two moving averages of a security’s price. It generates buy and sell signals based on crossovers between the MACD line (difference between two exponential moving averages) and a signal line (exponential moving average of the MACD line).
*   **Type**: Trend-following, momentum.
*   **Relevance**: Often used by [Technical Analyst Agents](../concepts/technical-analyst-agent.md).

### 3. KDJ and RSI (Relative Strength Index)
*   **Description**: A momentum strategy combining two indicators:
    *   **KDJ (Stochastic Oscillator)**: Measures the momentum of price changes, identifying overbought and oversold conditions.
    *   **RSI (Relative Strength Index)**: Measures the speed and change of price movements, also identifying overbought and oversold conditions.
    *   Trading signals are generated when these indicators suggest extreme market conditions.
*   **Type**: Momentum, oscillator.
*   **Relevance**: Often used by [Technical Analyst Agents](../concepts/technical-analyst-agent.md).

### 4. ZMR (Zero Mean Reversion)
*   **Description**: A mean reversion trading strategy that generates signals based on price deviations from, and subsequent reversions to, a zero reference line (or a long-term average). The assumption is that prices will eventually revert to their historical mean.
*   **Type**: Mean reversion.

### 5. SMA (Simple Moving Average)
*   **Description**: A trend-following strategy that generates trading signals based on crossovers between short-term and long-term simple moving averages. A common signal is to buy when the short-term SMA crosses above the long-term SMA (golden cross) and sell when it crosses below (death cross).
*   **Type**: Trend-following.
*   **Relevance**: Often used by [Technical Analyst Agents](../concepts/technical-analyst-agent.md).

## Role as Baselines
These strategies provide a fundamental comparison point for evaluating the effectiveness of more complex algorithmic trading systems. By benchmarking against these established methods, researchers can demonstrate the incremental value and superior performance of novel approaches like [TradingAgents](../entities/tradingagents.md) across [financial trading evaluation metrics](../concepts/financial-trading-evaluation-metrics.md) such as cumulative return, Sharpe ratio, and maximum drawdown.

## Related Concepts
*   [TradingAgents](../entities/tradingagents.md)
*   [Technical Analyst Agent](../concepts/technical-analyst-agent.md)
*   [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md)
*   [LLMs in Finance](../concepts/llms-in-finance.md)

---