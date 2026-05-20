---
tags: ["tastytrade", "api", "order", "status"]
created: 2023-10-27
reviewed: false
source_origin: "orders.md"
---
# tastytrade Order Status Values

This document lists and describes the possible status values for an order within the tastytrade Orders API. These statuses are found in the `status` field of the [[../concepts/tastytrade-order-object.md]].

| Status | Terminal? | Description |
|--------|-----------|-------------|
| `Received` | No | Order received by the system, not yet routed |
| `Routed` | No | Order has been routed to the exchange |
| `In Flight` | No | Order is in flight to the exchange |
| `Live` | No | Order is live and working on the exchange |
| `Contingent` | No | Order is contingent on another event (e.g., part of OTO waiting for trigger) |
| `Filled` | Yes | Order has been completely filled |
| `Cancelled` | Yes | Order was cancelled |
| `Expired` | Yes | Order expired (e.g., Day order at market close) |
| `Rejected` | Yes | Order was rejected (see `reject-reason` for details in the [[../concepts/tastytrade-order-object.md]]) |
| `Remove Pending` | No | Cancellation is pending |
| `Dead` | Yes | Order is dead (terminal, no fills) |

---
**See also:**
*   [[../entities/tastytrade-orders-api.md]]
*   [[../concepts/tastytrade-order-object.md]]
---