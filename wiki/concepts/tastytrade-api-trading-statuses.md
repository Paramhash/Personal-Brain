---
tags: ["tastytrade", "API", "trading", "accounts", "privileges"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Trading Statuses

Each [[../concepts/tastytrade-api-accounts.md|tastytrade account]] is associated with a single trading status. This status defines the specific trading privileges and capabilities granted to that account.

## Purpose

The trading status provides information on:

*   **Instrument Eligibility**: Whether the account is permitted to trade certain types of [[../concepts/tastytrade-api-instruments.md|instruments]], such as futures or cryptocurrencies.
*   **Strategy Eligibility**: Which options trading strategies (e.g., naked puts, iron condors) the account is authorized to execute.

## Impact on API Usage

The trading status directly influences which trading actions an account can successfully perform via the API. Attempts to execute trades for which an account lacks the necessary privileges may result in [[../concepts/tastytrade-api-error-codes.md|error codes]] like `403 Forbidden` or `422 Unprocessable Content`.

For more detailed information, refer to the tastytrade "Account Trading Status Api Guide."

This concept is an important aspect of [[../concepts/tastytrade-api-accounts.md|Accounts]] and is part of the broader [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].