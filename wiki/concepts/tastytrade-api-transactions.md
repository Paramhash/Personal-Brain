---
tags: ["tastytrade", "API", "transactions", "accounts", "history"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Transactions

tastytrade maintains a historical ledger of all activities that affect an [[../concepts/tastytrade-api-accounts.md|account's balance]]. Each of these account activities is recorded as a transaction.

## Purpose

Transactions provide a detailed audit trail of all financial movements and events within an account. They are crucial for reconciliation, reporting, and understanding the history of an account's [[../concepts/tastytrade-api-balances.md|balances]].

## Examples of Transactions

Common types of transactions include:

*   **Order Fills**: Records of when [[../concepts/tastytrade-api-orders.md|orders]] are executed.
*   **Dividends**: Payments received from stock holdings.
*   **Fees**: Charges incurred, such as trading commissions or regulatory fees.
*   **Cash Deposits**: Funds added to the account.
*   **Cash Withdrawals**: Funds removed from the account.
*   **Interest**: Interest earned or paid.
*   **Corporate Actions**: Events like stock splits or mergers.

For more detailed information, refer to the tastytrade "Account Transactions Api Guide."

This concept is integral to understanding the financial history of [[../concepts/tastytrade-api-accounts.md|Accounts]] and complements [[../concepts/tastytrade-api-balances.md|Balances]] within the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].