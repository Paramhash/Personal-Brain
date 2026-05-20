---
tags: ["tastytrade", "api", "websocket", "notifications", "data-structure", "json"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/tastytrade-streaming-account-data-doc.md"
---
# tastytrade Streamer Notification Structure

Notifications received from the [[./tastytrade-account-streamer.md|tastytrade Account Streamer]] adhere to a consistent JSON object representation. A key characteristic of these messages is that they always contain a **full object representation**, rather than partial or differential updates. This means each notification provides the complete state of the updated entity at the time of the event.

## Common Notification Structure

Every message published via the streamer will have the following top-level keys:

*   **`type`**: A string key that corresponds to the class of data being provided (e.g., `'Order'`, `'Balance'`, `'Position'`). This helps clients identify the type of entity being updated.
*   **`data`**: A JSON object containing the full representation of the updated entity. The structure of this object will vary depending on the `type` of notification.
*   **`timestamp`**: A numerical timestamp (e.g., Unix epoch milliseconds) indicating when the notification was generated.

## Example: Order Notification

Below is an example of an `Order` notification, demonstrating the `type`, `data`, and `timestamp` keys. The `data` field contains the complete order object with its current status and details.

```json
{
  "type": "Order",
  "data": {
    "id": 1,
    "account-number": "5WT00000",
    "time-in-force": "Day",
    "order-type": "Market",
    "size": 100,
    "underlying-symbol": "AAPL",
    "underlying-instrument-type": "Equity",
    "status": "Live",
    "cancellable": true,
    "editable": true,
    "edited": false,
    "legs": [
        {
            "instrument-type": "Equity",
            "symbol": "AAPL",
            "quantity": 100,
            "remaining-quantity": 100,
            "action": "Buy to Open",
            "fills": []
        }
    ]
  },
  "timestamp": 1688595114405
}
```

This structure ensures that clients always receive comprehensive information about the state change, simplifying parsing and state management on the client side. For specific behaviors related to order fills, refer to [[./tastytrade-order-fill-processing-nuances.md|tastytrade Order Fill Processing Nuances]].

---
*Source: [[../sources/tastytrade-streaming-account-data-doc.md|tastytrade Streaming Account Data Documentation]]*