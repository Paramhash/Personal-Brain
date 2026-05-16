---
tags: ["technology", "networking", "data-streaming", "api"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# WebSockets

WebSockets are a communication protocol that provides full-duplex communication channels over a single TCP connection. Unlike traditional HTTP, which is request-response based, WebSockets allow for persistent, bi-directional communication between a client and a server.

## Key Features

*   **Full-Duplex Communication:** Both client and server can send data to each other simultaneously.
*   **Persistent Connection:** Once established, the connection remains open, eliminating the overhead of repeatedly establishing new connections.
*   **Low Latency:** Reduces latency by avoiding HTTP headers and connection setup for each message.
*   **Real-time Data Streaming:** Ideal for applications requiring real-time updates, such as live chat, gaming, and financial market data.

## Applications in Finance

In financial technology, WebSockets are widely used for:
*   **Real-time Market Data:** Streaming live stock prices, options quotes, and trade data.
*   **[Options Greeks](../concepts/options-greeks.md) Feeds:** Delivering real-time Greek values.
*   **Order Book Updates:** Providing instant updates on bid and ask depths.
*   **Trading APIs:** Enabling low-latency interaction with brokerage platforms.

## Data Providers

Many modern [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md), including [Polygon.io](../entities/polygon-io.md), leverage WebSockets to deliver high-bandwidth, low-latency market data streams, such as the entire [Options Tape](../concepts/options-tape.md). This contrasts with older, often "clunkier" APIs that might rely on polling or less efficient protocols, like the [Interactive Brokers (IBKR) API](../entities/interactive-brokers-api.md).

---