---
tags: ["oauth2", "authorization", "grant-type"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# OAuth2 Authorization Code Grant Flow

The Authorization Code Grant flow is one of the most common and secure [[../concepts/oauth2.md|OAuth2]] grant types, particularly suitable for confidential clients (applications that can securely store a [[../concepts/oauth2-client-credentials.md|client secret]]) like web servers. It is the flow used by [[../entities/tastytrade.md|tastytrade]] for its "Trusted Partner" OAuth applications.

## Flow Overview

This flow involves several redirects and exchanges to ensure that the client application never directly handles the user's credentials and that the [[../concepts/oauth2-access-token.md|access token]] is not exposed in the user's browser history.

1.  **User Initiates Authorization**: The user clicks a link or button in the client application to authorize it.
2.  **Redirect to Authorization Endpoint**: The client application redirects the user's browser to the authorization server's (e.g., tastytrade's) authorization endpoint. This request includes the `client_id`, `redirect_uri`, `response_type` (set to `code`), and optionally `scope` and `state`.
    *   *tastytrade Authorization Endpoint:* `https://my.tastytrade.com/auth.html`
3.  **User Authentication & Consent**: The user logs in to the authorization server (if not already logged in) and is prompted to grant or deny the client application's requested [[../concepts/oauth2-scopes.md|scopes]]. If sensitive scopes are requested, [[../concepts/two-factor-authentication.md|Two-Factor Authentication]] may be required.
4.  **Redirect with Authorization Code**: If the user grants access, the authorization server redirects the user's browser back to the `redirect_uri` provided by the client application. This redirect includes a short-lived `code` (the authorization code) and the `state` parameter (if provided).
5.  **Client Requests Access Token**: The client application, on its backend server, makes a direct (server-to-server) POST request to the authorization server's token endpoint. This request includes the `grant_type` (set to `authorization_code`), the `code` received in the previous step, its `client_id`, `client_secret`, and the `redirect_uri`.
    *   *tastytrade Token Endpoint:* `POST https://api.tastyworks.com/oauth/token`
6.  **Authorization Server Issues Tokens**: The authorization server validates the request. If valid, it responds with an [[../concepts/oauth2-access-token.md|access token]], a [[../concepts/oauth2-refresh-token.md|refresh token]], `token_type` (Bearer), and `expires_in` (access token validity duration).
7.  **Client Accesses Resources**: The client application uses the access token to make authenticated requests to the resource server on behalf of the user.

## Security Advantages

*   **Authorization Code is not an Access Token**: The authorization code itself is useless to an attacker without the `client_secret`.
*   **Direct Token Exchange**: The access token is exchanged directly between the client's backend server and the authorization server, bypassing the user's browser and preventing its exposure in browser history or logs.
*   **`state` Parameter**: Used to prevent Cross-Site Request Forgery (CSRF) attacks by maintaining state between the authorization request and the callback.

For a detailed implementation guide for tastytrade's Authorization Code Grant flow, see [[../research/tastytrade-api-oauth2-integration.md|Tastytrade API OAuth2 Integration]].
For the official specification, refer to [[../sources/rfc6749-oauth2-framework.md|RFC 6749: The OAuth 2.0 Authorization Framework]].

---