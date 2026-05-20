---
tags: ["api", "security", "authentication"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# API Authentication

API authentication refers to the process of verifying the identity of a client making requests to an API. This ensures that only authorized users or applications can access protected resources.

For the [[Market Data API (Tastyworks)|Tastyworks Market Data API]], authentication requires a valid session token.

## Tastyworks Market Data API Authentication
*   **Method:** Session token.
*   **Mechanism:** The session token must be passed via the `Authorization` header in each API request.

## Related
*   [[Market Data API (Tastyworks)]]
*   [[REST API]]
*   [[Tastyworks]]