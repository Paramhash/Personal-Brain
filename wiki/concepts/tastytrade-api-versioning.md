---
tags: ["tastytrade", "API", "versioning", "deprecation", "headers"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Versioning

The tastytrade API employs a versioning strategy to manage breaking changes without disrupting existing client integrations.

## Versioning Strategy

*   **Date-Based Versions**: API versions are identified by the date they were introduced, in `YYYYMMDD` format (e.g., `20250904`).
*   **Breaking Changes**: When breaking changes are introduced, tastytrade deprecates the existing version and implements the changes in a new API version.
*   **Targeting a Version**: To specify an API version for your request, include the `Accept-Version` header (e.g., `Accept-Version: 20250904`). This header is part of the [[../concepts/tastytrade-api-conventions.md|tastytrade API Conventions]].

## Deprecation Policy

*   **Lifespan**: Deprecated API versions typically have a 9-month lifespan. Developers are advised to monitor the API Docs and Release Notes for updates and migrate to the latest versions.
*   **Unsupported Version Error**: If a request targets a version that no longer exists, the API will return an HTTP `406 Not Acceptable` error:
    ```json
    {
      "error": {
        "code": 406,
        "message": "The requested version is not supported."
      }
    }
    ```

## Targeting the Latest Version

To always target the latest available API version, you can send today's date in the `Accept-Version` header (e.g., `Accept-Version: 20250101` if today is January 1st, 2025).

*   **Routing Logic**: tastytrade will route your request to the nearest API version at or before your target date. For example, if versions `20250101` and `20250201` exist, a request with `Accept-Version: 20250102` will be routed to `20250101`. Requests are never routed to a version greater than the one specified.

For a comprehensive understanding of the API's structure, refer to the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].