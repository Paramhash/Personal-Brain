---
tags: ["trading", "order-status", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "order-flow-raw-payload.md"
---
# Order Status: Working Phase (tastytrade)

The Working Phase signifies that an order has successfully reached the exchange and the exchange has confirmed its receipt. During this phase, an order is considered "live" and actively seeking a fill. This phase can last from milliseconds to days or even months for GTC (Good 'Til Canceled) orders.

Statuses in this phase include:

*   **Live**: This is always the first status after the [[../concepts/order-status-submission-phase.md|Submission Phase]]. A `Live` order is actively working at the exchange. Once an order is `Live`, a user can choose to cancel or replace it.
*   **Cancel Requested**: When a user decides to cancel a `Live` order, its status changes to `Cancel Requested`. This means [[../entities/tastytrade.md|tastytrade]] has sent the cancellation request to the exchange and is awaiting confirmation. Upon confirmation, the order will transition to the [[../concepts/order-status-terminal-phase.md|Canceled]] status.
*   **Replace Requested**: If a user submits a replacement order for an existing `Live` order (referred to as the original order), the original order's status becomes `Replace Requested`. [[../entities/tastytrade.md|tastytrade]] then sends a cancel request for the original order to the exchange. During this time, the replacement order's status is [[../concepts/order-status-submission-phase.md|Contingent]], waiting for the original order to become `Canceled`. Once the exchange confirms the cancellation of the original order, the replacement order will be routed. This mechanism ensures that the replacement order is not sent until the original is definitively off the market.

---
This note details the active phase of [[../concepts/order-flow.md|Order Flow]] within the [[../entities/tastytrade.md|tastytrade]] system, based on the [[../sources/order-flow-raw-payload.md|Order Flow Raw Payload]].