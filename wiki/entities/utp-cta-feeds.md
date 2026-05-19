---
tags: ["Data Feed", "Stock Data", "Delayed Data", "Historical Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# UTP & CTA Feeds

The UTP (Unlisted Trading Privileges) and CTA (Consolidated Tape Association) feeds are primary sources for consolidated market data in the U.S. equities market. They provide comprehensive trade and quote information across various exchanges. In the context of the [Theta Data v3](../../entities/theta-data-v3.md) API, these feeds are used for 15-minute delayed stock data and historical data.

## Key Characteristics:
*   **Consolidated Data**: Merged feeds provide a comprehensive view of market activity.
*   **Delayed Data**: Typically provides 15-minute delayed data for certain [Subscription Tiers](../../concepts/subscription-tiers.md) (e.g., "value" subscription for stocks).
*   **Historical Data**: Serves as a source for extensive historical trade and quote data.
*   **EOD Reports**: Theta Data generates its own national End-of-Day (EOD) reports at 17:15 ET, as the equity SIPs (Securities Information Processors, which include UTP & CTA) only generate partial EOD reports.

## Usage in Theta Data v3:
*   **Stock Snapshot OHLC**: Returns 15-minute delayed session OHLC for "value" subscription.
*   **Stock Snapshot Quote**: Returns 15-minute delayed NBBO quote for "value" subscription.
*   **Stock Snapshot Market Value**: Returns 15-minute delayed market value for "value" subscription.
*   **Stock History OHLC**: Aggregated OHLC bars using SIP rules.
*   **Stock History Trade**: Returns every trade reported by UTP & CTA.
*   **Stock History Quote**: Returns every NBBO quote reported by UTP & CTA.
*   **Stock History Trade Quote**: Returns every trade paired with the last BBO quote reported by UTP or CTA.
*   **Stock At-Time Trade**: Returns 15-minute delayed session for "value" subscription, or historical last trade.
*   **Stock At-Time Quote**: Returns 15-minute delayed NBBO quote for "value" subscription, or historical last NBBO quote.

## Related Concepts:
*   [Data Feeds](../../concepts/data-feeds.md)
*   [Exchanges](../../concepts/exchanges.md)
*   [Stock Data](../../concepts/stock-data.md)
*   [API Parameters](../../concepts/api-parameters.md) (specifically `venue`)

---