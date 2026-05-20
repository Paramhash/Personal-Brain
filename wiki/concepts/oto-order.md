---
tags: ["trading", "api", "orders", "complex-order", "bracket-order"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# OTO Order (One Triggers Other)

An OTO (One Triggers Other) order is a type of [[../concepts/complex-orders.md|complex order]] where an initial "trigger order" activates one or more additional orders upon its fill. Unlike OTOCO orders, the triggered orders in an OTO sequence do not automatically cancel each other out.

This type of order is useful for strategies where subsequent actions are dependent on an initial trade's execution but are not mutually exclusive (e.g., closing multiple legs of a spread or initiating follow-up trades).

## Submission

*   **API Endpoint**: `POST /accounts/{account_number}/complex-orders`
*   **Request Body**: The JSON includes a `type` field set to "OTO", a `trigger-order` object, and an `orders` array containing up to three additional orders that will be routed when the trigger order fills.

## Response

Similar to OTOCO, the response provides an `id` for the overall complex order and individual `id`s for the trigger order and each of the contingent orders.

## Example Request Body
```json
{
  "type": "OTO",
  "trigger-order": {
    "time-in-force": "Day",
    "order-type": "Limit",
    "underlying-symbol": "AAPL",
    "price": 11.50,
    "price-effect": "Debit",
    "legs": [
      {
        "instrument-type": "Equity Option",
        "symbol": "AAPL  250214C00240000",
        "quantity": 1,
        "action": "Buy to Close"
      },
      {
        "instrument-type": "Equity Option",
        "symbol": "AAPL  250214P00235000",
        "quantity": 1,
        "action": "Buy to Close"
      }
    ]
  },
  "orders": [
    {
      "time-in-force": "Day",
      "order-type": "Market",
      "underlying-symbol": "AAPL",
      "legs": [
        {
          "instrument-type": "Equity Option",
          "symbol": "AAPL  250214C00242500",
          "quantity": 1,
          "action": "Sell to Close"
        }
      ]
    },
    {
      "time-in-force": "Day",
      "order-type": "Market",
      "underlying-symbol": "AAPL",
      "legs": [
        {
          "instrument-type": "Equity Option",
          "symbol": "AAPL  250214P00232500",
          "quantity": 1,
          "action": "Sell to Close"
        }
      ]
    }
  ]
}
```

## Related
*   [[../concepts/complex-orders.md|Complex Orders]]
*   [[../concepts/otoco-order.md|OTOCO Order]]
*   [[../concepts/oco-order.md|OCO Order]]
*   [[../concepts/order-management.md|Order Management]]