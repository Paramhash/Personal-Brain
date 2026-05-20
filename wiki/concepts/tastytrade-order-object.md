---
tags: ["tastytrade", "api", "order", "schema", "response"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# tastytrade Order Object

The `Order` object represents a single trading order within the tastytrade system. It is returned by various GET endpoints (e.g., `GET /accounts/{account_number}/orders/{id}`) and embedded within the [[../concepts/tastytrade-placed-order-response.md]] object after order submission or dry-run.

## Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | The unique order identifier |
| `account-number` | string | The account number |
| `status` | string | Current order status (see [[../concepts/tastytrade-order-status-values.md]] for values) |
| `order-type` | string | The order type (`Limit`, `Market`, etc.) |
| `time-in-force` | string | The time-in-force setting |
| `price` | number (double) | The order price (limit price for limit orders) |
| `price-effect` | string | `Credit` or `Debit` |
| `stop-trigger` | string | The stop trigger price |
| `value` | number (double) | Notional value (for notional market orders) |
| `value-effect` | string | `Credit` or `Debit` |
| `size` | string | The total order size |
| `underlying-symbol` | string | The underlying symbol |
| `underlying-instrument-type` | string | The underlying instrument type |
| `gtc-date` | date | The GTD expiration date |
| `source` | string | The order source |
| `external-identifier` | string | External identifier |

## Lifecycle Timestamps

| Field | Type | Description |
|-------|------|-------------|
| `received-at` | datetime | When the order was received by the system |
| `live-at` | datetime | When the order went live on the exchange |
| `in-flight-at` | datetime | When the order entered in-flight status |
| `terminal-at` | datetime | When the order reached a terminal state (filled, cancelled, rejected, expired) |
| `cancelled-at` | datetime | When the order was cancelled |
| `updated-at` | string | Last update timestamp |

## State & Control

| Field | Type | Description |
|-------|------|-------------|
| `cancellable` | boolean | Whether the order can currently be cancelled |
| `editable` | boolean | Whether the order can currently be edited/replaced |
| `edited` | boolean | Whether the order has been edited |
| `reject-reason` | string | The reason the order was rejected (if applicable) |
| `replaces-order-id` | string | The ID of the order this order replaces (if cancel-replace) |
| `replacing-order-id` | string | The ID of the order replacing this one |
| `complex-order-id` | string | The ID of the parent complex order (if part of one) |
| `complex-order-tag` | string | The tag identifying this order's role in a complex order (e.g., `OTO::trigger-order`) |
| `contingent-status` | string | Contingent status for complex order components |
| `preflight-id` | string | The preflight identifier |
| `global-request-id` | string | Global request tracking ID |
| `leg-count` | string | Number of legs in the order |

## User Information

| Field | Type | Description |
|-------|------|-------------|
| `user-id` | string | The user who placed the order |
| `username` | string | The username who placed the order |
| `cancel-user-id` | string | The user who cancelled the order |
| `cancel-username` | string | The username who cancelled the order |

## Legs (Response)

Each leg in the response includes fill information:

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The instrument symbol |
| `instrument-type` | string | The instrument type |
| `action` | string | The order action |
| `quantity` | string | The ordered quantity |
| `remaining-quantity` | string | The quantity remaining to be filled |
| `fills` | array | Array of fill objects (see below) |

## Fill Object

Each fill represents a partial or complete execution of a leg.

| Field | Type | Description |
|-------|------|-------------|
| `fill-id` | string | Unique fill identifier |
| `fill-price` | number (double) | The price at which the fill occurred |
| `quantity` | string | The quantity filled |
| `filled-at` | datetime | When the fill occurred |
| `destination-venue` | string | The venue where the fill occurred |
| `ext-exec-id` | string | External execution ID |
| `ext-group-fill-id` | string | External group fill ID (for multi-leg fills) |

## Order Rule (Response)

| Field | Type | Description |
|-------|------|-------------|
| `route-after` | datetime | Earliest routing time |
| `routed-at` | datetime | When the order was actually routed |
| `cancel-at` | datetime | Auto-cancel time |
| `cancelled-at` | datetime | When the auto-cancel executed |
| `order-conditions` | array | Array of conditions with their trigger state (`triggered-at`, `triggered-value`) |

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-order-request-body.md]]
*   [[../concepts/tastytrade-placed-order-response.md]]
*   [[../concepts/tastytrade-order-status-values.md]]
---