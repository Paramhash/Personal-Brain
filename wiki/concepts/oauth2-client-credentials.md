---
tags: ["oauth2", "security", "api"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# OAuth2 Client Credentials (Client ID & Client Secret)

In the context of [[../concepts/oauth2.md|OAuth2]], client credentials are used to identify and authenticate a client application with the authorization server. The two primary components are the Client ID and the Client Secret.

## Client ID

The Client ID is a publicly exposed identifier for a client application. It is used by the authorization server to identify which application is requesting authorization or tokens.

*   **Visibility**: It is not considered sensitive and can be embedded in client-side code or publicly accessible parts of an application.
*   **Purpose**: To identify the application to the user during the authorization process and to the authorization server when requesting tokens.

## Client Secret

The Client Secret is a confidential credential used by the client application to authenticate itself to the authorization server. It functions much like a password for the application itself.

*   **Confidentiality**: The client secret **must be kept confidential** and stored securely. It should never be exposed in client-side code, public repositories, or transmitted insecurely.
*   **Purpose**: To prove the identity of the client application when exchanging an authorization grant for an [[../concepts/oauth2-access-token.md|access token]] or when refreshing an access token using a [[../concepts/oauth2-refresh-token.md|refresh token]].
*   **One-time Display**: Many services, including tastytrade, will only display the client secret once upon creation. If lost, it typically needs to be regenerated, which may invalidate existing grants.

## Management in tastytrade

For tastytrade API users, client credentials are created when you register an OAuth2 application on my.tastytrade.com.

*   **Creation**: You define a client name, redirect URIs, and requested [[../concepts/oauth2-scopes.md|scopes]]. Upon creation, the Client ID and Client Secret are displayed.
*   **Secure Storage**: It is crucial to store the Client Secret securely immediately upon receipt, as tastytrade will not display it again.
*   **Regeneration**: If a Client Secret is lost or compromised, it can be regenerated through the tastytrade portal. This action will invalidate any active grants associated with the old secret.

For detailed instructions on managing client credentials with tastytrade, refer to [[../research/tastytrade-api-oauth2-integration.md|Tastytrade API OAuth2 Integration]].

---