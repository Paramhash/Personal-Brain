---
tags: ["tastytrade", "api", "websocket", "connection", "authentication", "heartbeat"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/tastytrade-streaming-account-data-doc.md"
---
# tastytrade Streamer Connection Management

Managing a connection to the [[./tastytrade-account-streamer.md|tastytrade Account Streamer]] involves a specific sequence of steps to ensure proper authentication and continuous real-time data flow.

## Connection Steps

At a high level, the following steps must be performed in order:

1.  **Open a Websocket Connection**: Establish a websocket connection to the appropriate back-end host.
2.  **Authenticate and Subscribe to Notifications**: Send a subscription message, including an authentication token, to specify the types of notifications desired.
3.  **Send Heartbeats**: Periodically send heartbeat messages to maintain the connection.

### 1. Open a Websocket Connection

Clients must open a websocket connection using their preferred programming language or library. The host URLs vary by environment:
*   **Sandbox**: `wss://streamer.cert.tastyworks.com`
*   **Production**: `wss://streamer.tastyworks.com`

**Example (Node.js with `ws` package):**
```javascript
const WebSocket = require('ws')
const host = 'wss://streamer.cert.tastyworks.com' // or production host
const websocket = new WebSocket(host)

websocket.addEventListener('open', () => {
  console.log('Websocket connection opened.')
  // Proceed to subscription and schedule heartbeats
})

websocket.addEventListener('message', (messageEvent) => {
  // Parse and process incoming notifications
  console.log('Received message:', messageEvent.data)
})

websocket.addEventListener('close', () => {
  console.log('Websocket connection closed.')
  // Handle reconnection logic
})

websocket.addEventListener('error', (error) => {
  console.error('Websocket error:', error)
})
```

### 2. Authenticate and Subscribe to Notifications

After opening the websocket, a subscription message must be sent. This message includes an `auth-token` (your tastytrade access token) and specifies the `action` to subscribe to. The `auth-token` must be prefixed with `'Bearer '`.

The most common subscription action is `connect`, which subscribes to all account-related updates for specified account numbers. For a full list of available actions, see [[./tastytrade-streamer-subscription-actions.md|tastytrade Streamer Subscription Actions]].

**Sample Connect Message:**
```json
{
  "action": "connect",
  "value": ["5WT00000","5WT00001"],
  "auth-token": "Bearer your_access_token_here",
  "request-id": 2
}
```

A successful `connect` message will typically receive a response like:
```json
{
  "status": "ok",
  "action": "connect",
  "web-socket-session-id": "5b6e2799",
  "value": [ "5WT00000", "5WT00001" ],
  "request-id": 2
}
```

**Important Note**: If subscription actions are not performed in the correct order (e.g., subscribing before the websocket is fully open), a "not implemented error" may occur. Heartbeats should only begin after a successful `connect` message.

### 3. Send Heartbeats

Once an active streamer connection is established and subscribed, clients must send periodic heartbeat messages to the tastytrade server. This ensures the websocket connection remains active and helps detect connection drops.

Heartbeats should be sent at regular intervals, typically between 2 seconds and 1 minute.

**Sample Heartbeat Message:**
```json
{
  "action": "heartbeat",
  "auth-token": "Bearer your_access_token_here",
  "request-id": 1
}
```
The `request-id` is optional but will be included in the server's response.

**Heartbeat Response Message:**
```json
{
  "status": "ok",
  "action": "heartbeat",
  "web-socket-session-id": "5b6e2799",
  "request-id": 1
}
```

---
*Source: [[../sources/tastytrade-streaming-account-data-doc.md|tastytrade Streaming Account Data Documentation]]*