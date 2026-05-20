---
tags: ["tastytrade", "api", "trading", "platform"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/tastytrade-streaming-account-data-doc.md"
---
# tastytrade API

The **tastytrade API** provides programmatic access to the tastytrade trading platform, allowing developers to integrate trading functionalities, account management, and real-time data into their applications. It supports various interactions, from submitting orders to retrieving account information.

## Key Components

A significant component of the tastytrade API is the [[../concepts/tastytrade-account-streamer.md|tastytrade Account Streamer]], which utilizes websockets to deliver real-time, one-directional notifications about account state changes, order updates, and other market events. This enables clients to receive immediate updates without the need for continuous polling.

## Authentication

Access to the tastytrade API, including the Account Streamer, requires authentication using an access token. This token is typically provided in the `Authorization` header for HTTP requests and within the `auth-token` field (prefixed with `Bearer `) for websocket messages.

## Functionality

The API generally supports:
*   Order submission and management.
*   Retrieval of account balances and positions.
*   Access to market data.
*   Real-time notifications via the Account Streamer.

---
*Source: [[../sources/tastytrade-streaming-account-data-doc.md|tastytrade Streaming Account Data Documentation]]*