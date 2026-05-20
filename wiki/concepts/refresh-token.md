---
tags: ["security", "authentication", "authorization", "oauth2", "api"]
created: 2023-10-27
reviewed: false
source_origin: "oauth2.md"
---
# Refresh Token

A refresh token is a long-lived credential used in the [[../entities/oauth2.md|OAuth2]] framework to obtain new, short-lived [[../concepts/access-token.md|access tokens]] without requiring the user to re-authenticate.

## Characteristics

*   **Long-lived**: Unlike access tokens, refresh tokens typically have a much longer lifespan, often not expiring until explicitly revoked.
*   **Confidential**: Refresh tokens are highly sensitive and must be stored securely by the client application, as their compromise could allow an attacker to continuously generate new access tokens.
*   **Used for Token Renewal**: When an [[../concepts/access-token.md|access token]] expires, the client application can use the refresh token (along with its `client_secret`) to request a new access token from the authorization server. This process is transparent to the user, improving user experience by avoiding frequent re-logins.
*   **Revocable**: Refresh tokens can be revoked by the user or the authorization server, immediately preventing the generation of new access tokens.

## Usage

After a user grants authorization, the application typically receives both an [[../concepts/access-token.md|access token]] and a refresh token. The access token is used for immediate API calls. When the access token expires, the application uses the refresh token to request a new one from the `/oauth/token` endpoint.

In the tastytrade API context, refresh tokens for personal grants do not expire, but they should be deleted if lost or compromised. For trusted partner applications, if a refresh token is lost or compromised, tastytrade API support should be contacted immediately.

---