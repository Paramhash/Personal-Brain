---
tags: ["Data Feed", "Stock Data", "Real-time Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Nasdaq Basic

Nasdaq Basic is a data feed that provides real-time stock data. It is often referenced in the Theta Data v3 API for endpoints requiring real-time or near real-time information, particularly for users with higher [Subscription Tiers](../../concepts/subscription-tiers.md) (Standard or Pro).

## Usage in Theta Data v3:
*   **Stock Snapshot OHLC**: Returns real-time session OHLC.
*   **Stock Snapshot Trade**: Returns real-time last trade.
*   **Stock Snapshot Quote**: Returns real-time last BBO quote.
*   **Stock Snapshot Market Value**: Returns real-time market value derived from the last BBO quote.
*   **Stock History OHLC**: Can access current-day real-time historic data.
*   **Stock History Trade**: Can access current-day real-time historic data.
*   **Stock History Trade Quote**: Can access current-day real-time historic data.
*   **Stock At-Time Trade**: Returns real-time session.
*   **Stock At-Time Quote**: Returns real-time last BBO quote.

## Related Concepts:
*   [Data Feeds](../../concepts/data-feeds.md)
*   [Exchanges](../../concepts/exchanges.md)
*   [Stock Data](../../concepts/stock-data.md)
*   [API Parameters](../../concepts/api-parameters.md) (specifically `venue`)

---