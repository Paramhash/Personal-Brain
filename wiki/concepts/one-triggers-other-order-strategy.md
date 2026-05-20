---
tags: ["tastytrade", "api", "complex-order", "strategy", "OTO"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# One-Triggers-Other (OTO) Order Strategy

The One-Triggers-Other (OTO) is a complex order strategy where a primary "trigger" order must execute first. Once the trigger order is completely filled, one or more "child" orders are then activated and submitted to the market.

This strategy is defined in the [[../concepts/tastytrade-complex-order-request-body.md]] using the `type: "OTO"`, and requires both a `trigger-order` and an `orders` array. The response object for this strategy is detailed in [[../concepts/tastytrade-complex-order-object.md]].

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-complex-order-request-body.md]]
*   [[../concepts/tastytrade-complex-order-object.md]]
*   [[../concepts/one-cancels-other-order-strategy.md]]
*   [[../concepts/one-triggers-other-cancels-other-order-strategy.md]]
---