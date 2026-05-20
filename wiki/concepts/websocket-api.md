---
tags: ["api", "architecture", "streaming-data"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# WebSocket API

A WebSocket API provides a full-duplex communication channel over a single TCP connection. Unlike [[REST API]]s which are request-response based, WebSockets enable persistent, real-time, two-way communication between a client and a server.

This makes them ideal for applications requiring continuous data streams, such as live market data feeds.

## Use in Market Data
For real-time, continuous market data, [[Tastyworks]] offers the [[DXLink]] WebSocket streaming API as an alternative to its snapshot-based [[Market Data API (Tastyworks)|Market Data API]].

## Key Characteristics
*   **Full-Duplex:** Simultaneous two-way communication.
*   **Persistent Connection:** Maintains an open connection, reducing overhead compared to repeated HTTP requests.
*   **Low Latency:** Ideal for real-time applications.
*   **Event-Driven:** Data is pushed from the server to the client as it becomes available.

## Contrast with
*   [[REST API]] (for point-in-time data)

## Related
*   [[DXLink]]
*   [[Market Data API (Tastyworks)]]
*   [[Tastyworks]]