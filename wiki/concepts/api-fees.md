---
tags: ["trading", "api", "finance", "fees"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# API Fees

API fees refer to the various charges associated with executing trading orders through an API. These fees are typically calculated and presented during the [[../concepts/order-dry-run.md|Order Dry Run]] phase and confirmed upon [[../concepts/submit-order.md|order submission]].

Common types of fees include:

*   **Regulatory Fees**: Charges imposed by regulatory bodies.
*   **Clearing Fees**: Fees for clearing and settlement services.
*   **Commission**: Brokerage commission for executing the trade.
*   **Proprietary Index Option Fees**: Specific fees for trading proprietary index options.
*   **Total Fees**: The sum of all applicable fees.

Each fee component usually has an associated `effect` (Debit or None) indicating whether it reduces the account balance.

## Calculation Example
```json
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
```

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/order-dry-run.md|Order Dry Run]]
*   [[../concepts/submit-order.md|Submit Order]]
*   [[../concepts/buying-power.md|Buying Power]]