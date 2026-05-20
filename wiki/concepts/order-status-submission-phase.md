---
tags: ["trading", "order-status", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "order-flow-raw-payload.md"
---
# Order Status: Submission Phase (tastytrade)

The Submission Phase in the [[../entities/tastytrade.md|tastytrade]] order flow refers to the initial stages where an order has not yet been received by an exchange and is therefore not considered "working."

Statuses in this phase include:

*   **Received**: This status appears when an order is submitted while the markets are closed. It signifies that [[../entities/tastytrade.md|tastytrade]] has received the order, and it will be routed once the markets open.
*   **Routed**: The order is currently being submitted from the [[../entities/tastytrade.md|tastytrade]] system to an exchange. This is often the initial status seen after submitting an order during market hours.
*   **In Flight**: Immediately following `Routed`, this status means the order has left the [[../entities/tastytrade.md|tastytrade]] system and is awaiting confirmation from the exchange that it has been received.
*   **Contingent**: This status applies to complex orders such as OTOCO (One Triggers OCO) and OTO (One Triggers One) orders. These orders remain dormant within the [[../entities/tastytrade.md|tastytrade]] system until another order "triggers" them, at which point they will be routed to an exchange. Replacement orders also become `Contingent` immediately after submission, waiting for the original order to transition to `Canceled` status before being routed.

Occasionally, an order might immediately transition to a [[../concepts/order-status-terminal-phase.md|Rejected]] status during the submission phase. This can happen if, for example, the account lacks sufficient buying power to place the order.

---
This note details the initial phase of [[../concepts/order-flow.md|Order Flow]] within the [[../entities/tastytrade.md|tastytrade]] system, based on the [[../sources/order-flow-raw-payload.md|Order Flow Raw Payload]].