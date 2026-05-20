---
tags: ["api-documentation", "tastyworks", "market-data", "reference"]
created: 2023-10-27
reviewed: false
source_origin: "market-sessions.md"
---
# Tastyworks Market Sessions API Documentation

This document summarizes the official API documentation for the Tastyworks Market Sessions API. It provides endpoints for retrieving market open/close times, current market state, and trading holidays across various exchanges for equities and futures.

**Key Features:**
*   Determine market open/close times for specific dates or ranges.
*   Check the current market state (e.g., `Open`, `Closed`, `Pre-Market`, `After-Hours`).
*   Identify trading holidays and half-days.
*   Support for multiple [[../concepts/instrument-collections.md|instrument collections]] including US Equities, CME, CFE, and Zero Hash CLOB.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token in the `Authorization` header.

For detailed usage and endpoint specifics, refer to the related [[../concepts/market-sessions.md|Market Sessions]] concept note.

---
## Related Notes
*   [[../concepts/market-sessions.md|Market Sessions]]
*   [[../entities/tastyworks.md|Tastyworks]]
*   [[../concepts/api-endpoints.md|API Endpoints]]
*   [[../concepts/data-models.md|Data Models]]