---
tags: ["api-integration", "oauth2", "tastytrade", "how-to", "security"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# Tastytrade API OAuth2 Integration Guide

This guide details the process of integrating with the [[../entities/tastytrade.md|tastytrade]] API using [[../concepts/oauth2.md|OAuth2]], covering both personal application setup and the "Trusted Partner" flow for third-party applications. tastytrade mandates OAuth2 for all API interactions to ensure account security.

## Core Security Principles

*   **No Password Sharing**: Your tastytrade password remains with tastytrade and is never shared with third-party applications.
*   **Short-lived, Scoped [[../concepts/oauth2-access-token.md|Access Tokens]]**: Access tokens are valid for 15 minutes and grant limited, specific permissions (defined by [[../concepts/oauth2-scopes.md|scopes]]).
*   **Long-lived [[../concepts/oauth2-refresh-token.md|Refresh Tokens]]**: Used to obtain new access tokens without re-authentication. Must be stored securely.
*   **[[../concepts/two-factor-authentication.md|Two-Factor Authentication (2FA)]]**: Highly recommended and required for sensitive scopes like `read` and `trade`.

## Part 1: Personal OAuth Application Setup

This section covers setting up an OAuth2 application for your own personal use with the tastytrade API.

### 1. Create an OAuth Application

1.  Navigate to `my.tastytrade.com` > `Manage` tab > `My Profile` > `API` > `OAuth Applications`.
2.  Click `+ New OAuth client`.
3.  **Client Name**: Will be pre-populated with your tastytrade username.
4.  **Redirect URI per environment requested**:
    *   Enter full URIs (e.g., `https://www.my-redirect-uri.com`). Multiple URIs can be added.
5.  **Scopes requested**: Select the necessary [[../concepts/oauth2-scopes.md|scopes]]: `read`, `trade`, `openid`.
6.  Click `Create`.
7.  **Securely Store Credentials**: You will be presented with your **[[../concepts/oauth2-client-credentials.md|Client ID]]** and **[[../concepts/oauth2-client-credentials.md|Client Secret]]**.
    *   **IMPORTANT**: Your Client Secret is shown only once. Store it securely immediately. If lost, you must regenerate it, which invalidates existing grants.

### 2. Generate a Personal Grant

For personal applications, tastytrade allows you to directly generate a grant without going through the full authorization flow.

1.  Go to `my.tastytrade.com` > `Manage` tab > `My Profile` > `API` > `OAuth Applications`.
2.  Locate your personal application and click the `Manage` button on the right.
3.  Click `Create Grant`.
4.  **Securely Store Refresh Token**: You will be shown your grant's **[[../concepts/oauth2-refresh-token.md|refresh token]]**.
    *   **IMPORTANT**: Refresh tokens are long-lived. Store it securely. If lost or compromised, delete the corresponding grant on the API page and generate a new one.

### 3. Generate an Access Token (Personal Application)

Use your refresh token to obtain an access token.

*   **Endpoint**: `POST https://api.tastyworks.com/oauth/token` (Sandbox: `https://api.cert.tastyworks.com/oauth/token`)
*   **Required Parameters (Form-encoded or JSON body)**:
    *   `grant_type`: `refresh_token`
    *   `refresh_token`: The refresh token obtained in Step 2.
    *   `client_secret`: The client secret obtained in Step 1.
*   **Response**: Includes a new `access_token` (valid for 15 minutes), `refresh_token` (if it was rotated), `token_type` (Bearer), `expires_in` (seconds until expiration), and `id_token` (if `openid` scope was used).
*   **Usage**: Include the `access_token` as a bearer token in the `Authorization` header of each API request (e.g., `Authorization: "Bearer <access_token>"`).
*   **Expiration**: Access tokens expire after 15 minutes. An HTTP 401 response indicates an expired token; generate a new one using your refresh token.

## Part 2: Becoming a Trusted Partner (for Third-Party Applications)

If you intend for other tastytrade users to connect to your application, you must complete the trusted partner verification process. Contact `api.support@tastytrade.com` for approval. Once approved, your application will use the [[../concepts/oauth2-authorization-code-grant.md|Authorization Code Grant]] flow.

### 1. User Authorization (Trusted Partner Flow)

Direct users to authorize your application.

*   **Authorization Endpoint**: `https://my.tastytrade.com/auth.html` (Sandbox: `https://cert-my.staging-tasty.works/auth.html`)
*   **Required Query Parameters**:
    *   `client_id`: Your application's Client ID.
    *   `redirect_uri`: The URI where the user will be redirected after authorization. Must match a registered URI.
    *   `response_type`: `code`
*   **Optional Query Parameters**:
    *   `scope`: Space-separated list of requested [[../concepts/oauth2-scopes.md|scopes]] (e.g., `read trade openid`).
    *   `state`: An opaque value used to maintain state between the request and callback, preventing CSRF attacks.
*   **User Experience**: Users will log in to tastytrade, potentially complete [[../concepts/two-factor-authentication.md|2FA]] for sensitive scopes, and then grant or deny your application's requested permissions.
*   **Redirect Response**: Upon successful authorization, the user is redirected back to your `redirect_uri` with `code` (the authorization code) and `state` (if provided) as query parameters.

### 2. Request an Access Token (Trusted Partner Flow)

Exchange the authorization code for an access token from your backend server.

*   **Endpoint**: `POST https://api.tastyworks.com/oauth/token` (Sandbox: `https://api.cert.tastyworks.com/oauth/token`)
*   **Required Parameters (Form-encoded or JSON body)**:
    *   `grant_type`: `authorization_code`
    *   `code`: The authorization code received from the redirect.
    *   `client_id`: Your application's Client ID.
    *   `client_secret`: Your application's Client Secret.
    *   `redirect_uri`: The same redirect URI used in the authorization request.
*   **Response**: Includes `access_token`, `refresh_token` (never expires), `token_type` (Bearer), `expires_in` (seconds until access token expires), and `id_token` (if `openid` scope was used).
*   **Usage**: Store the `refresh_token` securely for future use. Use the `access_token` in the `Authorization` header for API requests.

### 3. Refresh an Access Token (Trusted Partner Flow)

Use the refresh token to obtain new access tokens when the current one expires.

*   **Endpoint**: `POST https://api.tastyworks.com/oauth/token` (Sandbox: `https://api.cert.tastyworks.com/oauth/token`)
*   **Required Parameters (Form-encoded or JSON body)**:
    *   `grant_type`: `refresh_token`
    *   `refresh_token`: The refresh token obtained during the initial access token request.
    *   `client_secret`: Your application's Client Secret.
*   **Response**: Includes a new `access_token` (valid for 15 minutes), `refresh_token` (if it was rotated), `token_type` (Bearer), `expires_in` (seconds until expiration), and `id_token` (if `openid` scope was used).
*   **Security Note**: If a refresh token is lost or compromised, contact tastytrade API support immediately.

## Two-Factor Authentication (2FA)

For sensitive scopes (`read`, `trade`), tastytrade requires users to have 2FA enabled on their account. During the authorization step, after entering credentials, users will be prompted for their 2FA code (from an authenticator app or SMS).

Users can enable 2FA via `My Profile | Security` on my.tastytrade.com.

## External References

*   [[../sources/rfc6749-oauth2-framework.md|RFC 6749: The OAuth 2.0 Authorization Framework]]
    *   Section 4.1.1: Authorization Request
    *   Section 4.1.2: Authorization Response
    *   Section 4.1.3: Access Token Request
    *   Section 5.1: Access Token Response
    *   Section 6: Refreshing an Access Token

---