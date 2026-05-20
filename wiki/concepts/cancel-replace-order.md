---
tags: ["trading", "api", "orders", "modification"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Cancel Replace Order

The "Cancel Replace Order" functionality allows users to modify certain parameters of an existing working order. This operation effectively cancels the original order and submits a new one with the specified changes.

## Modifiable Parameters

When performing a cancel/replace operation, only the following body parameters are typically allowed to be changed:

*   `price`
*   `order-type`
*   `time-in-force`

All other fields in the JSON request body, particularly the order legs and underlying instrument details, must remain identical to the original order being replaced.

## API Endpoint
`PUT /accounts/{account_number}/orders/{id}`

## Request Body Example
```json
{
  "time-in-force": "Day",
  "order-type": "Limit",
  "price": "3.0",
  "price-effect": "Credit",
  "legs": [
     {
     "instrument-type": "Equity Option",
      "symbol": "SPY   191018C00299000",
      "quantity": 1,
      "action": "Buy to Open"
     },
     {
     "instrument-type": "Equity Option",
      "symbol": "SPY   191018C00295000",
      "quantity": 1,
      "action": "Sell to Open"
    }
  ]
}
```

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/cancel-order.md|Cancel Order]]
*   [[../concepts/submit-order.md|Submit Order]]