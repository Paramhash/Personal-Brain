---
tags: ["trading", "api", "orders", "query"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Search Orders

The "Search Orders" functionality allows users to retrieve a paginated list of trading orders based on various filtering parameters. This is typically implemented via a GET request to an API endpoint.

## API Endpoint
`GET /orders` (implied from context, though not explicitly stated with full path, only "Search Orders" heading)

## Query Parameters

*   **`start-date`** (Date): Date to begin searching orders (e.g., `2023-01-01`).
*   **`end-date`** (Date): Date to stop searching orders (e.g., `2023-01-10`).
*   **`underlying-symbol`** (String): Filters orders by the underlying asset's symbol (e.g., `AAPL`).
*   **`status`** (Array[String]): Filters orders by their [[../concepts/order-status.md|status]] (e.g., `status[]=Live&status[]=Filled`).
*   **`futures-symbol`** (String): Filters futures and future option orders by their outright contract symbol (e.g., `ESM3`).
*   **`underlying-instrument-type`** (String): Filters orders by the underlying instrument type.
    *   Values: `Cryptocurrency`, `Equity`, `Future` (Note: "Future" includes both futures and future options; "Equity" includes both equities and equity options).
*   **`sort`** (String): The chronological order that results are returned (ascending or descending).
    *   Default: `Desc` (Descending)
    *   Values: `Asc`, `Desc`
*   **`start-at`** (DateTime): Date and time to start searching orders (e.g., `2023-01-01T00:00:00`).
*   **`end-at`** (DateTime): Date and time to stop searching orders (e.g., `2023-01-05T01:00:00`).
*   **`per-page`** (Integer): Number of paginated results to return at a time.
    *   Default: `10`
*   **`page-offset`** (Integer): Page number to fetch.
    *   Default: `0`

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/live-orders.md|Live Orders]]
*   [[../concepts/order-status.md|Order Status]]