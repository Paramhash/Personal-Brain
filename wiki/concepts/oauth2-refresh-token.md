---
tags: ["oauth2", "security", "token"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# OAuth2 Refresh Token

An OAuth2 refresh token is a credential used by a client application to obtain new [[../concepts/oauth2-access-token.md|access tokens]] after the current one has expired, without requiring the user to re-authenticate.

## Characteristics

*   **Long-lived**: Unlike access tokens, refresh tokens are designed to be long-lived and often do not expire (or have a very long expiration period). This allows applications to maintain continuous access to resources without frequent user interaction.
*   **Secure Storage**: Due to their long lifespan and ability to grant new access tokens, refresh tokens are highly sensitive and must be stored securely by the client application.
*   **Revocable**: Refresh tokens can be revoked by the user or the service provider. If a refresh token is compromised, it should be immediately deleted or revoked to prevent unauthorized access.
*   **Used for Token Refresh**: The primary purpose of a refresh token is to be exchanged with the authorization server for a new access token. This process typically also involves the client's [[../concepts/oauth2-client-credentials.md|client secret]].

## Security Considerations

While refresh tokens are long-lived, they are typically exchanged directly with the authorization server and are not sent with every API request to the resource server. This reduces their exposure compared to access tokens. However, their long lifespan makes their compromise a significant security risk, as an attacker could continuously generate new access tokens.

If a refresh token is lost or compromised, it is crucial to delete the corresponding grant or contact API support to have it revoked. Generating a new grant will issue a new refresh token, invalidating the old one.

## Generation and Usage

Refresh tokens are typically issued alongside the initial access token during the authorization process (e.g., after a user grants permission to an application).

To generate a new access token using a refresh token, the client application sends a request to the token endpoint of the authorization server, including the `grant_type` (set to `refresh_token`), the `refresh_token` itself, and the `client_secret`.

For details on how tastytrade uses refresh tokens, refer to [[../research/tastytrade-api-oauth2-integration.md|Tastytrade API OAuth2 Integration]].
See also: [[../concepts/oauth2.md|OAuth2]].

---