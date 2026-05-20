---
tags: ["tastytrade", "api", "websocket", "subscription", "actions", "notifications"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/tastytrade-streaming-account-data-doc.md"
---
# tastytrade Streamer Subscription Actions

The [[./tastytrade-account-streamer.md|tastytrade Account Streamer]] allows clients to subscribe to various types of real-time notifications by sending specific "action" messages over the websocket connection. Each subscription message follows a common schema.

## Subscription Message Schema

All subscription messages sent to the streamer server must adhere to the following JSON structure:

```json
{
  "action": "<action>",     // One of the available actions listed below
  "value": "<string|array>", // Optional. Depends on the specific action being sent
  "auth-token": "<string>", // Your tastytrade access token (prefixed with 'Bearer ')
  "request-id": "<number>"  // Optional. Included in server response if provided.
}
```

## Available Actions

Here are the primary actions available for subscription:

### `connect`
*   **Purpose**: Subscribes the client to all account-related notifications for specified account numbers. This includes updates for [[../concepts/tastytrade-order-flow.md|orders]], account balances, and positions.
*   **`value`**: An array of strings, where each string is an account number (e.g., `["5WT00000", "5WT00001"]`).
*   **Authentication**: Requires an `auth-token`.
*   **Usage**: Typically the first subscription action after opening the websocket connection.

### `heartbeat`
*   **Purpose**: Sent periodically by the client to the streamer server to prevent the socket connection from being considered "stale" and to detect connection drops.
*   **`value`**: Blank (not required).
*   **Authentication**: Requires an `auth-token`.
*   **Usage**: Heartbeat messages should be sent at regular intervals, typically between 2 seconds and 1 minute, after a successful `connect` message.

### `public-watchlists-subscribe`
*   **Purpose**: Subscribes the client to updates regarding public watchlists.
*   **`value`**: Blank (not required).
*   **Authentication**: Requires an `auth-token`, even though it subscribes to public data.

### `quote-alerts-subscribe`
*   **Purpose**: Subscribes the client to quote alert messages. These alerts are for configurations the user has previously set up via a POST request to the `/quote-alerts` endpoint of the [[../entities/tastytrade-api.md|tastytrade API]].
*   **`value`**: Blank (not required).
*   **Authentication**: Requires an `auth-token`.
*   **Important Note**: Quote alerts exist at a user level, not an account level.

For details on the overall connection process, refer to [[./tastytrade-streamer-connection-management.md|tastytrade Streamer Connection Management]].

---
*Source: [[../sources/tastytrade-streaming-account-data-doc.md|tastytrade Streaming Account Data Documentation]]*