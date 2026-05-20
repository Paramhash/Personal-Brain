---
tags: ["oauth2", "security", "token"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# OAuth2 Access Token

An OAuth2 access token is a credential that represents the authorization granted by a user to a client application. It is a temporary key that the client application uses to access protected resources on a resource server on behalf of the user.

## Characteristics

*   **Short-lived**: Access tokens are designed to expire after a relatively short period (e.g., 15 minutes, as with tastytrade's API). This limits the window of opportunity for an attacker if the token is compromised.
*   **Scoped**: Each access token is typically associated with specific [[../concepts/oauth2-scopes.md|scopes]], defining the exact permissions the client application has (e.g., `read` access to an account, `trade` execution). An attacker with a compromised token can only access the resources authorized by that token's scope.
*   **Bearer Token**: Access tokens are commonly "bearer" tokens, meaning whoever possesses the token can use it. They are typically sent in the `Authorization` header of HTTP requests (e.g., `Authorization: Bearer <access_token>`).
*   **Revocable**: Users or the service provider can revoke access tokens, immediately invalidating them and cutting off the client application's access.

## Security Implications

The short lifespan and scoped nature of access tokens significantly enhance security compared to long-lived, unscoped session tokens. If a 15-minute, read-only access token is compromised, an attacker has a very small window to cause damage and can only view data, not modify it. In contrast, a 24-hour session token with full access could allow an attacker an entire day to potentially control an account.

## Generation and Usage

Access tokens are typically obtained after a user authorizes an application, either directly via a [[../concepts/oauth2-refresh-token.md|refresh token]] or through an [[../concepts/oauth2-authorization-code-grant.md|authorization code grant]] flow. Once obtained, they must be included in the `Authorization` header of every API request to the resource server.

When an access token expires, the client application receives an HTTP 401 (Unauthorized) response. It must then use a refresh token (if available) to obtain a new access token.

For details on how tastytrade uses access tokens, refer to [[../research/tastytrade-api-oauth2-integration.md|Tastytrade API OAuth2 Integration]].
See also: [[../concepts/oauth2.md|OAuth2]].

---