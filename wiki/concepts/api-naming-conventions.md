---
tags: ["api", "best-practices", "naming-conventions"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# API Naming Conventions

API naming conventions refer to the standardized rules and patterns used for naming elements within an API, such as endpoints, parameters, and data fields. Consistent naming improves readability, predictability, and ease of use for developers.

The [[Market Data API (Tastyworks)|Tastyworks Market Data API]] has specific naming conventions that are important to note, particularly regarding field names and query parameters.

## Field Naming (camelCase)
*   Unlike many other [[Tastyworks]] API responses that use `kebab-case` (e.g., `net-liquidating-value`), the [[Market Data API (Tastyworks)|Market Data API]] returns fields in `camelCase` (e.g., `netLiquidatingValue`).
*   This difference is attributed to the Market Data service being a Java-based service with different serialization conventions.

## Query Parameter Naming (Singular Hyphenated)
*   Query parameters for [[Market Data Instrument Types|instrument types]] must use **singular hyphenated** form (e.g., `equity-option`, not `equity-options`). This is a common source of errors if not followed.

## Related
*   [[Market Data API (Tastyworks)]]
*   [[Tastyworks]]
*   [[Market Data Instrument Types]]