---
tags: ["authentication", "security", "api", "oauth2", "bearer-token"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# OAuth2 Authentication for tastytrade API

The [[../entities/tastytrade-open-api.md|tastytrade Open API]] utilizes OAuth2 for all API request authentication. This standard protocol ensures secure access to user accounts and functionalities.

## Key Aspects
*   **Bearer Tokens**: All API requests require an OAuth2 bearer token in the `Authorization` header.
*   **Token Generation**: Access tokens (typically 15-minute expiry) are generated via a `POST /oauth/token` endpoint.
*   **Application Creation**: Developers must create an OAuth application at `my.tastytrade.com` to obtain necessary credentials.
*   **Personal Grant & Refresh Tokens**: For single-user applications, personal grant and refresh tokens can be generated. Refresh tokens are used to obtain new access tokens without re-authentication.
*   **Authorization Code Grant Flow**: For third-party applications requiring multi-user access, the authorization code grant flow is used, often requiring trusted partner status.
*   **Two-Factor Authentication (2FA)**: Required for `read` and `trade` scopes to enhance security.

## Workflow
1.  Create an OAuth application on the tastytrade platform.
2.  Generate a personal grant and refresh token (for personal use) or implement the authorization code grant flow (for multi-user apps).
3.  Use the refresh token to obtain a short-lived access token.
4.  Include the access token as a `Bearer` token in the `Authorization` header for all subsequent API requests.
5.  Refresh the access token before it expires using the refresh token.

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]