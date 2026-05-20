---
tags: []
created: 2023-10-27
reviewed: false
source_origin: "transactions.md"
---
# API Pagination

**API Pagination** is a common technique used in Application Programming Interfaces (APIs) to manage and retrieve large datasets efficiently. Instead of returning all results in a single, potentially massive response, pagination divides the data into smaller, more manageable chunks called "pages." This approach improves performance, reduces network load, and makes it easier for client applications to process data incrementally.

## Tastyworks Transactions API Implementation

The [Tastyworks Transactions API](../entities/tastyworks-transactions-api.md) utilizes pagination for its `Search Transactions` endpoint (`GET /accounts/{account_number}/transactions`). This allows users to retrieve transaction history in segments, especially for accounts with extensive activity.

Key query parameters for pagination include:

*   `page-offset` (integer): Specifies the starting point for the results. A `page-offset` of `0` typically refers to the first page.
*   `per-page` (integer): Defines the maximum number of results to return in a single page.
    *   **Default:** `250`
    *   **Minimum:** `1`
    *   **Maximum:** `2000`

### Important Considerations

*   **Limits:** The maximum number of results per page is 2,000. For accounts with heavy trading activity, it is essential to combine date range filtering with pagination to ensure all historical data is retrieved.
*   **Retrieval Strategy:** To fetch a complete history, clients should typically make successive requests, incrementing the `page-offset` until no more results are returned.

---
**Source:** [Tastyworks Transactions API Documentation](../sources/tastyworks-transactions-api-docs.md)