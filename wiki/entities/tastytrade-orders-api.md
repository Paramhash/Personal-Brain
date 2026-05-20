---
tags: ["api", "trading", "tastytrade", "orders"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# tastytrade Orders API

The tastytrade Orders API is the core trading interface for the tastytrade Open API, providing comprehensive functionality for managing trading orders. It allows users to submit, retrieve, modify, and cancel single orders, as well as manage complex multi-order strategies. The API also includes dry-run endpoints for pre-flight validation, ensuring orders meet requirements before live submission.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 0.0.1 (versioned as `20250813`)

## Endpoints — Single Orders

These endpoints manage individual trading orders for a specific account.

*   **Search Orders**
    `GET /accounts/{account_number}/orders`
    Returns a paginated list of orders with filtering and sorting options.
*   **Get Live Orders**
    `GET /accounts/{account_number}/orders/live`
    Returns all orders from the current trading day, regardless of status.
*   **Get Order by ID**
    `GET /accounts/{account_number}/orders/{id}`
    Retrieves a single order using its unique identifier.
*   **Submit Order**
    `POST /accounts/{account_number}/orders`
    Places a new order. The request body structure is detailed in [[../concepts/tastytrade-order-request-body.md]].
*   **Order Dry Run**
    `POST /accounts/{account_number}/orders/dry-run`
    Validates an order without placing it live. Returns a [[../concepts/tastytrade-placed-order-response.md]] object.
*   **Cancel Order**
    `DELETE /accounts/{account_number}/orders/{id}`
    Requests cancellation of a live order.
*   **Replace Order (Full)**
    `PUT /accounts/{account_number}/orders/{id}`
    Atomically cancels an existing live order and submits a new one.
*   **Edit Order (Partial)**
    `PATCH /accounts/{account_number}/orders/{id}`
    Modifies specific properties (e.g., price, time-in-force) of a live order via a cancel-replace mechanism.
*   **Replace/Edit Dry Run**
    `POST /accounts/{account_number}/orders/{id}/dry-run`
    Performs pre-flight checks for a cancel-replace or edit operation. Returns a [[../concepts/tastytrade-placed-order-response.md]] object.

## Endpoints — Complex Orders

These endpoints manage strategies combining multiple orders with defined execution relationships. For details on the request body, see [[../concepts/tastytrade-complex-order-request-body.md]].

*   **Get Complex Orders**
    `GET /accounts/{account_number}/complex-orders`
    Returns a paginated list of all complex orders for an account.
*   **Get Live Complex Orders**
    `GET /accounts/{account_number}/complex-orders/live`
    Returns all complex orders where a component order was placed today.
*   **Get Complex Order by ID**
    `GET /accounts/{account_number}/complex-orders/{id}`
    Retrieves a single complex order by its ID.
*   **Submit Complex Order**
    `POST /accounts/{account_number}/complex-orders`
    Creates a new complex order strategy.
*   **Complex Order Dry Run**
    `POST /accounts/{account_number}/complex-orders/dry-run`
    Validates a complex order without placing it.
*   **Edit Complex Order**
    `PATCH /accounts/{account_number}/complex-orders/{id}`
    Edits specific properties of a complex order, such as the threshold price for PAIRS trades.
*   **Cancel Complex Order**
    `DELETE /accounts/{account_number}/complex-orders/{id}`
    Cancels all non-terminal component orders of a complex order.
*   **Complex Order Edit Dry Run**
    `POST /accounts/{account_number}/complex-orders/{id}/dry-run`
    Performs pre-flight checks for editing a complex order.

## Endpoints — Customer-Level Order Queries

These endpoints allow querying orders across all accounts for a given customer.

*   **Search Customer Orders**
    `GET /customers/{customer_id}/orders`
    Similar to account-level search, but across all customer accounts.
*   **Get Customer Live Orders**
    `GET /customers/{customer_id}/orders/live`
    Returns all live orders for a customer across all their accounts.

## Data Models

The API utilizes several key data models for requests and responses:

*   [[../concepts/tastytrade-order-request-body.md]]: Structure for submitting single orders.
*   [[../concepts/tastytrade-complex-order-request-body.md]]: Structure for submitting complex orders.
*   [[../concepts/tastytrade-order-object.md]]: The detailed object representing a single order in responses.
*   [[../concepts/tastytrade-placed-order-response.md]]: The response object returned after submitting or dry-running an order.
*   [[../concepts/tastytrade-complex-order-object.md]]: The detailed object representing a complex order in responses.
*   [[../concepts/tastytrade-order-status-values.md]]: A comprehensive list of possible order statuses.

## Complex Order Types

The API supports various complex order strategies:

*   [[../concepts/one-triggers-other-order-strategy.md]] (OTO)
*   [[../concepts/one-cancels-other-order-strategy.md]] (OCO)
*   [[../concepts/one-triggers-other-cancels-other-order-strategy.md]] (OTOCO)
*   [[../concepts/blast-order-strategy.md]] (BLAST)
*   [[../concepts/pairs-order-strategy.md]] (PAIRS)

## Example Requests

### Buy 100 Shares of Stock

```json
{
  "order-type": "Limit",
  "time-in-force": "Day",
  "price": 185.00,
  "price-effect": "Debit",
  "legs": [
    {
      "symbol": "AAPL",
      "instrument-type": "Equity",
      "action": "Buy to Open",
      "quantity": 100
    }
  ]
}
```

### Sell to Close an Equity Position

```json
{
  "order-type": "Limit",
  "time-in-force": "Day",
  "price": 190.00,
  "price-effect": "Credit",
  "legs": [
    {
      "symbol": "AAPL",
      "instrument-type": "Equity",
      "action": "Sell to Close",
      "quantity": 100
    }
  ]
}
```

### Buy a Call Option

```json
{
  "order-type": "Limit",
  "time-in-force": "Day",
  "price": 3.50,
  "price-effect": "Debit",
  "legs": [
    {
      "symbol": "AAPL  260619C00200000",
      "instrument-type": "Equity Option",
      "action": "Buy to Open",
      "quantity": 1
    }
  ]
}
```

### Sell a Put Credit Spread (2-Leg)

```json
{
  "order-type": "Limit",
  "time-in-force": "Day",
  "price": 1.25,
  "price-effect": "Credit",
  "legs": [
    {
      "symbol": "SPY   260619P00540000",
      "instrument-type": "Equity Option",
      "action": "Sell to Open",
      "quantity": 1
    },
    {
      "symbol": "SPY   260619P00535000",
      "instrument-type": "Equity Option",
      "action": "Buy to Open",
      "quantity": 1
    }
  ]
}
```

### Iron Condor (4-Leg)

```json
{
  "order-type": "Limit",
  "time-in-force": "Day",
  "price": 2.00,
  "price-effect": "Credit",
  "legs": [
    {
      "symbol": "SPY   260619P00530000",
      "instrument-type": "Equity Option",
      "action": "Buy to Open",
      "quantity": 1
    },
    {
      "symbol": "SPY   260619P00540000",
      "instrument-type": "Equity Option",
      "action": "Sell to Open",
      "quantity": 1
    },
    {
      "symbol": "SPY   260619C00570000",
      "instrument-type": "Equity Option",
      "action": "Sell to Open",
      "quantity": 1
    },
    {
      "symbol": "SPY   260619C00580000",
      "instrument-type": "Equity Option",
      "action": "Buy to Open",
      "quantity": 1
    }
  ]
}
```

### Notional Market Order (Fractional Shares by Dollar Amount)

```json
{
  "order-type": "Notional Market",
  "time-in-force": "Day",
  "value": 500.00,
  "value-effect": "Debit",
  "legs": [
    {
      "symbol": "AAPL",
      "instrument-type": "Equity",
      "action": "Buy to Open"
    }
  ]
}
```

### OTO (One-Triggers-Other) Complex Order

```json
{
  "type": "OTO",
  "trigger-order": {
    "order-type": "Limit",
    "time-in-force": "Day",
    "price": 185.00,
    "price-effect": "Debit",
    "legs": [
      {
        "symbol": "AAPL",
        "instrument-type": "Equity",
        "action": "Buy to Open",
        "quantity": 100
      }
    ]
  },
  "orders": [
    {
      "order-type": "Stop",
      "time-in-force": "GTC",
      "stop-trigger": 175.00,
      "price-effect": "Credit",
      "legs": [
        {
          "symbol": "AAPL",
          "instrument-type": "Equity",
          "action": "Sell to Close",
          "quantity": 100
        }
      ]
    }
  ]
}
```

## Common Use Cases

*   **Place and monitor:** Submit an order via POST, then poll `GET /accounts/{account_number}/orders/{id}` or use the account streamer WebSocket to monitor status changes through `Received` → `Routed` → `Live` → `Filled`.
*   **Pre-flight validation:** Always use the dry-run endpoint first to check buying power, fees, and potential errors before submitting a live order. The response structure is identical to a live submission, returning a [[../concepts/tastytrade-placed-order-response.md]] object.
*   **Cancel-replace to adjust price:** Use `PATCH /accounts/{account_number}/orders/{id}` with just the new `price` field to adjust a working limit order's price without resubmitting the full order.
*   **Bracket orders:** Use an [[../concepts/one-triggers-other-cancels-other-order-strategy.md]] (OTOCO) complex order to submit an entry order that, when filled, automatically activates a take-profit limit and a stop-loss as an OCO pair.
*   **Search for fills:** Use `GET /accounts/{account_number}/orders?status[]=Filled&start-date=YYYY-MM-DD` to find all filled orders for a specific date. Each order's legs contain `fills` with the execution details.

## Important Notes

*   **Price for multi-leg orders:** The `price` field represents the **net** price of all legs combined, not the price of any individual leg. For a credit spread priced at `1.25` credit, set `price: 1.25` and `price-effect: "Credit"`.
*   **Options quantity:** The `quantity` for equity options is the **number of contracts**, not the number of shares. A quantity of `1` means 1 contract = 100 shares of exposure (for standard options).
*   **Options price:** The `price` for options orders is the **per-contract price** (e.g., `3.50`), not the total cost. The total cost is `price × quantity × multiplier` (e.g., `3.50 × 1 × 100 = $350`).
*   **Futures actions:** Futures use `Buy` and `Sell` (not `Buy to Open`/`Sell to Close`) because futures do not distinguish between opening and closing transactions.
*   **Time-in-force values:** `Ext` = extended hours, `Ext Overnight` = extended hours including overnight session, `GTC Ext` = good-til-canceled including extended hours, `IOC` = immediate-or-cancel.
*   **Automated source flag:** Set `automated-source: true` for algorithmically-generated orders. This may affect order handling and regulatory reporting.
*   **Dry run before live:** The dry-run response includes `errors` (blocking) and `warnings` (non-blocking). Always check `errors` — if non-empty, the order would be rejected.

---