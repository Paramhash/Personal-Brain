---
tags: ["authentication", "api", "market-data", "streaming", "tastytrade"]
created: 2024-07-30
reviewed: false
source_origin: "streaming-market-data.md"
---
# API Quote Token (tastytrade)

The API quote token is a crucial component for accessing streaming market data from tastytrade's platform via DXLink. It serves to identify and authenticate the customer with tastytrade's quote provider.

## Obtaining the Token

Clients can obtain an API quote token by making a `GET` request to the `/api-quote-tokens` endpoint:

```http
GET /api-quote-tokens
```

The response will include the token, the DXLink websocket URL, and the access level:

```json
{
    "data": {
        "token": "<redacted>",
        "dxlink-url": "wss://tasty-openapi-ws.dxfeed.com/realtime",
        "level": "api"
    },
    "context": "/api-quote-tokens"
}
```

## Token Validity and Requirements

*   **Expiration**: API quote tokens are valid for 24 hours. After this period, a new token must be requested.
*   **Customer Status**: To successfully request an API quote token, the client must be a registered tastytrade customer with an open account. Requests from users who have only registered a username/password but not completed the account opening process will be rejected with a `quote_streamer.customer_not_found_error`.

## Usage

The `token` received from this endpoint is used in the `AUTHORIZE` step of the [[../concepts/dxlink-websocket-protocol.md|DXLink WebSocket Protocol]] to establish an authenticated connection for streaming market data. The `dxlink-url` provides the websocket endpoint for connecting to [[../entities/dxlink.md|DXLink]].

## Related Concepts

*   [[../concepts/streaming-market-data.md|Streaming Market Data (tastytrade & DXLink)]]
*   [[../entities/dxlink.md|DXLink]]
*   [[../concepts/dxlink-websocket-protocol.md|DXLink WebSocket Protocol]]