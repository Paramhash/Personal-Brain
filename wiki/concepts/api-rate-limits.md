---
tags: ["api", "rate-limiting", "performance"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# API Rate Limits

API rate limits are restrictions on the number of requests a client can make to an API within a given timeframe. These limits are implemented to prevent abuse, ensure fair usage, and maintain the stability and performance of the API service.

For the [[Market Data API (Tastyworks)|Tastyworks Market Data API]], a specific limit applies to the number of symbols that can be requested in a single call.

## Tastyworks Market Data API Specific Limit
*   **Symbol Limit:** The combined total of symbols across all [[Market Data Instrument Types|instrument type]] parameters cannot exceed **100 symbols per request**.

## Implications
*   Clients must design their applications to respect this limit, potentially batching requests or making multiple calls if more than 100 symbols are needed.
*   Exceeding this limit will likely result in an error response from the API.

## Related
*   [[Market Data API (Tastyworks)]]
*   [[Market Data Instrument Types]]