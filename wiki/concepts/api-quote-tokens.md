---
tags: ["market-data", "api-endpoint", "tastyworks", "streaming", "authentication"]
created: 2023-10-27
reviewed: false
source_origin: "accounts-and-customers.md"
---
# API Quote Tokens (Tastyworks API)

The `Get API Quote Tokens` endpoint is crucial for establishing a real-time market data streaming connection with Tastyworks. It provides the necessary credentials and connection details for the [[../concepts/dxlink-streaming.md]] WebSocket streamer.

## Get API Quote Tokens Endpoint

Returns the DXLink streaming endpoint URL and authentication token needed to connect to the real-time market data WebSocket streamer.

**Request**

```
GET /api-quote-tokens
```

**Parameters:** None (uses the authenticated session to determine the customer's market data entitlements).

**Response** — `200 OK`

Returns a `QuoteStreamerTokenAuthResult` object.

| Field | Type | Description |
|-------|------|-------------|
| `token` | string | The authentication token to pass when connecting to the DXLink streamer |
| `dxlink-url` | string | The DXLink WebSocket URL to connect to for streaming market data |
| `websocket-url` | string | Alternative WebSocket URL for the streaming connection |
| `level` | string | The market data entitlement level for this customer (determines data depth and speed) |
| `issued-at` | datetime | Timestamp when the token was issued |
| `expires-at` | datetime | Timestamp when the token expires (tokens must be refreshed before expiry) |

**Example Response**

```json
{
  "data": {
    "token": "dGVzdF90b2tlbl9leGFtcGxl...",
    "dxlink-url": "wss://tasty-live-web.dxfeed.com/live/cometd",
    "websocket-url": "wss://tasty-live-web.dxfeed.com/live/cometd",
    "level": "live",
    "issued-at": "2026-04-09T12:00:00.000+00:00",
    "expires-at": "2026-04-09T13:00:00.000+00:00"
  }
}
```

### Usage

After successfully authenticating with the Tastyworks API, calling this endpoint is typically the next step to prepare for real-time market data consumption. The `token` and `dxlink-url` (or `websocket-url`) from the response are then used to establish a WebSocket connection to the DXLink streamer. It's important to note the `expires-at` timestamp, as tokens must be refreshed before they expire to maintain a continuous data stream.

This endpoint is a core component for integrating [[../concepts/dxlink-streaming.md]] into applications.

---