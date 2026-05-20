---
tags: ["tastytrade", "api", "websocket", "orders", "fills", "notifications", "multi-leg"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/tastytrade-streaming-account-data-doc.md"
---
# tastytrade Order Fill Processing Nuances

The [[./tastytrade-account-streamer.md|tastytrade Account Streamer]] provides detailed and timely notifications regarding order fills. Understanding the nuances of how these notifications are processed, especially for multi-leg orders, is crucial for accurate client-side state management.

## Order Filled Notifications Workflow

tastytrade aims to mark an order as "Filled" and send corresponding fill data through the Account Streamer as quickly as possible. The process generally follows these steps:

1.  **Fill Data Reception**: tastytrade receives fill data from the exchange for each individual leg of an order.
2.  **Order Status Update**: An order is marked as "Filled" when there is no remaining quantity left to fill across all its legs.
3.  **Fill Data Publication**: tastytrade publishes fill data over the Account Streamer for each filled leg.

## Multi-Leg Option Order Specifics

For multi-leg option orders, which are designed to be executed simultaneously, there's a specific handling mechanism:

*   **Initial "Filled" Status**: The order is marked "Filled" as soon as the **first leg** is processed, assuming that leg has no remaining quantity.
*   **Staggered Fill Data**: The initial account streamer message for a multi-leg order marked "Filled" will show only the fill data for that first processed leg.
*   **Subsequent Fill Data**: The fills for the remaining legs are processed and published over the Account Streamer immediately afterward.
*   **Final Message**: The final message for the order will include all fill data for all legs, reflecting the complete execution.

This staggered approach ensures that clients receive immediate notification of the order's "Filled" status, even if all individual leg fills haven't been fully processed and aggregated yet.

## Granular Fill Notifications

It's important to note that order legs can often be filled multiple times. For instance, an order to buy 100 shares of AAPL might result in 100 separate fills for 1 share each. The tastytrade Account Streamer publishes **each of these individual fills as a separate message** as they are processed. This provides a highly granular view of the order's execution progress.

This detailed streaming of fill data allows client applications to track the precise execution of orders in real-time.

---
*Source: [[../sources/tastytrade-streaming-account-data-doc.md|tastytrade Streaming Account Data Documentation]]*