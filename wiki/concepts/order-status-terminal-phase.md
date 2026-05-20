---
tags: ["trading", "order-status", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "order-flow-raw-payload.md"
---
# Order Status: Terminal Phase (tastytrade)

The Terminal Phase represents the final state of an order in the [[../entities/tastytrade.md|tastytrade]] system. Once an order enters any of these statuses, it will receive no further updates.

Statuses in this phase include:

*   **Filled**: This means your order has been fully executed. When an order fills, several actions occur:
    *   A position is created or updated in your account.
    *   Your account balance is updated to reflect the transaction.
    *   A trade transaction is created, detailing the trade and any associated fees.
    *   *Note*: [[../entities/tastytrade.md|tastytrade]] marks orders `Filled` as soon as possible. If an order's status is `Filled` but appears to be missing fills for one or more legs, it means the system is still processing the fills, which typically completes within milliseconds.
*   **Canceled**: The order has been canceled, either by the user or by the system (e.g., due to a [[../concepts/order-status-working-phase.md|Cancel Requested]] action).
*   **Rejected**: An order can be `Rejected` during the [[../concepts/order-status-submission-phase.md|Submission Phase]] (e.g., for a non-existent stock symbol or insufficient buying power) or even during the [[../concepts/order-status-working-phase.md|Working Phase]] if an issue arises.
*   **Expired**: This status primarily applies to day orders that do not fill by the time the market closes. [[../entities/tastytrade.md|tastytrade]] automatically marks these orders as `Expired`.
*   **Removed**: An administrator has manually removed this order from the customer's account.
*   **Partially Removed**: An administrator has manually removed part of this order from the customer's account.

---
This note details the final phase of [[../concepts/order-flow.md|Order Flow]] within the [[../entities/tastytrade.md|tastytrade]] system, based on the [[../sources/order-flow-raw-payload.md|Order Flow Raw Payload]].