---
tags: ["tastytrade", "api", "order", "schema", "response"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# tastytrade PlacedOrderResponse Object

The `PlacedOrderResponse` object is returned by order submission endpoints (`POST /accounts/{account_number}/orders`, `POST /accounts/{account_number}/complex-orders`) and their corresponding dry-run endpoints. It provides details about the order that was placed or validated, including its status, buying power effect, fees, and any warnings or errors.

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `order` | [[../concepts/tastytrade-order-object.md]] | The created or validated single order object |
| `complex-order` | [[../concepts/tastytrade-complex-order-object.md]] | The complex order object (if submitting a complex order) |
| `buying-power-effect` | string | The impact on the account's buying power (formatted as a string with the amount and direction) |
| `fee-calculation` | string | Estimated fees for the order |
| `closing-fee-calculation` | string | Estimated fees specific to closing transactions |
| `warnings` | array | Non-blocking warnings about the order |
| `errors` | array | Blocking errors that prevent the order from being placed |
| `notes` | array | Informational notes about the order |

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-order-object.md]]
*   [[../concepts/tastytrade-complex-order-object.md]]
---