---
tags: ["trading", "account", "finance"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Buying Power

Buying power represents the total amount of money an investor has available to purchase securities. In the context of [[../concepts/order-management.md|order management]], it is a critical factor in determining whether an order can be placed.

## Impact of Orders

When an order is submitted or evaluated via an [[../concepts/order-dry-run.md|Order Dry Run]], the system calculates its impact on the account's buying power. This calculation typically includes:

*   **Change in Margin Requirement**: The amount of margin required for the new order.
*   **Change in Buying Power**: The net change in available buying power.
*   **Current Buying Power**: The buying power before the order.
*   **New Buying Power**: The projected buying power after the order.
*   **Isolated Order Margin Requirement**: Margin specific to the individual order.

The `effect` (Debit or Credit) indicates whether the buying power is decreased or increased by the transaction.

## Validation

During an [[../concepts/order-dry-run.md|Order Dry Run]], the system verifies that the account has sufficient buying power to afford the order. If not, a warning will be issued, and attempting to [[../concepts/submit-order.md|submit the order]] will result in rejection.

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/order-dry-run.md|Order Dry Run]]
*   [[../concepts/submit-order.md|Submit Order]]
*   [[../concepts/api-fees.md|API Fees]]