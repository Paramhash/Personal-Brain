---
tags: ["trading", "orders", "status"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Order Status

Order status refers to the current state of a trading order within the system, indicating its progression from submission to execution or cancellation. Understanding order statuses is crucial for monitoring trades and managing positions.

Common order statuses mentioned in the context of [[../concepts/order-management.md|Order Management]] include:

*   **Live**: The order is active and awaiting execution.
*   **Filled**: The order has been completely executed.
*   **Cancelled**: The order has been successfully cancelled.
*   **Rejected**: The order was not accepted by the system or exchange.
*   **Cancel Requested**: A request to cancel the order has been initiated and is pending.
*   **Routed**: The order has been successfully sent to the exchange.
*   **Contingent**: The order is pending a condition (e.g., a trigger order filling in a [[../concepts/complex-orders.md|complex order]]).
*   **Pending Order**: A specific contingent status, often seen within complex orders.
*   **Received**: The order has been received by the system (often an initial state before routing).

## Terminal Statuses

Certain statuses are considered "terminal," meaning the order can no longer be modified or cancelled. Attempting to cancel an order in a terminal status will result in an error. For more details on order flow and terminal statuses, refer to the [[../sources/order-flow-guide.md|Order Flow Guide]].

## Real-time Updates

For real-time updates on order status changes, it is recommended to use the [[../entities/account-streamer.md|Account Streamer]] rather than polling API endpoints like [[../concepts/live-orders.md|Live Orders]].

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/live-orders.md|Live Orders]]
*   [[../concepts/cancel-order.md|Cancel Order]]
*   [[../concepts/complex-orders.md|Complex Orders]]
*   [[../entities/account-streamer.md|Account Streamer]]
*   [[../sources/order-flow-guide.md|Order Flow Guide]]