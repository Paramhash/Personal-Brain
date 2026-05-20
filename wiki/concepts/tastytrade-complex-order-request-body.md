---
tags: ["tastytrade", "api", "complex-order", "schema", "request"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# tastytrade Complex Order Request Body

This document describes the JSON structure used when submitting a complex order strategy to the tastytrade Orders API, specifically for `POST /accounts/{account_number}/complex-orders` and its dry-run equivalent.

Complex orders combine multiple individual orders into a single strategy with defined execution relationships.

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | The complex order strategy: `OTO`, `OCO`, `OTOCO`, `BLAST`, `PAIRS` |
| `trigger-order` | object | Conditional | The initial live order for OTO-based strategies. This order executes first. Required for `OTO` and `OTOCO`. Contains a full [[../concepts/tastytrade-order-request-body.md]] structure. |
| `orders` | array | Conditional | Array of child orders for OCO/BLAST strategies. Required for `OCO`, `BLAST`, and the child portion of `OTOCO`. Each element is a full [[../concepts/tastytrade-order-request-body.md]] structure. |
| `source` | string | No | Source identifier |
| `ratio-price-comparator` | string | No | For [[../concepts/pairs-order-strategy.md]] trades: `gte` or `lte` |
| `ratio-price-threshold` | number (double) | No | For [[../concepts/pairs-order-strategy.md]] trades: the ratio price threshold |
| `ratio-price-is-threshold-based-on-notional` | boolean | No | For [[../concepts/pairs-order-strategy.md]] trades: whether the threshold comparison uses notional value |

## Complex Order Types

| Type | Description | Structure |
|------|-------------|-----------|
| `OTO` | [[../concepts/one-triggers-other-order-strategy.md]]: One-Triggers-Other: when the trigger order fills, the child order(s) are activated | `trigger-order` + `orders` |
| `OCO` | [[../concepts/one-cancels-other-order-strategy.md]]: One-Cancels-Other: multiple orders are live simultaneously; when one fills, the others are canceled | `orders` (array of 2+ orders) |
| `OTOCO` | [[../concepts/one-triggers-other-cancels-other-order-strategy.md]]: One-Triggers-OCO: trigger order fills, then an OCO group is activated | `trigger-order` + `orders` |
| `BLAST` | [[../concepts/blast-order-strategy.md]]: All orders are submitted simultaneously (no conditional relationship) | `orders` (array of orders) |
| `PAIRS` | [[../concepts/pairs-order-strategy.md]]: A pairs trade with a ratio-based price threshold | `orders` + ratio fields |

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-order-request-body.md]]
*   [[../concepts/tastytrade-complex-order-object.md]]
*   [[../concepts/one-triggers-other-order-strategy.md]]
*   [[../concepts/one-cancels-other-order-strategy.md]]
*   [[../concepts/one-triggers-other-cancels-other-order-strategy.md]]
*   [[../concepts/blast-order-strategy.md]]
*   [[../concepts/pairs-order-strategy.md]]
---