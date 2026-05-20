---
tags: ["security", "authentication", "authorization", "oauth2", "api"]
created: 2023-10-27
reviewed: false
source_origin: "oauth2.md"
---
# Access Token

An access token is a credential that grants an application temporary, scoped access to a user's resources on a server, without requiring the application to handle the user's password. It is a core component of the [[../entities/oauth2.md|OAuth2]] authorization framework.

## Characteristics

*   **Short-lived**: Access tokens typically have a limited lifespan (e.g., 15 minutes in the tastytrade API context). This minimizes the risk if a token is compromised, as an attacker has a small window to cause damage.
*   **Scoped**: An access token is usually associated with specific permissions or "scopes" (e.g., `read` access, `trade` access). This means the application can only perform actions explicitly granted by the user.
*   **Bearer Token**: Access tokens are often "bearer" tokens, meaning whoever possesses the token can use it. They are typically sent in the `Authorization` header of HTTP requests (e.g., `Authorization: Bearer <access_token>`).
*   **Revocable**: Users or the authorization server can revoke an access token, immediately invalidating it.

## Usage

When an application needs to access a user's protected resources (e.g., account information, trading capabilities), it includes the access token in its API requests. If the token is valid and has the necessary scopes, the server grants access.

Once an access token expires, a new one must be obtained. This is typically done using a [[../concepts/refresh-token.md|refresh token]] or by initiating a new authorization flow.

---