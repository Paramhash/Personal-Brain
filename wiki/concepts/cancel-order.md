---
tags: ["trading", "api", "orders", "cancellation"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Cancel Order

The "Cancel Order" functionality allows users to request the cancellation of an existing trading order.

## Behavior

*   **Terminal Status**: If an order is already in a terminal [[../concepts/order-status.md|status]] (e.g., "Filled", "Rejected"), the cancellation request will fail, returning an HTTP 422 error with a message like `"the order could not be cancelled"`. Refer to the [[../sources/order-flow-guide.md|Order Flow Guide]] for more information on terminal statuses.
*   **Successful Request**: For successful cancellation requests, the order's [[../concepts/order-status.md|status]] will transition to "Cancel Requested". This indicates that the system is attempting to cancel the order with the exchange.
*   **Real-time Updates**: Users should expect to receive a notification via the [[../entities/account-streamer.md|Account Streamer]] when the order officially transitions to a "Cancelled" status.

## API Endpoint
`DELETE /accounts/{account_number}/orders/{id}`

## Path Parameters
*   **`account-number`** (String): The account number the order belongs to.
*   **`id`** (Integer): The unique identifier of the order to be cancelled.

## Response Example
```json
{
    "data": {
        "id": 12345,
        "account-number": "5WT00001",
        "time-in-force": "Day",
        "order-type": "Limit",
        "size": 1,
        "underlying-symbol": "AAPL",
        "underlying-instrument-type": "Equity",
        "price": "100.0",
        "price-effect": "Debit",
        "status": "Cancel Requested",
        "cancellable": false,
        "editable": false,
        "edited": false,
        "received-at": "2023-07-31T15:33:45.899+00:00",
        "updated-at": 1690817636722,
        "legs": [
            {
                "instrument-type": "Equity",
                "symbol": "AAPL",
                "quantity": 1,
                "remaining-quantity": 1,
                "action": "Buy to Open",
                "fills": []
            }
        ]
    },
    "context": "/accounts/5WT00001/orders/12345"
}
```

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/submit-order.md|Submit Order]]
*   [[../concepts/cancel-replace-order.md|Cancel Replace Order]]
*   [[../concepts/order-status.md|Order Status]]
*   [[../entities/account-streamer.md|Account Streamer]]
*   [[../sources/order-flow-guide.md|Order Flow Guide]]