---
tags: ["tastytrade", "API", "accounts"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Accounts

Your account is a central entity in the tastytrade API, with most endpoints operating in the context of a specific account.

## Key Characteristics

*   **Multiple Accounts**: Customers can open and manage multiple accounts with tastytrade.
*   **Single Account Operations**: Each API endpoint request operates on a single account. You cannot submit an order or perform other actions across multiple accounts in a single HTTP request.
*   **Account Number**: Account numbers are typically required as a path parameter in API requests (e.g., `/accounts/{account_number}/orders`).

## Related Account Concepts

Accounts are linked to several other important concepts within the API:

*   **[[../concepts/tastytrade-api-trading-statuses.md|Trading Statuses]]**: Each account has a trading status that defines its privileges (e.g., eligibility for futures, crypto, or specific options strategies).
*   **[[../concepts/tastytrade-api-balances.md|Balances]]**: Each account has a balance that provides current financial information like cash, buying power, and net liquidating value.
*   **[[../concepts/tastytrade-api-transactions.md|Transactions]]**: A historical ledger of all activities affecting an account's balance.

For more detailed information, refer to the tastytrade "Customer Account Information Api Guide."

This concept is fundamental to the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].