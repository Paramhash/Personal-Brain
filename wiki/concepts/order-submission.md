---
tags: ["trading", "api", "orders", "json"]
created: 2023-10-27
reviewed: false
source_origin: "order-submission.md"
---
# Order Submission

Submitting an order via the [[../entities/tastytrade.md|tastytrade]] API involves constructing a specific JSON payload that defines the order's characteristics. This process can be broken down into understanding the overall order attributes and the attributes specific to each leg of the order.

This document clarifies the various attributes required for submitting an order and the rules for structuring the JSON. It focuses exclusively on attributes relevant *before* submission; post-submission attributes like `status` are not covered here.

For a high-level understanding of what an order means within the tastytrade ecosystem, refer to the API Overview's "High-level Concepts: Orders" section.

## Example Multi-leg Equity Option Order

Below is an example of a multi-leg equity option order. This order consists of two legs:
1.  Buying a 197.5 call option.
2.  Selling a 200 call option.

Both options have an expiration date of 2023-08-18 and are for the underlying symbol AAPL. The `action` for both legs is "Open," indicating new positions are being established. A `limit price` of $1.09 Debit is specified for the entire order.

If this order fills, it would result in two new positions: a long 2023-08-18 call option with a 197.5 strike and a short 2023-08-18 call option with a 200 strike.

```json
{   // Order Attributes
    "time-in-force": "Day", // Order will expire when the market closes
    "order-type": "Limit", // Order includes a limit price
    "price": "1.09", // Don't pay more than $1.09 for this trade as a whole
    "price-effect": "Debit", // Account will be debited for this trade
    "legs": [
    {
        // Leg Attributes
        "action": "Buy to Open", // Opening a new long position
        "symbol": "AAPL  230818C00197500", // AAPL Call Option with 197.5 strike price, option expires 2023-08-18
        "quantity": 1, // 1 option contract
        "instrument-type": "Equity Option", // Equity Option instrument
    },
    {
        // Leg Attributes
        "action": "Sell to Open", // Opening a new short position
        "symbol": "AAPL  230818C00200000", // AAPL Call Option with 200 strike price, option expires 2023-08-18
        "quantity": 1, // 1 option contract
        "instrument-type": "Equity Option", // Equity Option instrument
    }
  ]
}
```

The order JSON is typically divided into two main parts:
*   [[./order-attributes.md|Order Attributes]]: Apply to the order as a whole.
*   [[./leg-attributes.md|Leg Attributes]]: Apply to individual instruments within the order.

## Key Concepts for Order Submission

*   [[./order-types.md|Order Types]]
*   [[./price-and-price-effect.md|Price and Price Effect]]
*   [[./time-in-force.md|Time In Force]]
*   [[./value-and-value-effect.md|Value and Value Effect]]
*   [[./order-leg-action.md|Order Leg Action]]
*   [[./instrument-types.md|Instrument Types]]
*   [[./order-quantity.md|Order Quantity]]
*   [[./order-symbol.md|Order Symbol]]
*   [[./advanced-order-instructions.md|Advanced Order Instructions]]
*   [[./complex-orders.md|Complex Orders]]
*   [[./fractional-stock-orders.md|Fractional Stock Orders]]
*   [[./order-responses.md|Order Responses]]

## API Endpoints

Orders are typically submitted to the `POST /accounts/{account_number}/orders` endpoint. For [[./complex-orders.md|Complex Orders]], the `POST /accounts/{account_number}/complex-orders` endpoint is used.

You can also use `/accounts/{account_number}/orders/dry-run` to validate an order without sending it to the market.

---
### Related Concepts
*   [[../entities/tastytrade.md|tastytrade]]
*   [[./order-attributes.md|Order Attributes]]
*   [[./leg-attributes.md|Leg Attributes]]