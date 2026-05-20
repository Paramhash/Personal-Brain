---
tags: []
created: 2023-10-27
reviewed: false
source_origin: "transactions.md"
---
# Tastyworks Transactions API Documentation

This document serves as a source reference for the official documentation of the [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md). It details the API's functionality for retrieving an account's transaction history, including various types of account activity, execution details, and associated costs.

## Key Information Covered

*   **API Overview:** Purpose, base URL, authentication requirements, and API version.
*   **Endpoints:** Detailed descriptions of the `Search Transactions`, `Get Transaction by ID`, and `Get Total Fees` endpoints, including request parameters (path, query) and expected responses.
*   **Data Models:** Comprehensive schema for the [Transaction](../concepts/transaction.md) object, outlining its core fields, instrument details, execution specifics, [financial fees](../concepts/financial-fees.md) and commissions, pricing, [cost basis](../concepts/cost-basis.md) information, and external identifiers.
*   **Common Use Cases:** Practical examples of how to leverage the API for tasks such as trade history reporting, P&L calculation, fee analysis, dividend tracking, and options assignment/expiration history.
*   **Important Notes:** Critical considerations regarding [API Pagination](../concepts/api-pagination.md) limits, the significance of [Debit and Credit Effects](../concepts/debit-credit-effect.md) fields, the calculation of net value, and the reconciliation process for [cost basis](../concepts/cost-basis.md) data.

## Related Concepts and Entities

This source document is foundational for understanding:
*   The [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md) itself.
*   The definition and structure of a financial [Transaction](../concepts/transaction.md) within the Tastyworks ecosystem.
*   Mechanisms like [API Pagination](../concepts/api-pagination.md).
*   Various types of [Financial Fees](../concepts/financial-fees.md) encountered in trading.
*   The concept of [Cost Basis](../concepts/cost-basis.md) and its reconciliation.
*   The meaning of [Debit and Credit Effects](../concepts/debit-credit-effect.md) in transaction reporting.

---
**Origin:** The content of this source note is derived directly from the raw payload file `transactions.md`.