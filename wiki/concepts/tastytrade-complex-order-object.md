---
tags: ["tastytrade", "api", "complex-order", "schema", "response"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# tastytrade ComplexOrder Object

The `ComplexOrder` object represents a complex trading strategy within the tastytrade system. It is returned by various GET endpoints (e.g., `GET /accounts/{account_number}/complex-orders/{id}`) and can be embedded within the [[../concepts/tastytrade-placed-order-response.md]] object after complex order submission or dry-run.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The complex order identifier |
| `account-number` | string | The account number |
| `type` | string | The complex order type ([[../concepts/one-triggers-other-order-strategy.md]] (OTO), [[../concepts/one-cancels-other-order-strategy.md]] (OCO), [[../concepts/one-triggers-other-cancels-other-order-strategy.md]] (OTOCO), [[../concepts/blast-order-strategy.md]] (BLAST), [[../concepts/pairs-order-strategy.md]] (PAIRS)) |
| `trigger-order` | [[../concepts/tastytrade-order-object.md]] | The trigger order (tagged with `complex-order-tag` like `OTO::trigger-order`) |
| `orders` | array | The child orders (each element is a [[../concepts/tastytrade-order-object.md]]) |
| `related-orders` | array | Related orders |
| `terminal-at` | string | When the complex order reached terminal state |
| `ratio-price-comparator` | string | For [[../concepts/pairs-order-strategy.md]]: `gte` or `lte` |
| `ratio-price-threshold` | number (double) | For [[../concepts/pairs-order-strategy.md]]: the ratio threshold |
| `ratio-price-is-threshold-based-on-notional` | boolean | For [[../concepts/pairs-order-strategy.md]]: notional-based comparison |

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-complex-order-request-body.md]]
*   [[../concepts/tastytrade-order-object.md]]
*   [[../concepts/placed-order-response.md]]
*   [[../concepts/one-triggers-other-order-strategy.md]]
*   [[../concepts/one-cancels-other-order-strategy.md]]
*   [[../concepts/one-triggers-other-cancels-other-order-strategy.md]]
*   [[../concepts/blast-order-strategy.md]]
*   [[../concepts/pairs-order-strategy.md]]
---