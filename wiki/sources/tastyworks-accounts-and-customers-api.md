---
tags: ["api", "tastyworks", "brokerage", "customer-data", "account-data", "market-data"]
created: 2023-10-27
reviewed: false
source_origin: "accounts-and-customers.md"
---
# Tastyworks Accounts and Customers API

The Tastyworks Accounts and Customers API provides a comprehensive set of endpoints for managing and retrieving customer profile information, associated account details, and credentials for real-time market data streaming. It serves as a foundational API, typically being among the first endpoints called after authentication to discover a customer's accounts and obtain market data access.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 9.25.0

**Note on `customer_id`:** For all customer-related endpoints, the literal string `me` can be used in place of a specific `customer_id` path parameter. This allows referencing the currently authenticated customer without needing to know or store their internal identifier.

## Key Endpoints

*   **Get API Quote Tokens:** Retrieves the necessary URL and authentication token for connecting to the real-time market data WebSocket streamer.
    *   See: [[../concepts/api-quote-tokens.md]]
*   **Get Customer:** Retrieves the full profile for a specific customer.
    *   See: [[../concepts/customer-profile.md]]
*   **Get Customer Accounts:** Retrieves all accounts associated with a customer, including their authority level on each account.
    *   See: [[../concepts/account-management.md]]
*   **Get Specific Account:** Retrieves full details for a particular account belonging to a customer.
    *   See: [[../concepts/account-management.md]]

## Data Models

This API primarily utilizes the following data models:

*   **Customer:** Represents a full customer profile, including personal, contact, and regulatory information.
    *   See: [[../concepts/customer-profile.md]]
*   **Account:** Describes a tastytrade brokerage account and its configuration.
    *   See: [[../concepts/account-management.md]]
*   **AccountAuthorityDecorator:** Wraps an `Account` object with the customer's authority level for that account.
    *   See: [[../concepts/account-management.md]]
*   **QuoteStreamerTokenAuthResult:** The response object for obtaining market data streaming tokens.
    *   See: [[../concepts/api-quote-tokens.md]]

## Common Use Cases

*   **Session Bootstrap:** After authentication, call `GET /customers/me/accounts` to discover all accounts the user has access to. These account numbers are then used for subsequent API calls across other Tastyworks APIs.
*   **Market Data Streaming Setup:** Call `GET /api-quote-tokens` to obtain the DXLink WebSocket URL and token, then connect to the streamer for real-time quotes. For more details, see [[../concepts/dxlink-streaming.md]].
*   **Account Selection UI:** Utilize fields like `account-type-name`, `nickname`, `margin-or-cash`, and `authority-level` from the `Account` and `AccountAuthorityDecorator` objects to present a user-friendly account selector in applications.
*   **Pre-Trade Checks:** Use `is-futures-approved` and `suitable-options-level` from the `Account` object to determine which products an account is eligible to trade before presenting order entry options.
*   **Professional Data Classification:** Check the `is-professional` and `has-delayed-quotes` fields within the `Customer` profile to determine the appropriate market data billing tier and whether the user receives real-time or delayed data.

---