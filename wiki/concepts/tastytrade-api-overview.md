---
tags: ["tastytrade", "API", "overview"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Overview

The tastytrade API provides programmatic access to trading functionalities, account information, and market data. This overview serves as a central hub for understanding the core components and concepts of the API.

## Key API Concepts

The tastytrade API is built around several fundamental concepts and conventions:

*   **[[../concepts/tastytrade-api-conventions.md|API Conventions]]**: Details on how to interact with the API, including REST/JSON standards, headers, parameters, and response structures.
*   **[[../concepts/tastytrade-api-versioning.md|API Versioning]]**: Explains how API versions are managed, how to target specific versions, and the deprecation policy.
*   **[[../concepts/tastytrade-api-authentication.md|API Authentication]]**: Covers the OAuth2 flow, access tokens, and how to authenticate requests.
*   **[[../concepts/tastytrade-api-symbology.md|API Symbology]]**: Describes the unique symbol formats used for various tradeable instruments like equities, options, futures, and cryptocurrencies.
*   **[[../concepts/tastytrade-api-error-codes.md|API Error Codes]]**: A guide to common HTTP error codes returned by the API and their meanings.

## High-Level Trading Concepts

Beyond the API mechanics, understanding the core trading concepts is crucial:

*   **[[../concepts/tastytrade-api-orders.md|Orders]]**: The mechanism for initiating and managing trades, including order legs, actions (buy/sell to open/close), and their lifecycle.
*   **[[../concepts/tastytrade-api-positions.md|Positions]]**: Represents your current holdings in various instruments, detailing quantity, direction (long/short), and how they are created or adjusted.
*   **[[../concepts/tastytrade-api-accounts.md|Accounts]]**: Information about your trading accounts, including how multiple accounts are handled.
*   **[[../concepts/tastytrade-api-trading-statuses.md|Trading Statuses]]**: Details on the privileges and capabilities associated with an account, such as eligibility for futures or options trading.
*   **[[../concepts/tastytrade-api-balances.md|Balances]]**: Provides current financial information for an account, including cash, buying power, and net liquidating value.
*   **[[../concepts/tastytrade-api-transactions.md|Transactions]]**: A historical ledger of all account activities that affect your balance, such as order fills, dividends, and fees.
*   **[[../concepts/tastytrade-api-instruments.md|Instruments]]**: The definition of tradeable securities and how they are identified within the API.

This overview provides a starting point for navigating the tastytrade API documentation. Each linked concept note offers a deeper dive into its specific topic.