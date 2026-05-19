---
tags: ["Index", "Market Data", "Financial Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index Data

Index data refers to information about financial market indices, such as the S&P 500 (SPX). The [Theta Data v3](../../entities/theta-data-v3.md) API provides various endpoints to access real-time and historical data for indices.

## Key Characteristics:
*   **Symbols**: Indices are identified by unique [Symbols](../concepts/symbols.md).
*   **Price Reports**: [Exchanges](../../concepts/exchanges.md) typically generate price reports every second for popular indices.
*   **EOD Reports**: Theta Data generates its own national End-of-Day (EOD) reports for indices at 17:15 ET, as the underlying feeds do not provide a national EOD report for indices.

## Available Endpoints:

### List Endpoints:
*   **[Index List Symbols Endpoint](../concepts/index-list-symbols-endpoint.md)**: Returns all traded symbols for indices.
*   **[Index List Dates Endpoint](../concepts/index-list-dates-endpoint.md)**: Lists all available data dates for a given index symbol.

### Snapshot Endpoints (Real-time/Current Day):
*   **[Index Snapshot OHLC Endpoint](../concepts/index-snapshot-ohlc-endpoint.md)**: Retrieves the real-time current day Open, High, Low, Close (OHLC) for an index.
*   **[Index Snapshot Price Endpoint](../concepts/index-snapshot-price-endpoint.md)**: Retrieves a real-time last index price.
*   **[Index Snapshot Market Value Endpoint](../concepts/index-snapshot-market-value-endpoint.md)**: Retrieves a real-time last index market value.

### History Endpoints (Historical Data):
*   **[Index History EOD Endpoint](../concepts/index-history-eod-endpoint.md)**: Returns End-of-Day (EOD) reports for an index.
*   **[Index History OHLC Endpoint](../concepts/index-history-ohlc-endpoint.md)**: Provides aggregated historical OHLC bars for an index at specified [Time Intervals](../concepts/time-intervals.md).
*   **[Index History Price Endpoint](../concepts/index-history-price-endpoint.md)**: Retrieves historical index price reports, either as raw updates or at specified [Time Intervals](../concepts/time-intervals.md).

### At-Time Endpoints:
*   **[Index At-Time Price Endpoint](../concepts/index-at-time-price-endpoint.md)**: Retrieves historical index price reports at a specified millisecond of the day.

## Related Concepts:
*   [API Endpoints](../concepts/api-endpoints.md)
*   [API Parameters](../concepts/api-parameters.md)
*   [Data Formats](../concepts/data-formats.md)
*   [Time Intervals](../concepts/time-intervals.md)
*   [Subscription Tiers](../concepts/subscription-tiers.md)

---