---
tags: ["trading", "api", "orders", "real-time"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Live Orders

The "Live Orders" endpoint provides a snapshot of orders that were created or updated today, including those with various [[../concepts/order-status.md|statuses]] such as "Live", "Cancelled", "Rejected", or "Filled". It also includes GTC (Good 'Til Cancelled) orders that remain active from previous days.

**Important Note on Polling:**
It is strongly advised **not** to repeatedly poll the `GET /accounts/{account_number}/orders/live` endpoint for real-time updates. Excessive polling can degrade platform performance and may lead to API throttling or suspension. For real-time order status updates, users should leverage the [[../entities/account-streamer.md|Account Streamer]], which delivers updates with lower latency and without rate-limit concerns.

## API Endpoint
`GET /accounts/{account_number}/orders/live`

## Response Example
```json
{
    "data": {
        "items": [
            {
                "id": 54758826,
                "account-number": "5WT00001",
                "time-in-force": "GTC",
                "order-type": "Limit",
                "size": 1,
                "underlying-symbol": "QQQ",
                "price": "3.0",
                "price-effect": "Debit",
                "status": "Live",
                "cancellable": true,
                "editable": true,
                "edited": false,
                "legs": [
                    {
                        "instrument-type": "Equity Option",
                        "symbol": "QQQ   191115C00187000",
                        "quantity": 1,
                        "remaining-quantity": 1,
                        "action": "Buy to Close",
                        "fills": []
                    }
                ]
            }
            // ... other orders
        ]
    },
    "api-version": "v1",
    "context": "/accounts/5WT05758/orders/live"
}
```

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/search-orders.md|Search Orders]]
*   [[../entities/account-streamer.md|Account Streamer]]
*   [[../concepts/order-status.md|Order Status]]