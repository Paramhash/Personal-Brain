---
tags: ["trading", "order-management", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "order-flow-raw-payload.md"
---
# Order Flow (tastytrade)

Order flow in the [[../entities/tastytrade.md|tastytrade]] system describes the lifecycle of an order, from its initial submission to its final resolution. Orders can undergo various status changes, which are grouped into three main phases to help traders understand their progression:

1.  [[../concepts/order-status-submission-phase.md|Submission Phase]]
2.  [[../concepts/order-status-working-phase.md|Working Phase]]
3.  [[../concepts/order-status-terminal-phase.md|Terminal Phase]]

Understanding these phases and the associated statuses is crucial for managing trades effectively.

## Order Status Definitions

| Status            | Meaning                                                                                                                            | Terminal |
| :---------------- | :--------------------------------------------------------------------------------------------------------------------------------- | :------- |
| Received          | Initial order state, typically when markets are closed.                                                                            | No       |
| Routed            | Order is currently being submitted from tastytrade's system to an exchange.                                                        | No       |
| In Flight         | Order has left tastytrade's system and is awaiting confirmation of receipt from the exchange.                                      | No       |
| Live              | Order has been received by the exchange and is actively working.                                                                   | No       |
| Cancel Requested  | Customer has requested to cancel the order, awaiting confirmation from the exchange.                                               | No       |
| Replace Requested | Customer has submitted a replacement order. The original order is awaiting cancellation confirmation from the exchange.            | No       |
| Contingent        | Order is awaiting a status update of a related order (e.g., replacement orders, OTOCO, OTO orders).                                | No       |
| Filled            | Order has been fully executed.                                                                                                     | Yes      |
| Canceled          | Order has been canceled by the user or system.                                                                                     | Yes      |
| Expired           | Order has expired, typically for day orders that don't fill by market close.                                                       | Yes      |
| Rejected          | Order has been rejected by either tastytrade or the exchange (e.g., insufficient buying power, invalid symbol).                    | Yes      |
| Removed           | Administrator has manually removed this order from the customer account.                                                           | Yes      |
| Partially Removed | Administrator has manually removed part of this order from the customer account.                                                   | Yes      |

## Examples of Order Status Transitions

### 1. Immediate Fill (Market Order)

A market order to buy shares that fills instantly:

`Received` → `Routed` → `In Flight` → `Live` → `Filled`

### 2. Canceled by Customer (Limit Order)

A limit order that doesn't fill immediately and is subsequently canceled:

`Received` → `Routed` → `In Flight` → `Live` → `Cancel Requested` → `Canceled`

### 3. Expired Day Order

A limit order with a "Day" time-in-force that doesn't fill by market close:

`Received` → `Routed` → `In Flight` → `Live` → `Expired`

### 4. Rejected by Brokerage

An order for an already expired option, rejected by the tastytrade system:

`Received` → `Rejected`

---
This document summarizes the order flow process within the [[../entities/tastytrade.md|tastytrade]] system, drawing information from the original [[../sources/order-flow-raw-payload.md|Order Flow Raw Payload]].