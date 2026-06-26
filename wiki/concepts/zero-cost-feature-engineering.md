---
tags: ["feature-engineering", "quantitative-finance", "machine-learning", "reinforcement-learning", "trading", "data-science"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Zero-Cost Feature Engineering

Zero-Cost Feature Engineering describes a methodology for creating a robust 5-feature stack for a [[../concepts/reinforcement-learning-agent.md]] designed to trade stocks within the [[../entities/nasdaq-100.md]] universe. This approach leverages only free End-of-Day (EOD) data, primarily sourced via [[../entities/yfinance.md]] and processed with [[../entities/pandas-ta.md]], to mathematically reconstruct proxies for more expensive options data (such as IV Skew, Put/Call Volume, and Term Structure).

This method demonstrates how to perform effective [[../concepts/feature-engineering.md]] without incurring data costs, making advanced quantitative strategies accessible.

## The 5-Feature Stack

The RL agent receives a (100, 5) cross-sectional array every month, where the 5 features are derived entirely from free EOD data:

1.  **[[../concepts/downside-semi-variance.md]]**: Replaces IV Skew to assess crash risk.
2.  **[[../concepts/chaikin-money-flow.md]] (CMF)**: Replaces Put/Call Volume to track equity capital flow.
3.  **[[../concepts/cross-sectional-momentum.md]]**: The core engine, identifying trending tech stocks.
4.  **[[../concepts/mean-reversion-stretch.md]]**: Replaces Term Structure to identify temporarily overextended stocks.
5.  **[[../concepts/stochastic-rsi.md]]**: A timing overlay for optimizing entry points.

## Execution Workflow

A simple Python script automates the process:
*   **Timing**: Runs at 4:00 PM EST on the last Friday of each month.
*   **Data Acquisition**: Calls `yfinance.download(tickers, period="6mo")` to pull free historical data for all 100 NDX stocks in a single, efficient network request (typically takes about 5 seconds).
*   **Feature Calculation**: Computes the five features listed above.
*   **Normalization**: [[../concepts/z-scoring.md]] is applied cross-sectionally to the features.
*   **Agent Input**: The resulting (100, 5) array is fed to the trained Micro Agent.
*   **Output**: The Agent generates a "Top 10" list of stocks based on its learned strategy.

This workflow ensures a consistent, automated, and cost-effective data pipeline for the RL trading agent.

---
### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].