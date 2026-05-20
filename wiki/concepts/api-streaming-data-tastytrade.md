---
tags: ["api", "streaming", "market-data", "account-data", "websocket", "real-time", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# Streaming Market and Account Data (tastytrade API)

The [[../entities/tastytrade-open-api.md|tastytrade Open API]] offers real-time data streaming capabilities for both market data and account updates via WebSocket connections.

## Streaming Market Data (DXLink WebSocket)
Real-time market data is streamed using the **DXLink WebSocket protocol**.
*   **API Quote Tokens**: Required for authentication, obtained via `GET /api-quote-tokens` and valid for 24 hours.
*   **Connection Protocol**: Involves a sequence of messages: `SETUP`, `AUTHORIZE`, `CHANNEL_REQUEST`, `FEED_SETUP`, `FEED_SUBSCRIPTION`, and `KEEPALIVE`.
*   **Event Types**: Supports various event types including `Profile`, `Quote`, `Summary`, `Trade`, `Greeks`, `TimeAndSale`, and `Candle` events for historical OHLC data.
*   **Symbology**: Uses a `streamer-symbol` field, which may differ from REST API symbology.
*   **Data Format**: Requires `COMPACT` data format.

## Streaming Account Data (WebSocket)
Real-time account event updates are streamed via a separate WebSocket connection.
*   **Connection Setup**: Involves opening a WebSocket, subscribing with an `auth-token`, and sending heartbeats (2s-1m intervals).
*   **Available Actions**: Includes `heartbeat`, `connect` (for account updates), `public-watchlists-subscribe`, and `quote-alerts-subscribe`.
*   **Notification Format**: Notifications include a `type`, the full data object, and a `timestamp`.
*   **Order Fill Nuances**: Specific handling for multi-leg order fill notifications.
*   **Hosts**:
    *   Sandbox: `wss://streamer.cert.tastyworks.com`
    *   Production: `wss://streamer.tastyworks.com`

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]