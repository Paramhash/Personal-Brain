---
tags: ["api", "tastyworks", "use-cases", "portfolio-monitoring", "trading"]
created: 2024-05-15
reviewed: false
source_origin: "balances-and-positions.md"
---
# Tastyworks Balances and Positions API Use Cases

The [[../entities/tastyworks-balances-positions-api.md|Tastyworks Balances and Positions API]] is a versatile tool for developers building applications that interact with Tastyworks accounts. Here are some common use cases:

## Portfolio Dashboard
*   **Objective:** Display an account's current financial health and holdings.
*   **Endpoints:**
    *   `GET /accounts/{account_number}/balances` for headline numbers like `net-liquidating-value`, `cash-balance`, and `equity-buying-power`.
    *   `GET /accounts/{account_number}/positions` for a detailed table of current holdings.

## Pre-Trade Buying Power Check
*   **Objective:** Verify if an account has sufficient funds or margin before submitting a new order.
*   **Endpoints:**
    *   `GET /accounts/{account_number}/balances` to check specific buying power fields:
        *   `derivative-buying-power` for options trades.
        *   `equity-buying-power` for stock purchases.
        *   `day-trading-buying-power` for intraday trades (especially relevant for Pattern Day Trader accounts).

## Margin Monitoring
*   **Objective:** Keep track of an account's margin status to avoid or manage margin calls.
*   **Endpoints:**
    *   `GET /accounts/{account_number}/balances` to monitor:
        *   `maintenance-excess`: A negative value indicates a margin call.
        *   `maintenance-call-value`, `reg-t-call-value`, and `day-equity-call-value` for specific types and amounts of margin calls.

## Position-Level Profit & Loss (P&L)
*   **Objective:** Calculate unrealized and realized P&L for individual positions.
*   **Endpoints:**
    *   `GET /accounts/{account_number}/positions` provides:
        *   `average-open-price` and `mark-price` to calculate unrealized P&L per unit.
        *   `realized-day-gain` and `realized-today` for intraday realized gains/losses.

## Historical Performance Tracking
*   **Objective:** Chart account value and other metrics over time.
*   **Endpoints:**
    *   `GET /accounts/{account_number}/balance-snapshots` with `start-date` and `end-date` query parameters to retrieve historical account balance data.

## Filtering Positions
*   **Objective:** Display specific types of positions or positions related to a particular underlying asset.
*   **Endpoints:**
    *   `GET /accounts/{account_number}/positions` with query parameters:
        *   `instrument-type=Equity` to retrieve only stock positions.
        *   `underlying-symbol=AAPL` to get all positions (stock + options) for Apple.

## Options Expiration Awareness
*   **Objective:** Identify options and futures positions that are approaching their expiration date.
*   **Endpoints:**
    *   `GET /accounts/{account_number}/positions` provides the `expires-at` field for option and futures contracts.

---
## Related Concepts
*   [[../entities/tastyworks-balances-positions-api.md|Tastyworks Balances and Positions API]]
*   [[tastyworks-api-notes.md|Tastyworks Balances and Positions API Important Notes]]