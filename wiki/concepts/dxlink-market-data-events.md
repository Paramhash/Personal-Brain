---
tags: ["market-data", "streaming", "dxlink", "events", "api"]
created: 2024-07-30
reviewed: false
source_origin: "streaming-market-data.md"
---
# DXLink Market Data Events

[[../entities/dxlink.md|DXLink]] provides various market data events, each with its own specific schema, accessible via tastytrade's API quote token. When subscribing to data, clients must specify which event types they wish to receive.

The market data events accessible through tastytrade's API quote token include:

*   **Profile**: Provides descriptive and status information about an instrument (e.g., `description`, `shortSaleRestriction`, `tradingStatus`, `high52WeekPrice`, `low52WeekPrice`).
*   **Quote**: Delivers real-time bid and ask prices and sizes (e.g., `bidPrice`, `askPrice`, `bidSize`, `askSize`).
*   **Summary**: Offers aggregated daily statistics for an instrument (e.g., `openInterest`, `dayOpenPrice`, `dayHighPrice`, `dayLowPrice`, `prevDayClosePrice`).
*   **Trade**: Reports individual trade executions (e.g., `price`, `dayVolume`, `size`).
*   **Greeks**: Provides option Greeks values (e.g., `volatility`, `delta`, `gamma`, `theta`, `rho`, `vega`).
*   **TimeAndSale**: Detailed record of individual trades, often including timestamp, price, and size.

For a comprehensive overview of each event type and its full schema, refer to the official [[../entities/dxlink.md|DXLink protocol documentation]]. When configuring a feed using the [[../concepts/dxlink-websocket-protocol.md|DXLink WebSocket Protocol]], specific fields for each event type can be requested to optimize data transfer.

## Related Concepts

*   [[../concepts/streaming-market-data.md|Streaming Market Data (tastytrade & DXLink)]]
*   [[../entities/dxlink.md|DXLink]]
*   [[../concepts/dxlink-websocket-protocol.md|DXLink WebSocket Protocol]]
*   [[../concepts/candle-events-historic-data.md|Candle Events (DXLink Historic Data)]]