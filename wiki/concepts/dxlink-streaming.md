---
tags: ["market-data", "streaming", "websocket", "dxfeed", "tastyworks", "real-time"]
created: 2023-10-27
reviewed: false
source_origin: "accounts-and-customers.md"
---
# DXLink Market Data Streaming

DXLink is the WebSocket-based real-time market data streamer utilized by Tastyworks to deliver live quotes and other market information to clients. It is powered by dxFeed, a leading provider of financial market data solutions.

## Purpose

The primary purpose of DXLink streaming is to provide low-latency, real-time market data, enabling users to monitor price movements, order book changes, and other critical trading information as it happens. This is essential for active traders and applications requiring up-to-the-second data.

## Connection Details

To connect to the DXLink streamer, an application needs two key pieces of information:

1.  **WebSocket URL:** The endpoint for the DXLink WebSocket server.
2.  **Authentication Token:** A temporary token to authorize the connection and identify the customer's market data entitlements.

These details are obtained by calling the [[../concepts/api-quote-tokens.md]] endpoint of the Tastyworks Accounts and Customers API. The response from this endpoint provides the `dxlink-url` (or `websocket-url`) and the `token`.

## Market Data Entitlement Levels

The `level` field returned by the `Get API Quote Tokens` endpoint indicates the customer's market data entitlement. This level determines the depth, speed, and types of data the customer is authorized to receive (e.g., "live" for real-time, "delayed" for delayed data). This is often tied to a customer's subscription or professional status, which can be checked via the [[../concepts/customer-profile.md]] `is-professional` and `has-delayed-quotes` fields.

## Token Refresh

DXLink authentication tokens have an expiration time (`expires-at`). To maintain a continuous stream of market data, applications must monitor the token's expiration and proactively request a new token from the [[../concepts/api-quote-tokens.md]] endpoint before the current one expires.

---