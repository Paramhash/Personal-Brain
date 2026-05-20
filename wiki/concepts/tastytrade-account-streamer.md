---
tags: ["tastytrade", "api", "websocket", "real-time", "notifications", "trading"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/tastytrade-streaming-account-data-doc.md"
---
# tastytrade Account Streamer

The **tastytrade Account Streamer** is a one-directional websocket utilized by the [[../entities/tastytrade-api.md|tastytrade API]] for publishing real-time notifications from the API layer to trading client applications. It serves as a mechanism to provide immediate updates on state changes, eliminating the need for clients to continuously poll API endpoints.

## Purpose
The primary purpose of the Account Streamer is to enable clients to subscribe to real-time updates for various types of data, including:
*   State changes to existing account data (e.g., [[../concepts/tastytrade-order-flow.md|orders]], balances, positions).
*   State changes to non-account data (e.g., public watchlists, quote alert triggers).

This approach significantly improves efficiency and responsiveness compared to traditional polling methods, where clients would repeatedly make HTTP requests to check for updates.

## How it Works
When a significant event occurs, such as an order status change from "Routed" to "Filled", the Account Streamer publishes a notification via the open websocket connection. Clients receive these messages instantly, allowing them to update their application state without delay.

For details on establishing and maintaining a connection, see [[./tastytrade-streamer-connection-management.md|tastytrade Streamer Connection Management]]. To understand the types of notifications available, refer to [[./tastytrade-streamer-subscription-actions.md|tastytrade Streamer Subscription Actions]]. The structure of these notifications is described in [[./tastytrade-streamer-notification-structure.md|tastytrade Streamer Notification Structure]]. Specific nuances regarding order fill processing are covered in [[./tastytrade-order-fill-processing-nuances.md|tastytrade Order Fill Processing Nuances]].

## Example
Consider an order submission:
1.  A client submits an order via an HTTP POST request. The initial response shows the order status as "Routed".
2.  Instead of repeatedly fetching the order status via GET requests, the client maintains a websocket connection to the Account Streamer.
3.  As the order's status changes (e.g., to "Live", then "Filled"), the Account Streamer automatically sends real-time notifications to the client, providing the updated order object.

This eliminates the need for continuous polling, simplifying client-side logic and reducing API call overhead.

---
*Source: [[../sources/tastytrade-streaming-account-data-doc.md|tastytrade Streaming Account Data Documentation]]*