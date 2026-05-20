---
tags: ["api", "trading-platform", "options-trading", "tastyworks", "financial-technology"]
created: 2023-10-27
reviewed: false
source_origin: "backtesting.md"
---
# Tastyworks Backtesting API

The Tastyworks Backtesting API provides programmatic access to run historical backtests of options strategies. It allows users to create, monitor, retrieve results from, and simulate historical trade pricing for strategies. This API is a key tool for traders and developers looking to evaluate and validate their options trading strategies against historical market data available through the Tastyworks platform.

## API Details

*   **Base URL:** `https://api.tastyworks.com`
*   **Authentication:** Requires a valid session token passed via the `Authorization` header.
*   **API Version:** 1.0.0
*   **Scope:** All backtests created via this API are tied to the authenticated user, not to a specific trading account.

## Endpoints

### Get Available Dates
`GET /available-dates`
Returns the available historical date ranges for each symbol, which is crucial for determining valid backtesting periods.

### Get All Backtests
`GET /backtests`
Retrieves the identifiers (IDs) of all backtests previously created by the current user.

### Create Backtest
`POST /backtests`
Initiates a new backtest. The request body requires strategy configuration, including the underlying symbol, desired date range, entry/exit rules, and position sizing parameters. Returns the created backtest object with its ID.

### Get Backtest by ID
`GET /backtests/{id}`
Retrieves the full results, current status, and original parameters of a specific backtest using its unique ID.

### Cancel Backtest
`POST /backtests/{id}/cancel`
Cancels a backtest that is currently running, identified by its ID.

### Get Backtest Logs
`GET /backtests/{id}/logs`
Provides execution logs for a specified backtest, which can be invaluable for debugging or understanding the step-by-step execution flow.

### Simulate Trade
`POST /simulate-trade`
Returns historical prices for a hypothetical trade. This endpoint allows for quick, one-off historical price lookups without the overhead of running a full backtest.

## Important Notes

*   **User-scoped:** Backtests are inherently tied to the authenticated user's profile, not to any specific trading account within Tastyworks.
*   **Asynchronous execution:** Backtests, especially complex ones or those covering long periods, may take time to complete. The `Create Backtest` endpoint returns an ID immediately, and users should poll the `Get Backtest by ID` endpoint periodically to check its status and retrieve results.
*   **Schema limitations:** The official API swagger documentation may not always provide detailed request/response schemas. For comprehensive parameter details and examples, users are advised to refer to the `developer.tastytrade.com` documentation.

## Related Concepts

This API provides a concrete implementation for the general [[../concepts/backtesting.md|Backtesting]] methodology, specifically tailored for options strategies on the Tastyworks platform.