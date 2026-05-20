---
tags: []
created: 2023-10-27
reviewed: false
source_origin: "transactions.md"
---
# Tastyworks Transactions API

The Tastyworks Transactions API provides endpoints for retrieving a tastytrade account's complete transaction history. This includes a wide range of account activities such as trades, dividends, interest, fees, and transfers, serving as the definitive record of what happened in an account, including fill prices, commissions, and regulatory fees.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 9.1.2

## Endpoints

The API exposes several endpoints to interact with transaction data:

*   **Search Transactions:**
    *   `GET /accounts/{account_number}/transactions`
    *   Returns a paginated list of transactions for an account.
    *   Supports extensive filtering by date range, symbol, instrument type, transaction type, action, currency, and more.
    *   See also: [API Pagination](../concepts/api-pagination.md)
*   **Get Transaction by ID:**
    *   `GET /accounts/{account_number}/transactions/{id}`
    *   Retrieves a single, specific [Transaction](../concepts/transaction.md) record using its unique identifier.
*   **Get Total Fees:**
    *   `GET /accounts/{account_number}/transactions/total-fees`
    *   Returns the aggregated total [financial fees](../concepts/financial-fees.md) charged for an account on a specified day.

## Common Use Cases

The Transactions API supports various analytical and reporting needs:

*   **Trade History Report:** Fetch all trades for a specific date range.
*   **P&L Calculation:** Utilize `value`, `value-effect`, `commission`, and `regulatory-fees` from [Transaction](../concepts/transaction.md) objects to calculate net realized Profit & Loss.
*   **Fee Analysis:** Retrieve daily fee summaries or break down individual [financial fees](../concepts/financial-fees.md) by type.
*   **Dividend Tracking:** Filter transactions to specifically track dividend payments received.
*   **Options Assignment/Expiration History:** Identify options that were assigned or expired.
*   **Symbol-Specific History:** Obtain all activity (stock trades, option trades, etc.) related to a single underlying symbol.

## Important Notes

*   **Pagination Limits:** The API supports [API Pagination](../concepts/api-pagination.md) with a maximum of 2,000 results per page. For accounts with high activity, it's crucial to use date ranges and pagination to retrieve complete history.
*   **Effect Fields:** Every monetary value in a [Transaction](../concepts/transaction.md) object has a corresponding `*-effect` field (e.g., `value-effect`, `commission-effect`) indicating whether the value is a [Debit or Credit](../concepts/debit-credit-effect.md) to the account.
*   **Net Value:** The `net-value` field provides the transaction value *after* all associated [financial fees](../concepts/financial-fees.md) have been applied. This field is recommended for accurate P&L calculations.
*   **Cost Basis Reconciliation:** [Cost basis](../concepts/cost-basis.md) data may have a slight delay (up to a day) due to nightly reconciliation processes with the clearing firm. The `cost-basis-reconciliation-date` field indicates the most recent reconciliation.
*   **Transaction Types vs. Sub-types:** `transaction-type` provides a broad category (e.g., `Trade`, `Dividend`), while `transaction-sub-type` offers more specific details (e.g., `Sell to Open`, `Assignment`, `Expiration`).

---
**Source:** [Tastyworks Transactions API Documentation](../sources/tastyworks-transactions-api-docs.md)