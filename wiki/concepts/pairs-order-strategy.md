---
tags: ["tastytrade", "api", "complex-order", "strategy", "PAIRS"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# PAIRS Order Strategy

The PAIRS strategy is a complex order type designed for pairs trading, where two related instruments are traded simultaneously based on a ratio-based price threshold. The orders are submitted when a specified ratio price condition (greater than or equal to, or less than or equal to a threshold) is met.

This strategy is defined in the [[../concepts/tastytrade-complex-order-request-body.md]] using the `type: "PAIRS"`, and includes `orders` along with `ratio-price-comparator`, `ratio-price-threshold`, and `ratio-price-is-threshold-based-on-notional` fields. The response object for this strategy is detailed in [[../concepts/tastytrade-complex-order-object.md]].

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-complex-order-request-body.md]]
*   [[../concepts/tastytrade-complex-order-object.md]]
---