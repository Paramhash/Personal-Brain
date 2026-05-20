---
tags: ["trading", "api", "orders", "complex-order", "bracket-order"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# OTOCO Order (One Triggers One Cancels Other)

An OTOCO (One Triggers One Cancels Other) order is a type of [[../concepts/complex-orders.md|complex order]] designed to manage risk and profit for an opening position. It consists of three linked orders:

1.  **Trigger Order**: An opening order.
2.  **Contingent Orders (OCO Pair)**: Two closing orders that become active only if the trigger order fills. These two orders form an [[../concepts/oco-order.md|OCO (One Cancels Other)]] pair, meaning if one fills, the other is automatically cancelled. Typically, one is a "stop loss" order and the other is a "close at profit" order.

The contingent orders remain in a "Contingent" status, waiting for the trigger order to be filled.

## Submission

*   **API Endpoint**: `POST /accounts/{account_number}/complex-orders`
*   **Request Body**: The JSON includes a `type` field set to "OTOCO", a `trigger-order` object, and an `orders` array containing the two contingent closing orders.

## Response

The response for a submitted OTOCO order provides a unique `id` for the overall complex order, as well as individual `id`s for the trigger order and each of the two contingent orders. The complex order ID can be used to fetch the entire complex order, while individual order IDs can be used to fetch details of specific legs.

## Example Request Body
```json
{
  "type": "OTOCO",
  "trigger-order": {
    "time-in-force": "Day",
    "order-type": "Limit",
    "underlying-symbol": "UA",
    "price": 6.50,
    "price-effect": "Debit",
    "legs": [
      {
        "instrument-type": "Equity",
        "symbol": "UA",
        "quantity": 100,
        "action": "Buy to Open"
      }
    ]
  },
  "orders": [
    {
      "time-in-force": "Day",
      "order-type": "Limit",
      "underlying-symbol": "UA",
      "price": 8,
      "price-effect": "Credit",
      "legs": [
        {
          "instrument-type": "Equity",
          "symbol": "UA",
          "quantity": 100,
          "action": "Sell to Close"
        }
      ]
    },
    {
      "time-in-force": "Day",
      "order-type": "Stop",
      "underlying-symbol": "UA",
      "stop-trigger": 6,
      "legs": [
        {
          "instrument-type": "Equity",
          "symbol": "UA",
          "quantity": 100,
          "action": "Sell to Close"
        }
      ]
    }
  ]
}
```

## Related
*   [[../concepts/complex-orders.md|Complex Orders]]
*   [[../concepts/oto-order.md|OTO Order]]
*   [[../concepts/oco-order.md|OCO Order]]
*   [[../concepts/order-management.md|Order Management]]