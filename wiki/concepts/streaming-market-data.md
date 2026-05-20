---
tags: ["market-data", "streaming", "websocket", "tastytrade", "dxlink"]
created: 2024-07-30
reviewed: false
source_origin: "streaming-market-data.md"
---
# Streaming Market Data (tastytrade & DXLink)

tastytrade supports streaming quote data asynchronously via websocket, primarily through integration with DXLink. This method allows clients to receive real-time market events as they occur. For synchronous quote data fetching, refer to the Market Data Guide.

The process for subscribing to streaming market events involves two main parts:

1.  **Obtain an API quote token**: This token authenticates the client with tastytrade's quote provider.
2.  **Fetch market events from DXLink**: Using the obtained API quote token, clients connect to and interact with the DXLink streamer.

## Important Considerations

*   **API Quote Token Expiration**: API quote tokens expire after 24 hours and must be refreshed.
*   **Market Event Frequency**: DXLink publishes market data events as they occur. Tickers with high trading volume will generate rapid changes and frequent events, while those with lower liquidity may see fewer events, potentially none for minutes or hours. This is normal behavior; if a websocket is connected and heartbeating but no messages are received, check the ticker's liquidity.

## Related Concepts

*   [[../concepts/api-quote-token.md|API Quote Token (tastytrade)]]
*   [[../entities/dxlink.md|DXLink]]
*   [[../concepts/dxlink-websocket-protocol.md|DXLink WebSocket Protocol]]
*   [[../concepts/dxlink-market-data-events.md|DXLink Market Data Events]]
*   [[../concepts/dxlink-symbology.md|DXLink Symbology]]
*   [[../concepts/candle-events-historic-data.md|Candle Events (DXLink Historic Data)]]