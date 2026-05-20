---
tags: ["trading", "api", "orders", "execution"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Submit Order

The "Submit Order" functionality is used to send a validated trading order to the exchange for execution. The requirements for structuring the order JSON are identical to those used for the [[../concepts/order-dry-run.md|Order Dry Run]] endpoint.

Upon successful submission, the API response will include a unique `id` for the order, which can then be used for subsequent operations such as looking up its [[../concepts/order-status.md|status]] or requesting its [[../concepts/cancel-order.md|cancellation]].

## API Endpoint
`POST /accounts/{account_number}/orders`

## Request Body
The request body is the same JSON structure as used for the [[../concepts/order-dry-run.md|Order Dry Run]] endpoint.

## Response Example
```json
{
    "data": {
        "order": {
            "id": 771043,
            "account-number": "5WT0001",
            "time-in-force": "Day",
            "order-type": "Limit",
            "size": 1,
            "underlying-symbol": "SPY",
            "price": "3.0",
            "price-effect": "Credit",
            "status": "Routed",
            "cancellable": false,
            "editable": false,
            "edited": false,
            "received-at": "2019-10-01T18:26:52.513+00:00",
            "updated-at": 1569954412572,
            "legs": [
                {
                    "instrument-type": "Equity Option",
                    "symbol": "SPY   191018C00295000",
                    "quantity": 1,
                    "remaining-quantity": 1,
                    "action": "Sell to Open",
                    "fills": []
                }
            ]
        },
        "warnings": [],
        "buying-power-effect": { /* ... buying power details ... */ },
        "fee-calculation": { /* ... fee details ... */ }
    },
    "api-version": "v1",
    "context": "/accounts/5WT0001/orders/"
}
```

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/order-dry-run.md|Order Dry Run]]
*   [[../concepts/cancel-order.md|Cancel Order]]
*   [[../concepts/order-status.md|Order Status]]
*   [[../sources/order-submission-guide.md|Order Submission Guide]]