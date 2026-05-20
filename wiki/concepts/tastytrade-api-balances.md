---
tags: ["tastytrade", "API", "balances", "accounts", "financial"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Balances

Each [[../concepts/tastytrade-api-accounts.md|tastytrade account]] is linked to a single account balance, which provides a snapshot of its current financial state.

## Information Provided

The account balance includes critical financial data such as:

*   **Cash**: Available cash in the account.
*   **Buying Power**: The amount of capital available for new trades.
*   **Value of Long/Short Positions**: The current market value of all [[../concepts/tastytrade-api-positions.md|long]] and [[../concepts/tastytrade-api-positions.md|short positions]].
*   **Net Liquidating Value**: The total value of the account if all positions were closed at current market prices.
*   And other relevant financial metrics.

## Updates

Account balances are dynamically updated in response to various account activities, including:

*   **Order Fills**: When an [[../concepts/tastytrade-api-orders.md|order]] is executed.
*   **Cash Deposits/Withdrawals**: Funds moving in or out of the account.
*   **Dividends/Interest**: Income or expenses related to holdings.
*   **Fees**: Trading commissions or other charges.

For more detailed information, refer to the tastytrade "Account Balances Api Guide."

This concept is closely related to [[../concepts/tastytrade-api-accounts.md|Accounts]] and [[../concepts/tastytrade-api-transactions.md|Transactions]], forming a key part of the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].