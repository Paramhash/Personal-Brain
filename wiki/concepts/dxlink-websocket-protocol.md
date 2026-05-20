---
tags: ["websocket", "protocol", "market-data", "streaming", "dxlink"]
created: 2024-07-30
reviewed: false
source_origin: "streaming-market-data.md"
---
# DXLink WebSocket Protocol

Interacting with [[../entities/dxlink.md|DXLink]] for streaming market data involves a specific sequence of messages exchanged over a websocket connection. This protocol ensures proper setup, authentication, data subscription, and connection maintenance.

The general order of operations is:

1.  **SETUP**
2.  **AUTHORIZE**
3.  **CHANNEL_REQUEST**
4.  **FEED_SETUP**
5.  **FEED_SUBSCRIPTION**
6.  **KEEPALIVE** (ongoing)

## Detailed Steps and Example Messages

### 1. SETUP

This is the initial message sent to establish the connection.

*   **Sent**: `{"type":"SETUP","channel":0,"version":"0.1-DXF-JS/0.3.0","keepaliveTimeout":60,"acceptKeepaliveTimeout":60}`
*   **Received**: `{"type":"SETUP","channel":0,"keepaliveTimeout":60,"acceptKeepaliveTimeout":60,"version":"1.0-1.2.1-20240722-153442"}`

### 2. AUTHORIZE

After receiving an `AUTH_STATE` message with `state: UNAUTHORIZED`, the client sends the [[../concepts/api-quote-token.md|API Quote Token]] for authentication.

*   **Received**: `{"type":"AUTH_STATE","channel":0,"state":"UNAUTHORIZED"}`
*   **Sent**: `{"type":"AUTH","channel":0,"token":"<redacted>"}`
*   **Received**: `{"type":"AUTH_STATE","channel":0,"state":"AUTHORIZED","userId":"<redacted>"}`

### 3. CHANNEL_REQUEST

A channel is a virtual connection used to subscribe to different data streams (e.g., one for equities, another for futures). The `channel` number is client-defined.

*   **Sent**: `{"type":"CHANNEL_REQUEST","channel":3,"service":"FEED","parameters":{"contract":"AUTO"}}`
*   **Received**: `{"type":"CHANNEL_OPENED","channel":3,"service":"FEED","parameters":{"contract":"AUTO","subFormat":"LIST"}}`

### 4. FEED_SETUP

Once a channel is opened, configure the desired data fields for specific [[../concepts/dxlink-market-data-events.md|market data events]]. It is recommended to use the `COMPACT` data format.

*   **Sent**: `{"type":"FEED_SETUP","channel":3,"acceptAggregationPeriod":0.1,"acceptDataFormat":"COMPACT","acceptEventFields":{"Trade":["eventType","eventSymbol","price","dayVolume","size"],"TradeETH":["eventType","eventSymbol","price","dayVolume","size"],"Quote":["eventType","eventSymbol","bidPrice","askPrice","bidSize","askSize"],"Greeks":["eventType","eventSymbol","volatility","delta","gamma","theta","rho","vega"],"Profile":["eventType","eventSymbol","description","shortSaleRestriction","tradingStatus","statusReason","haltStartTime","haltEndTime","highLimitPrice","lowLimitPrice","high52WeekPrice","low52WeekPrice"],"Summary":["eventType","eventSymbol","openInterest","dayOpenPrice","dayHighPrice","dayLowPrice","prevDayClosePrice"]}}`
*   **Received**: `{"type":"FEED_CONFIG","channel":3,"dataFormat":"COMPACT","aggregationPeriod":0.1}`

### 5. FEED_SUBSCRIPTION

Subscribe to market event data for one or more symbols. DXLink will stream events until unsubscribed. Multiple events for multiple symbols can be added in a single message.

*   **Sent (Add)**: `{"type":"FEED_SUBSCRIPTION","channel":3,"reset":true,"add":[{"type":"Trade","symbol":"BTC/USD:CXTALP"},{"type":"Quote","symbol":"BTC/USD:CXTALP"},{"type":"Profile","symbol":"BTC/USD:CXTALP"},{"type":"Summary","symbol":"BTC/USD:CXTALP"},{"type":"Trade","symbol":"SPY"},{"type":"TradeETH","symbol":"SPY"},{"type":"Quote","symbol":"SPY"},{"type":"Profile","symbol":"SPY"},{"type":"Summary","symbol":"SPY"}]}`
*   **Received**: `{"type":"FEED_DATA","channel":3,"data":["Trade",["Trade","SPY",559.36,1.3743299E7,100.0,"Trade","BTC/USD:CXTALP",58356.71,"NaN","NaN"]]}`
*   **Sent (Remove)**: `{"type":"FEED_SUBSCRIPTION","channel":3,"remove":[{"type":"Trade","symbol":"SPY"},{"type":"Quote","symbol":"SPY"},{"type":"Summary","symbol":"SPY"}]}`

### 6. KEEPALIVE

To prevent the websocket connection from closing due to inactivity, a `KEEPALIVE` message must be sent at regular intervals (e.g., every 30 seconds, given a 60-second timeout).

*   **Sent**: `{"type":"KEEPALIVE","channel":0}`

## Related Concepts

*   [[../concepts/streaming-market-data.md|Streaming Market Data (tastytrade & DXLink)]]
*   [[../entities/dxlink.md|DXLink]]
*   [[../concepts/api-quote-token.md|API Quote Token (tastytrade)]]
*   [[../concepts/dxlink-market-data-events.md|DXLink Market Data Events]]