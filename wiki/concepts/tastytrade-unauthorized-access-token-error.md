---
tags: ["tastytrade", "api", "errors", "authentication", "access-token"]
created: 2023-10-27
reviewed: false
source_origin: "faq.md"
---
# Unauthorized Error (Missing/Invalid Access Token) (tastytrade API)

An `unauthorized` error typically indicates that a request was made without a valid access token, or with an expired or malformed one.

## Access Token Requirements

*   **Duration:** Access tokens are short-lived, lasting only **15 minutes**.
*   **Inclusion:** A valid access token **must** be sent with every API request in the `Authorization` header.

## Resolution

1.  **Generate a new access token:** Follow the procedures outlined in the [[./tastytrade-auth-patterns.md|tastytrade Auth Patterns]] documentation to obtain a fresh access token.
2.  **Include in Header:** Ensure the newly generated access token is included as the value of the `Authorization` header in all subsequent requests. The format is typically `Authorization: Bearer <your_access_token>`.

## Related Concepts

*   [[../entities/tastytrade.md|tastytrade]]
*   [[./tastytrade-auth-patterns.md|tastytrade Auth Patterns]]
*   [[./tastytrade-api-conventions.md|tastytrade API Conventions]]

---
*This information is derived from the tastytrade API FAQ.*