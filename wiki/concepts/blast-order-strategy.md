---
tags: ["tastytrade", "api", "complex-order", "strategy", "BLAST"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# BLAST Order Strategy

The BLAST (All orders submitted simultaneously) is a complex order strategy where all component orders are submitted to the market at the same time, with no conditional relationship between them. This is essentially a way to group multiple individual orders for simultaneous submission, without any trigger or cancellation logic.

This strategy is defined in the [[../concepts/tastytrade-complex-order-request-body.md]] using the `type: "BLAST"` and requires an `orders` array. The response object for this strategy is detailed in [[../concepts/tastytrade-complex-order-object.md]].

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-complex-order-request-body.md]]
*   [[../concepts/tastytrade-complex-order-object.md]]
---