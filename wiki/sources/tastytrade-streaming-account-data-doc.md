---
tags: ["source", "tastytrade", "api", "documentation", "websocket"]
created: 2023-10-27
reviewed: false
source_origin: "streaming-account-data.md"
---
# tastytrade Streaming Account Data Documentation

This document serves as the primary source of information regarding the **tastytrade Account Streamer**, a websocket-based system for real-time notifications within the [[../entities/tastytrade-api.md|tastytrade API]].

## Overview

The documentation details how to utilize the Account Streamer to receive one-directional notifications about state changes to account data (orders, balances, positions) and non-account data (public watchlists, quote alert triggers). It highlights the benefits of real-time updates over traditional polling methods.

## Key Sections Covered

*   **Getting Started**: Outlines the sequential steps for initiating and maintaining a streamer connection, including opening a websocket, subscribing to notifications, and sending heartbeats.
*   **Available Actions**: Lists and describes the various subscription actions (e.g., `connect`, `heartbeat`, `public-watchlists-subscribe`, `quote-alerts-subscribe`) that clients can use to specify the types of notifications they wish to receive.
*   **Receiving Notifications**: Explains the common JSON structure of messages received from the streamer, emphasizing the `type` and `data` keys and the principle of full object representation.
*   **Notification Nuances**: Provides specific details on how order fill notifications are handled, particularly for multi-leg option orders and granular fill reporting.
*   **Hosts**: Specifies the websocket host URLs for both sandbox and production environments.
*   **Demo**: References an available demo page for testing sandbox account data subscriptions.

## Related Concepts

This source document is foundational for understanding:
*   [[../concepts/tastytrade-account-streamer.md|tastytrade Account Streamer]]
*   [[../concepts/tastytrade-streamer-connection-management.md|tastytrade Streamer Connection Management]]
*   [[../concepts/tastytrade-streamer-subscription-actions.md|tastytrade Streamer Subscription Actions]]
*   [[../concepts/tastytrade-streamer-notification-structure.md|tastytrade Streamer Notification Structure]]
*   [[../concepts/tastytrade-order-fill-processing-nuances.md|tastytrade Order Fill Processing Nuances]]

---
*Original Payload File: `streaming-account-data.md`*