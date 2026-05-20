---
tags: []
created: 2023-10-27
reviewed: false
source_origin: "transactions.md"
---
# Debit and Credit Effects (Financial)

In financial accounting, **Debit** and **Credit** are fundamental terms used to describe the two sides of every financial transaction and their effect on account balances. They are not inherently "good" or "bad" but rather indicate the direction of a transaction's impact.

*   **Debit:**
    *   Generally, a debit increases asset and expense accounts, and decreases liability, equity, and revenue accounts.
    *   In the context of the [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md), a `Debit` effect typically signifies a reduction in the account's cash value or an increase in an obligation. Examples include fees charged, purchases of securities, or withdrawals.
*   **Credit:**
    *   Generally, a credit increases liability, equity, and revenue accounts, and decreases asset and expense accounts.
    *   In the context of the [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md), a `Credit` effect typically signifies an increase in the account's cash value. Examples include proceeds from selling securities, dividend payments received, or deposits.

## Tastyworks Transactions API Usage

The [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md) extensively uses `Debit` and `Credit` to clarify the impact of monetary values within a [Transaction](../concepts/transaction.md) object. Many fields representing monetary amounts have a corresponding `*-effect` field (e.g., `value-effect`, `net-value-effect`, `commission-effect`, `regulatory-fees-effect`, `other-charge-effect`).

For instance:
*   A `commission` will typically have a `commission-effect` of `Debit`.
*   A `dividend` payment (part of a `Transaction`) would contribute to a `value-effect` of `Credit`.

Understanding these effect fields is crucial for accurately interpreting transaction data and performing calculations like profit and loss (P&L) or [financial fees](../concepts/financial-fees.md) analysis.

---
**Source:** [Tastyworks Transactions API Documentation](../sources/tastyworks-transactions-api-docs.md)