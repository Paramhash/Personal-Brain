---
tags: ["api", "tastyworks", "trading", "portfolio-monitoring", "account-management"]
created: 2024-05-15
reviewed: false
source_origin: "balances-and-positions.md"
---
# Tastyworks Balances and Positions API

The Tastyworks Balances and Positions API provides a comprehensive set of endpoints for retrieving an account's current financial state, including cash balances, buying power, margin requirements, and open positions. This API is fundamental for applications requiring portfolio monitoring, pre-trade validation, and building account dashboards.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 0.0.1 (versioned as `20240501` or later for current field availability)

## Endpoints

### Get Account Balances
Retrieves the current balance values for an account across all currencies.
*   **Request:** `GET /accounts/{account_number}/balances`
*   **Path Parameters:** `account_number` (string, required)
*   **Response:** `200 OK` - Returns an array of [[./account-balance.md|AccountBalance]] objects.

### Get Account Balance by Currency
Retrieves the current balance values for an account in a specific currency.
*   **Request:** `GET /accounts/{account_number}/balances/{currency}`
*   **Path Parameters:** `account_number` (string, required), `currency` (string, required, e.g., `USD`)
*   **Response:** `200 OK` - Returns a single [[./account-balance.md|AccountBalance]] object.

### Get Balance Snapshots
Retrieves historical balance snapshots for an account, useful for tracking portfolio value over time. The most recent snapshot plus the current balance are returned by default.
*   **Request:** `GET /accounts/{account_number}/balance-snapshots`
*   **Path Parameters:** `account_number` (string, required)
*   **Query Parameters:** `snapshot-date`, `start-date`, `end-date` (string, date), `time-of-day` (string, e.g., `BOD`, `EOD`), `currency` (string), `page-offset` (integer), `per-page` (integer).
*   **Response:** `200 OK` - Returns an array of [[./account-balance-snapshot.md|AccountBalanceSnapshot]] objects.

### Get Account Positions
Retrieves the account's current open positions. Can be filtered by symbol, underlying symbol, or instrument type.
*   **Request:** `GET /accounts/{account_number}/positions`
*   **Path Parameters:** `account_number` (string, required)
*   **Query Parameters:** `symbol` (string), `underlying-symbol` (array), `instrument-type` (string, e.g., `Equity`, `Equity Option`), `include-closed-positions` (boolean), `include-marks` (boolean), `net-positions` (boolean), `underlying-product-code` (string), `partition-keys` (array).
*   **Response:** `200 OK` - Returns an array of [[./current-position.md|CurrentPosition]] objects.

For common ways to utilize these endpoints, refer to [[../concepts/tastyworks-api-use-cases.md|Tastyworks Balances and Positions API Use Cases]].
For important details regarding data handling and specific field interpretations, see [[../concepts/tastyworks-api-notes.md|Tastyworks Balances and Positions API Important Notes]].

---
## Related Data Models
*   [[./current-position.md|CurrentPosition]]
*   [[./account-balance.md|AccountBalance]]
*   [[./account-balance-snapshot.md|AccountBalanceSnapshot]]