---
tags: ["trading", "api", "orders", "complex-order", "bracket-order"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# OCO Order (One Cancels Other)

An OCO (One Cancels Other) order is a type of [[../concepts/complex-orders.md|complex order]] that consists of two contingent closing orders submitted simultaneously. These orders are typically a "stop loss" order and a "close at profit" (limit) order.

The defining characteristic of an OCO order is that if one of the two orders fills, the other is automatically cancelled. This helps manage risk and profit targets for an existing position. Since both orders are closing orders, an existing position must be held in the account to submit an OCO order.

## Submission

*   **API Endpoint**: `POST /accounts/{account_number}/complex-orders`
*   **Request Body**: The JSON includes a `type` field set to "OCO" and an `orders` array containing the two contingent closing orders. There is no `trigger-order` for OCO orders.

## Response

The response provides an `id` for the overall complex order and individual `id`s for each of the two contingent orders.

## Example Request Body
```json
{
    "type": "OCO",
    "orders": [{
    "order-type": "Limit",
    "price": 200.50,
    "price-effect": "Credit",
    "time-in-force": "GTC",
    "legs": [
        {
            "symbol": "AAPL",
            "instrument-type": "Equity",
            "action": "Sell to Close",
            "quantity": 100
            }
        ]
    },
    {
        "order-type": "Stop",
        "time-in-force": "GTC",
        "stop-trigger": 150.25,
        "legs": [{
            "symbol": "AAPL",
            "instrument-type": "Equity",
            "action": "Sell to Close",
            "quantity": 100
            }]
        }
    ]
}
```

## Related
*   [[../concepts/complex-orders.md|Complex Orders]]
*   [[../concepts/otoco-order.md|OTOCO Order]]
*   [[../concepts/oto-order.md|OTO Order]]
*   [[../concepts/order-management.md|Order Management]]