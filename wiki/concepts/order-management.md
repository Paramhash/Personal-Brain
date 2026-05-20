---
tags: ["trading", "api", "orders"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Order Management

Order Management refers to the suite of functionalities and API endpoints designed to create, monitor, modify, and cancel trading orders within a financial system. It encompasses various operations from simple order submission to complex multi-leg strategies.

Key aspects of order management include:
*   [[../concepts/search-orders.md|Searching and retrieving orders]]
*   [[../concepts/live-orders.md|Monitoring live and recently updated orders]]
*   [[../concepts/order-dry-run.md|Verifying order validity and impact without execution]]
*   [[../concepts/submit-order.md|Submitting new orders]]
*   [[../concepts/cancel-order.md|Canceling existing orders]]
*   [[../concepts/cancel-replace-order.md|Modifying and replacing existing orders]]
*   [[../concepts/complex-orders.md|Managing advanced order types like OTOCO, OTO, and OCO]]

Effective order management is crucial for traders to execute strategies efficiently, manage risk, and react to market changes. Real-time updates are often facilitated through mechanisms like [[../entities/account-streamer.md|Account Streamers]] to avoid performance degradation from polling.

## Related Concepts
*   [[../concepts/order-status.md|Order Status]]
*   [[../concepts/buying-power.md|Buying Power]]
*   [[../concepts/api-fees.md|API Fees]]
*   [[../entities/tastytrade.md|tastytrade]] (as the platform provider)

## External References
*   [[../sources/order-submission-guide.md|Order Submission Guide]]
*   [[../sources/order-flow-guide.md|Order Flow Guide]]