---
tags: ["api", "trading", "orders", "order-flow", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# Order Submission and Management (tastytrade API)

The [[../entities/tastytrade-open-api.md|tastytrade Open API]] provides comprehensive functionalities for submitting, managing, and tracking the lifecycle of trading orders.

## Order Submission
Detailed JSON structures are used to define orders, including:
*   **Order Attributes**: `order-type`, `price`, `price-effect`, `time-in-force`, `value`.
*   **Leg Attributes**: `action`, `instrument-type`, `quantity`, `symbol`.
*   **Examples**: Support for equity market/limit orders, equity option orders, multi-leg spreads (verticals, iron condors, strangles), and fractional stock orders.
*   **Order Responses**: Indicate whether an order is `rejected` or `accepted`, including `buying-power-effect` and `fee-calculation`.

## Order Flow (Lifecycle)
Orders progress through three main phases:
1.  **Submission**: `Received`, `Routed`, `In Flight`, `Contingent`.
2.  **Working**: `Live`, `Cancel Requested`, `Replace Requested`.
3.  **Terminal**: `Filled`, `Canceled`, `Rejected`, `Expired`, `Removed`.
The API provides status transition examples for various scenarios like immediate fills, customer cancellations, and brokerage rejections.

## Order Management Endpoints
The API offers a suite of endpoints for managing orders:
*   **Search/Filter Orders**: Retrieve orders based on various criteria.
*   **Live Orders**: View currently active orders.
*   **Order Dry Run**: Pre-flight validation of an order without actually placing it, useful for estimating margin impact.
*   **Submit Order**: Place new orders.
*   **Cancel Order**: Request cancellation of an existing order.
*   **Cancel-Replace (Modify)**: Modify parameters like price or quantity of a working order.
*   **Complex Order Operations**: Submit, cancel, or manage advanced strategies such as OTO (One Triggers Other), OCO (One Cancels Other), OTOCO (One Triggers One Cancels Other), BLAST, and PAIRS.
*   **Order Types**: Support for Limit, Market, Marketable Limit, Notional Market, Stop, Stop Limit.
*   **Time-in-Force (TIF)**: Day, Ext, GTC (Good Till Cancel), GTD (Good Till Date), IOC (Immediate Or Cancel).
*   **Conditional Rules**: Orders can include price triggers.
*   **Fill Tracking**: Detailed tracking of order fills.

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]
*   [[../concepts/api-margin-requirements-tastytrade.md|API Margin Requirements]]