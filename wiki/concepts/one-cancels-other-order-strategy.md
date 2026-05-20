---
tags: ["tastytrade", "api", "complex-order", "strategy", "OCO"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# One-Cancels-Other (OCO) Order Strategy

The One-Cancels-Other (OCO) is a complex order strategy involving two or more orders that are live simultaneously. If one of the orders in the group is filled (either partially or completely), the other orders in the same OCO group are automatically canceled. This is commonly used for profit-taking and stop-loss orders.

This strategy is defined in the [[../concepts/tastytrade-complex-order-request-body.md]] using the `type: "OCO"` and requires an `orders` array containing at least two orders. The response object for this strategy is detailed in [[../concepts/tastytrade-complex-order-object.md]].

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-complex-order-request-body.md]]
*   [[../concepts/tastytrade-complex-order-object.md]]
*   [[../concepts/one-triggers-other-order-strategy.md]]
*   [[../concepts/one-triggers-other-cancels-other-order-strategy.md]]
---