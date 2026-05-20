---
tags: ["api", "architecture", "web-services"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# REST API

A REST (Representational State Transfer) API is an architectural style for designing networked applications. It relies on a stateless, client-server communication model, typically using standard HTTP methods (GET, POST, PUT, DELETE) to interact with resources.

The [[Market Data API (Tastyworks)|Market Data API]] provided by [[Tastyworks]] is an example of a REST API, offering point-in-time data snapshots via HTTP requests.

## Key Characteristics
*   **Stateless:** Each request from client to server must contain all the information needed to understand the request.
*   **Client-Server:** Separation of concerns between the client (user interface) and the server (data storage).
*   **Cacheable:** Responses can be cached to improve performance.
*   **Layered System:** Intermediary servers (proxies, load balancers) can be placed between clients and servers.
*   **Uniform Interface:** Standardized methods and resource identification.

## Contrast with
*   [[WebSocket API]] (for streaming data)

## Related
*   [[Market Data API (Tastyworks)]]
*   [[API Authentication]]