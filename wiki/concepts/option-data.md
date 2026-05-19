---
tags: ["Options", "Market Data", "Financial Data", "Derivatives"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Data

Option data refers to information about options contracts, which are financial derivatives that give the buyer the right, but not the obligation, to buy or sell an underlying asset at a specified strike price on or before a certain expiration date. The [Theta Data v3](../../entities/theta-data-v3.md) API provides extensive endpoints for accessing real-time and historical options data, including various [Option Greeks](../concepts/option-greeks.md).

## Key Characteristics:
*   **Underlying Assets**: Options are tied to an underlying asset, typically a [Stock Symbol](../concepts/symbols.md) or [Index Symbol](../concepts/symbols.md).
*   **[Expirations](../concepts/expirations.md)**: Each option contract has a specific expiration date.
*   **[Strike Prices](../concepts/strike-prices.md)**: The predetermined price at which the underlying asset can be bought or sold.
*   **Right**: Options are either "Call" (right to buy) or "Put" (right to sell).
*   **Data Source**: Primarily sourced from [OPRA (Options Price Reporting Authority)](../../entities/opra.md).
*   **EOD Reports**: Theta Data generates its own national End-of-Day (EOD) reports for options at 17:15 ET, as OPRA does not provide a national EOD report.
*   **Open Interest**: Reported around 06:30 ET every morning by OPRA, reflecting the open interest at the end of the previous trading day.

## Available Endpoints:

### List Endpoints:
*   **[Option List Symbols Endpoint](../concepts/option-list-symbols-endpoint.md)**: Returns all traded underlying symbols for options.
*   **[Option List Dates Endpoint](../concepts/option-list-dates-endpoint.md)**: Lists all available data dates for an option with a given symbol, request type, and expiration.
*   **[Option List Expirations Endpoint](../concepts/option-list-expirations-endpoint.md)**: Lists all available expiration dates for an option with a given symbol.
*   **[Option List Strikes Endpoint](../concepts/option-list-strikes-endpoint.md)**: Lists all available strike prices for an option with a given symbol and expiration date.
*   **[Option List Contracts Endpoint](../concepts/option-list-contracts-endpoint.md)**: Lists all contracts that were traded or quoted on a particular date, optionally filtered by symbol.

### Snapshot Endpoints (Real-time/Current Day):
*   **[Option Snapshot OHLC Endpoint](../concepts/option-snapshot-ohlc-endpoint.md)**: Retrieves a real-time last OHLC of an option contract.
*   **[Option Snapshot Trade Endpoint](../concepts/option-snapshot-trade-endpoint.md)**: Retrieves the real-time last trade of an option contract.
*   **[Option Snapshot Quote Endpoint](../concepts/option-snapshot-quote-endpoint.md)**: Retrieves a real-time last NBBO quote of an option contract.
*   **[Option Snapshot Open Interest Endpoint](../concepts/option-snapshot-open-interest-endpoint.md)**: Retrieves the last open interest message of an option contract.
*   **[Option Snapshot Market Value Endpoint](../concepts/option-snapshot-market-value-endpoint.md)**: Returns a real-time market value derived from the last NBBO quote of an option contract.
*   **[Option Snapshot Greeks Implied Volatility Endpoint](../concepts/option-snapshot-greeks-implied-volatility-endpoint.md)**: Returns implied volatilities calculated using the national best bid, mid, and ask price.
*   **[Option Snapshot Greeks All Endpoint](../concepts/option-snapshot-greeks-all-endpoint.md)**: Retrieves a real-time last Greeks calculation for all option contracts on a provided expiration.
*   **[Option Snapshot Greeks First Order Endpoint](../concepts/option-snapshot-greeks-first-order-endpoint.md)**: Retrieves real-time last first-order Greeks.
*   **[Option Snapshot Greeks Second Order Endpoint](../concepts/option-snapshot-greeks-second-order-endpoint.md)**: Retrieves real-time last second-order Greeks.
*   **[Option Snapshot Greeks Third Order Endpoint](../concepts/option-snapshot-greeks-third-order-endpoint.md)**: Retrieves real-time last third-order Greeks.

### History Endpoints (Historical Data):
*   **[Option History EOD Endpoint](../concepts/option-history-eod-endpoint.md)**: Returns End-of-Day (EOD) reports for an option contract.
*   **[Option History OHLC Endpoint](../concepts/option-history-ohlc-endpoint.md)**: Provides aggregated historical OHLC bars for an option contract at specified [Time Intervals](../concepts/time-intervals.md).
*   **[Option History Trade Endpoint](../concepts/option-history-trade-endpoint.md)**: Returns every trade reported by OPRA for an option contract.
*   **[Option History Quote Endpoint](../concepts/option-history-quote-endpoint.md)**: Returns every NBBO quote reported by OPRA for an option contract.
*   **[Option History Trade Quote Endpoint](../concepts/option-history-trade-quote-endpoint.md)**: Returns every trade reported by OPRA paired with the last NBBO quote at the time of trade.
*   **[Option History Open Interest Endpoint](../concepts/option-history-open-interest-endpoint.md)**: Returns historical open interest messages for an option contract.
*   **[Option History Greeks EOD Endpoint](../concepts/option-history-greeks-eod-endpoint.md)**: Returns End-of-Day Greeks calculations using closing option and underlying prices.
*   **[Option History Greeks All Endpoint](../concepts/option-history-greeks-all-endpoint.md)**: Returns historical Greeks calculations for all contracts on a provided expiration at specified [Time Intervals](../concepts/time-intervals.md).
*   **[Option History Greeks First Order Endpoint](../concepts/option-history-greeks-first-order-endpoint.md)**: Returns historical first-order Greeks.
*   **[Option History Greeks Second Order Endpoint](../concepts/option-history-greeks-second-order-endpoint.md)**: Returns historical second-order Greeks.
*   **[Option History Greeks Third Order Endpoint](../concepts/option-history-greeks-third-order-endpoint.md)**: Returns historical third-order Greeks.
*   **[Option History Trade Greeks All Endpoint](../concepts/option-history-trade-greeks-all-endpoint.md)**: Calculates all Greeks for every trade reported by OPRA.
*   **[Option History Trade Greeks First Order Endpoint](../concepts/option-history-trade-greeks-first-order-endpoint.md)**: Calculates first-order Greeks for every trade reported by OPRA.
*   **[Option History Trade Greeks Second Order Endpoint](../concepts/option-history-trade-greeks-second-order-endpoint.md)**: Calculates second-order Greeks for every trade reported by OPRA.
*   **[Option History Trade Greeks Third Order Endpoint](../concepts/option-history-trade-greeks-third-order-endpoint.md)**: Calculates third-order Greeks for every trade reported by OPRA.
*   **[Option History Greeks Implied Volatility Endpoint](../concepts/option-history-greeks-implied-volatility-endpoint.md)**: Returns historical implied volatilities calculated using bid, mid, and ask prices.
*   **[Option History Trade Greeks Implied Volatility Endpoint](../concepts/option-history-trade-greeks-implied-volatility-endpoint.md)**: Returns historical implied volatilities calculated using trade prices.

### At-Time Endpoints:
*   **[Option At-Time Trade Endpoint](../concepts/option-at-time-trade-endpoint.md)**: Returns the last trade reported by OPRA at a specified millisecond of the day.
*   **[Option At-Time Quote Endpoint](../concepts/option-at-time-quote-endpoint.md)**: Returns the last NBBO quote reported by OPRA at a specified millisecond of the day.

## Related Concepts:
*   [API Endpoints](../concepts/api-endpoints.md)
*   [API Parameters](../concepts/api-parameters.md)
*   [Data Formats](../concepts/data-formats.md)
*   [Time Intervals](../concepts/time-intervals.md)
*   [Subscription Tiers](../concepts/subscription-tiers.md)

---