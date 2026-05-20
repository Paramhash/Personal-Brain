---
tags: ["api", "backtesting", "trading-strategy", "historical-data", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# API Backtesting (tastytrade)

The [[../entities/tastytrade-open-api.md|tastytrade Open API]] offers dedicated endpoints for running historical options strategy backtests. This functionality allows users to evaluate the performance of trading strategies against past market data.

## Backtesting Endpoints
*   **`GET /available-dates`**: Retrieve dates for which historical data is available for backtesting.
*   **`POST /backtests`**: Initiate a new backtest for a specified options strategy.
*   **`GET /backtests/{id}`**: Retrieve the results of a previously initiated backtest using its unique ID.
*   **`POST /backtests/{id}/cancel`**: Cancel a running backtest.
*   **`GET /backtests/{id}/logs`**: Access logs related to a specific backtest.
*   **`POST /simulate-trade`**: Obtain historical pricing for a simulated trade, useful for granular analysis.

These tools enable quantitative traders and strategists to refine their approaches by understanding how their strategies would have performed under various historical market conditions.

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]