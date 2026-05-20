---
tags: ["financial-modeling", "trading-strategies", "quantitative-finance", "risk-management"]
created: 2023-10-27
reviewed: false
source_origin: "backtesting.md"
---
# Backtesting

Backtesting is a method for evaluating the performance of a trading strategy or model using historical data. It involves applying a set of predefined rules (entry, exit, position sizing, etc.) to past market data to simulate how the strategy would have performed. This process helps traders and analysts assess the viability, profitability, and risk characteristics of a strategy before deploying it in live markets.

## Purpose

The primary purpose of backtesting is to:
*   **Validate strategies:** Determine if a strategy has a historical edge and if its underlying assumptions hold true across different market conditions.
*   **Optimize parameters:** Fine-tune strategy rules and parameters to potentially improve performance or reduce risk.
*   **Assess risk:** Understand potential drawdowns, volatility, and other risk metrics associated with the strategy.
*   **Build confidence:** Gain conviction in a strategy's robustness and suitability for real-world trading.

## Common Use Cases

*   **Strategy validation:** Evaluate how a specific options strategy (e.g., selling 30-delta puts at 45 DTE) would have performed historically across various market cycles.
*   **Date range discovery:** Confirm historical data availability for a target symbol and time period before committing to a full backtest.
*   **Quick price check:** Perform a one-off historical price lookup for a hypothetical trade without the overhead of running a complete backtest.
*   **Long-running backtests:** For complex strategies over extended time periods, initiate the backtest and monitor its progress asynchronously.

## Related Implementations

For a specific API implementation designed for backtesting options strategies, refer to the [[../entities/tastyworks-backtesting-api.md|Tastyworks Backtesting API]].