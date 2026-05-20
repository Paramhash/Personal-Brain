---
tags: ["tastytrade", "api", "complex-order", "strategy", "OTOCO"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# One-Triggers-Other-Cancels-Other (OTOCO) Order Strategy

The One-Triggers-Other-Cancels-Other (OTOCO) is a hybrid complex order strategy that combines the functionality of OTO and OCO. A primary "trigger" order is submitted first. Once this trigger order is filled, an [[../concepts/one-cancels-other-order-strategy.md]] (OCO) group of child orders is then activated and submitted. This is often used for bracket orders, where an entry order triggers both a profit-taking limit and a stop-loss order.

This strategy is defined in the [[../concepts/tastytrade-complex-order-request-body.md]] using the `type: "OTOCO"`, and requires both a `trigger-order` and an `orders` array (for the OCO group). The response object for this strategy is detailed in [[../concepts/tastytrade-complex-order-object.md]].

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-complex-order-request-body.md]]
*   [[../concepts/tastytrade-complex-order-object.md]]
*   [[../concepts/one-triggers-other-order-strategy.md]]
*   [[../concepts/one-cancels-other-order-strategy.md]]
---