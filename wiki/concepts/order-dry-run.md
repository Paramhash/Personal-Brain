---
tags: ["trading", "api", "orders", "validation"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Order Dry Run

The "Order Dry Run" functionality allows users to verify the validity and potential impact of an order on their account without actually submitting it for execution. This is a critical step for pre-validation and understanding the financial implications of a trade.

## Key Considerations

The system evaluates two primary factors during a dry run:

1.  **Order Validity**: Numerous checks are performed to ensure the order adheres to trading rules and system constraints. Examples include:
    *   Validating symbols.
    *   Checking for expired options.
    *   Verifying that a position exists if the order is intended to close one.
    *   Detecting conflicts with existing working orders.

2.  **Account State**: The system assesses the account's financial standing.
    *   **[[../concepts/buying-power.md|Buying Power]]**: Ensures sufficient buying power is available to cover the order's cost.
    *   Account Status: Confirms the account is in good standing with the platform (e.g., [[../entities/tastytrade.md|tastytrade]]).

## Warnings and Rejection

The dry run endpoint will return warnings in its response if any issues are detected with the order or the account. If an order with such warnings is subsequently submitted via the actual order submission endpoint, it will be rejected, and an error message will be returned in the HTTP response.

## API Endpoint
`POST /accounts/{account_number}/orders/dry-run`

## Response Example (showing buying power and fees)
```json
{
    "data": {
        "order": { /* ... order details ... */ },
        "warnings": [],
        "buying-power-effect": {
            "change-in-margin-requirement": "300.0",
            "change-in-margin-requirement-effect": "Debit",
            "change-in-buying-power": "102.302",
            "change-in-buying-power-effect": "Debit",
            "current-buying-power": "8995981.2613",
            "current-buying-power-effect": "Credit",
            "new-buying-power": "8995878.9593",
            "new-buying-power-effect": "Credit",
            "isolated-order-margin-requirement": "300.0",
            "isolated-order-margin-requirement-effect": "Debit",
            "is-spread": true,
            "impact": "102.302",
            "effect": "Debit"
        },
        "fee-calculation": {
            "regulatory-fees": "0.102",
            "regulatory-fees-effect": "Debit",
            "clearing-fees": "0.2",
            "clearing-fees-effect": "Debit",
            "commission": "2.0",
            "commission-effect": "Debit",
            "proprietary-index-option-fees": "0.0",
            "proprietary-index-option-fees-effect": "Debit",
            "total-fees": "2.302",
            "total-fees-effect": "Debit"
        }
    },
    "api-version": "v1",
    "context": "/accounts/5WT0001/orders/dry-run"
}
```

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/submit-order.md|Submit Order]]
*   [[../concepts/buying-power.md|Buying Power]]
*   [[../concepts/api-fees.md|API Fees]]
*   [[../sources/order-submission-guide.md|Order Submission Guide]]