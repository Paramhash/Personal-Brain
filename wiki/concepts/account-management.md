---
tags: ["account", "brokerage-account", "api-model", "tastyworks", "trading", "suitability"]
created: 2023-10-27
reviewed: false
source_origin: "accounts-and-customers.md"
---
# Account Management (Tastyworks API)

The Account Management concept in the Tastyworks API focuses on retrieving and understanding brokerage account details. It involves the `Account` and `AccountAuthorityDecorator` data models, and the `GET /customers/{customer_id}/accounts` and `GET /customers/{customer_id}/accounts/{account_number}` endpoints.

## Get Customer Accounts Endpoint

Retrieves all accounts associated with a customer, including the authority level the customer has on each account.

**Request**

```
GET /customers/{customer_id}/accounts
```

**Path Parameters**

*   `customer_id` (string, Required): The customer identifier, or `me` for the currently authenticated customer.

**Response** — `200 OK`

Returns an array of `AccountAuthorityDecorator` objects.

**Example Response**

```json
{
  "data": {
    "items": [
      {
        "account": {
          "account-number": "5WX34382",
          "account-type-name": "Individual",
          "margin-or-cash": "Margin",
          "is-closed": false,
          "is-futures-approved": true,
          "day-trader-status": "false",
          "opened-at": "2023-06-15T00:00:00.000+00:00",
          "nickname": "Main Trading",
          "investment-objective": "GROWTH",
          "risk-tolerance": "HIGH"
        },
        "authority-level": "owner"
      },
      {
        "account": {
          "account-number": "5WZ29543",
          "account-type-name": "Individual",
          "margin-or-cash": "Cash",
          "is-closed": false,
          "is-futures-approved": false,
          "day-trader-status": "false",
          "opened-at": "2024-01-10T00:00:00.000+00:00",
          "nickname": "Cash Account"
        },
        "authority-level": "owner"
      }
    ]
  }
}
```

## Get Specific Account Endpoint

Retrieves full details for a specific account under a customer.

**Request**

```
GET /customers/{customer_id}/accounts/{account_number}
```

**Path Parameters**

*   `customer_id` (string, Required): The customer identifier, or `me` for the currently authenticated customer.
*   `account_number` (string, Required): The tastytrade account number.

**Response** — `200 OK`

Returns a single `Account` object.

## Data Models

### AccountAuthorityDecorator

This object wraps an `Account` object with the customer's authority level on that specific account.

*   `account` (Account): The full account object.
*   `authority-level` (string): The customer's authority on this account (e.g., `owner`, `power-of-attorney`, `custodian`).

### Account

The `Account` object describes a tastytrade brokerage account and its configuration.

#### Core Identification

*   `account-number` (string): The tastytrade account number (e.g., `5WX34382`).
*   `account-type-name` (string): The account type (e.g., `Individual`, `Joint`, `IRA`, `Entity`).
*   `nickname` (string): User-assigned nickname for the account.
*   `external-id` (string): External identifier for the account.
*   `ext-account-id` (string): External account identifier used in partner integrations.
*   `ext-crm-id` (string): External CRM identifier.
*   `external-fdid` (string): External FDID (Financial Data Identifier).
*   `submitting-user-id` (string): The user ID that submitted the account application.

#### Account Status

*   `margin-or-cash` (string): Whether the account is a `Margin` or `Cash` account.
*   `is-closed` (boolean): Whether the account has been closed.
*   `closed-at` (datetime): Timestamp when the account was closed (null if open).
*   `created-at` (datetime): Timestamp when the account record was created.
*   `opened-at` (datetime): Timestamp when the account was opened.
*   `funding-date` (date): The date the account was first funded.
*   `is-firm-error` (boolean): Whether the account is a firm error account.
*   `is-firm-proprietary` (boolean): Whether the account is a firm proprietary account.
*   `is-foreign` (string): Whether the account belongs to a foreign (non-US) customer.
*   `regulatory-domain` (string): The regulatory domain for the account (e.g., US).

#### Trading Configuration

*   `day-trader-status` (string): The account's day trader status designation.
*   `is-futures-approved` (boolean): Whether the account is approved for futures trading.
*   `futures-account-purpose` (string): The stated purpose for the futures account (if futures-approved).
*   `suitable-options-level` (string): The options level the account is suitable for based on suitability responses.

#### Suitability & Investment Profile

*   `investment-objective` (string): The customer's stated investment objective (e.g., `GROWTH`, `INCOME`, `SPECULATION`).
*   `investment-time-horizon` (string): The customer's investment time horizon (e.g., `SHORT_TERM`, `AVERAGE`, `LONGEST`).
*   `liquidity-needs` (string): The customer's stated liquidity needs.
*   `risk-tolerance` (string): The customer's stated risk tolerance (e.g., `LOW`, `MEDIUM`, `HIGH`).

These accounts are associated with a [[../concepts/customer-profile.md]].

---