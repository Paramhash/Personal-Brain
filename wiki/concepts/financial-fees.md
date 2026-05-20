---
tags: []
created: 2023-10-27
reviewed: false
source_origin: "transactions.md"
---
# Financial Fees

**Financial fees** are charges levied by financial institutions for various services, transactions, or account maintenance. These fees can impact the net value of a transaction or the overall profitability of an investment.

## Types of Fees in Tastyworks Transactions API

The [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md) provides detailed breakdowns of various fees associated with a [Transaction](../concepts/transaction.md) object. Each monetary fee field includes a corresponding `*-effect` field (e.g., `commission-effect`) indicating whether it's a [Debit or Credit](../concepts/debit-credit-effect.md) to the account. Fees typically have a `Debit` effect, reducing the account's value.

Common fee types include:

*   **Commission:** A charge for executing a trade.
*   **Clearing Fees:** Fees associated with the clearing and settlement process of a trade.
*   **Regulatory Fees:** Charges imposed by regulatory bodies, such as SEC (Securities and Exchange Commission) fees or TAF (Trading Activity Fee).
*   **Proprietary Index Option Fees:** Specific fees applied to transactions involving proprietary index options (ee.g., SPX, VIX).
*   **Currency Conversion Fees:** Charges incurred when converting funds between different currencies.
*   **Other Charge:** Any other miscellaneous charges, often accompanied by an `other-charge-description`.
*   **`is-estimated-fee`:** A boolean field indicating if the fee amounts are estimated and may be subject to later reconciliation.

## API Endpoint for Total Fees

The [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md) offers a dedicated endpoint to quickly retrieve aggregated fee information:

*   `GET /accounts/{account_number}/transactions/total-fees`
    *   Returns the total fee amount charged for an account on a specified day.

## Impact on Net Value

The `net-value` field within a [Transaction](../concepts/transaction.md) object in the Tastyworks API represents the transaction's total value *after* all associated fees have been deducted. This field is crucial for accurate profit and loss (P&L) calculations, as it accounts for the true cost of the transaction.

---
**Source:** [Tastyworks Transactions API Documentation](../sources/tastyworks-transactions-api-docs.md)