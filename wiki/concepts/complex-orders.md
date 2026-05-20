---
tags: ["trading", "api", "orders", "strategy"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Complex Orders

Complex orders, often referred to as bracket orders, are advanced trading strategies that involve multiple linked orders. These orders have dedicated API endpoints for their submission, retrieval, and cancellation, distinct from simple single-leg orders.

The JSON structure for submitting complex orders differs significantly from standard orders, as it needs to define the relationships and conditions between the constituent orders.

## Types of Complex Orders

Common types of complex orders include:

*   [[../concepts/otoco-order.md|OTOCO (One Triggers One Cancels Other)]]: An opening order that, upon filling, triggers two contingent closing orders (a stop loss and a profit target), where one cancels the other.
*   [[../concepts/oto-order.md|OTO (One Triggers Other)]]: An opening order that, upon filling, triggers one or more additional orders that do not cancel each other out.
*   [[../concepts/oco-order.md|OCO (One Cancels Other)]]: Two contingent closing orders (a stop loss and a profit target) that are submitted simultaneously, where the fill of one automatically cancels the other.

## Management Endpoints

*   **Submit Complex Order**: `POST /accounts/{account_number}/complex-orders`
*   **Cancel Complex Order**: `DELETE /accounts/{account_number}/complex-orders/{id}`

## External References
For more detailed information on bracket orders and their strategic purpose, refer to the [[../entities/tastytrade.md|tastytrade]] help center article (implied, as the source mentions "tastytrade's help center article here").

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/submit-order.md|Submit Order]]
*   [[../concepts/cancel-order.md|Cancel Order]]
*   [[../entities/tastytrade.md|tastytrade]]