---
tags: ["security", "authentication", "authorization", "api"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# OAuth2

OAuth2 (Open Authorization 2.0) is a widely trusted industry-standard protocol for authorization. It allows a user to grant a third-party application limited access to their resources on another service (like tastytrade) without sharing their credentials (username and password).

Instead of an application directly asking for a user's password, OAuth2 facilitates a secure delegation of access. The user authenticates with the service provider (e.g., tastytrade), and the service provider then issues a temporary, limited-permission token to the third-party application. This ensures the user's password remains with the trusted service and is never exposed to the third-party application.

## Key Components of OAuth2

*   **[[../concepts/oauth2-access-token.md|Access Token]]**: A short-lived credential that grants specific permissions to an application.
*   **[[../concepts/oauth2-refresh-token.md|Refresh Token]]**: A long-lived credential used to obtain new access tokens without re-authenticating the user.
*   **[[../concepts/oauth2-client-credentials.md|Client ID and Client Secret]]**: Credentials that identify the third-party application to the authorization server.
*   **[[../concepts/oauth2-scopes.md|Scopes]]**: Define the specific permissions or access levels an application is requesting (e.g., read-only access, trading capabilities).
*   **Authorization Server**: The server that handles user authentication and issues tokens.
*   **Resource Server**: The server that hosts the protected user resources and accepts access tokens.

## How it Works (General Flow)

1.  **Authorization Request**: The client application requests authorization from the user to access their resources on the service provider.
2.  **User Authorization**: The user is redirected to the service provider's login page, where they authenticate and grant (or deny) the application's requested permissions.
3.  **Authorization Grant**: If approved, the service provider issues an authorization grant (e.g., an authorization code) back to the client application.
4.  **Access Token Request**: The client application exchanges the authorization grant (along with its client credentials) for an access token from the authorization server.
5.  **Access Token Granted**: The authorization server validates the request and issues an access token (and often a refresh token).
6.  **Resource Access**: The client application uses the access token to make requests to the resource server on behalf of the user.

## Security Benefits

*   **Password Protection**: User passwords are never shared with third-party applications.
*   **Limited Access**: Access tokens are scoped to specific permissions, preventing applications from accessing more data than necessary.
*   **Revocability**: Users can revoke an application's access at any time without changing their password.
*   **Temporary Access**: Access tokens are typically short-lived, reducing the window of opportunity for attackers if a token is compromised.

For a practical application of OAuth2, see [[../research/tastytrade-api-oauth2-integration.md|Tastytrade API OAuth2 Integration]].
For the official specification, refer to [[../sources/rfc6749-oauth2-framework.md|RFC 6749: The OAuth 2.0 Authorization Framework]].

---