---
tags: ["tastytrade", "api", "order", "schema", "request"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# tastytrade Order Request Body

This document describes the JSON structure used when submitting a single order to the tastytrade Orders API, specifically for `POST /accounts/{account_number}/orders` and its dry-run equivalent.

This request body is also used as a component within the [[../concepts/tastytrade-complex-order-request-body.md]] for defining individual orders within a complex strategy.

## Order-Level Fields

These fields define the overall characteristics of the order.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `order-type` | string | Yes | `Limit`, `Market`, `Marketable Limit`, `Notional Market`, `Stop`, `Stop Limit` |
| `time-in-force` | string | Yes | `Day`, `Ext`, `Ext Overnight`, `GTC`, `GTC Ext`, `GTC Ext Overnight`, `GTD`, `IOC` |
| `price` | number (double) | Conditional | The limit price. Required for `Limit` and `Stop Limit` orders. For multi-leg orders, this is the **net** price of all legs combined. |
| `price-effect` | string | Conditional | `Credit` or `Debit`. Required when `price` is specified. |
| `stop-trigger` | number (double) | Conditional | The stop trigger price. Required for `Stop` and `Stop Limit` orders. |
| `value` | number (double) | Conditional | The notional dollar value. Required for `Notional Market` orders (fractional share purchases by dollar amount). |
| `value-effect` | string | Conditional | `Credit` or `Debit`. Required when `value` is specified. |
| `gtc-date` | string (date) | Conditional | Expiration date for `GTD` orders (`YYYY-MM-DD`). Only valid when `time-in-force` is `GTD`. |
| `legs` | array | Yes | Array of 1–4 order legs (see below) |
| `rules` | object | No | Conditional execution rules (see below) |
| `advanced-instructions` | object | No | Advanced order instructions (see below) |
| `source` | string | No | Identifier for the source of the order (e.g., your application name) |
| `external-identifier` | string | No | Your external identifier for the order |
| `automated-source` | boolean | No | Set to `true` if the order was placed by an automated/algorithmic system |
| `preflight-id` | string | No | Transient identifier for matching preflight errors to a specific order |
| `partition-key` | string | No | Account partition key |

## Leg Fields

Each order contains 1–4 legs, where each leg represents a single instrument action.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `symbol` | string | Yes | The instrument symbol. Equity: `AAPL`. Equity Option (OCC format): `AAPL  260417C00200000`. Future: `/ESM6`. Future Option: `./ESZ9 EW4U9 190927P2975`. |
| `instrument-type` | string | Yes | `Cryptocurrency`, `Equity`, `Equity Option`, `Event Contract`, `Fixed Income Security`, `Future`, `Future Option`, `Liquidity Pool` |
| `action` | string | Yes | `Buy to Open`, `Buy to Close`, `Sell to Open`, `Sell to Close`. For futures only: `Buy`, `Sell`. |
| `quantity` | number (double) | Conditional | Number of shares or contracts. Required for all orders except `Notional Market`. |

**Action values explained:**

| Action | Use When |
|--------|----------|
| `Buy to Open` | Opening a new long position (buying stock, buying options) |
| `Buy to Close` | Closing an existing short position |
| `Sell to Open` | Opening a new short position (selling options, shorting stock) |
| `Sell to Close` | Closing an existing long position |
| `Buy` | Buying futures (futures do not distinguish open/close) |
| `Sell` | Selling futures |

## Rules (Conditional Execution)

Optional rules for controlling when an order is routed or canceled.

| Field | Type | Description |
|-------|------|-------------|
| `route-after` | datetime | Earliest time the order should be routed (delayed submission) |
| `cancel-at` | datetime | Latest time the order should remain active before auto-cancellation |
| `conditions` | array | Array of price-based conditions that must be met before the order is routed or canceled |

Each condition object:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | string | Yes | `route` (route the order when triggered) or `cancel` (cancel the order when triggered) |
| `symbol` | string | No | The symbol to monitor for the condition (e.g., `AAPL`, `/ESZ9`) |
| `instrument-type` | string | No | The instrument type of the monitored symbol |
| `indicator` | string | Yes | The price indicator to monitor: `last` (last trade price) or `nat` (natural price) |
| `comparator` | string | Yes | `gte` (greater than or equal to) or `lte` (less than or equal to) |
| `threshold` | number (double) | Yes | The price threshold that triggers the condition |
| `price-components` | array | No | For complex conditions based on a synthetic price derived from multiple instruments |

## Advanced Instructions

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `strict-position-effect-validation` | boolean | false | If true, the order is rejected when the open/close position effect is not valid (e.g., trying to `Sell to Close` a position you don't hold) |

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-complex-order-request-body.md]]
*   [[../concepts/tastytrade-order-object.md]]
---