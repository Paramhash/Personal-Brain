---
tags: ["security", "authentication", "authorization", "api", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "oauth2.md"
---
# OAuth2 (tastytrade Implementation)

OAuth2 is a widely trusted security standard that [[../entities/tastytrade.md|tastytrade]] utilizes to ensure the safety and security of user accounts when interacting with its API and third-party applications. Instead of sharing sensitive credentials like passwords directly with every application, OAuth2 enables users to grant limited, temporary access through a trusted service like tastytrade.

## Core Principles

The fundamental idea behind OAuth2 is to delegate authorization. This means your password remains securely with tastytrade, and external applications receive only temporary, scoped credentials known as [[../concepts/access-token.md|access tokens]].

### Key Components

*   **[[../concepts/access-token.md|Access Token]]**: A short-lived credential that grants an application specific permissions to a user's resources. tastytrade access tokens are valid for 15 minutes.
*   **[[../concepts/refresh-token.md|Refresh Token]]**: A long-lived credential used to obtain new access tokens without requiring the user to re-authenticate.
*   **Client ID**: A public identifier for your OAuth2 application.
*   **Client Secret**: A confidential key used to authenticate your application with tastytrade's OAuth2 server. This must be stored securely and is shown only once upon creation.
*   **Redirect URI**: The URI where tastytrade will redirect the user's browser after they authorize your application, often including an authorization code.
*   **Scopes**: Define the specific permissions an application is requesting (e.g., `read`, `trade`, `openid`).

## Security Benefits

*   **No Password Sharing**: User passwords are never shared with third-party applications.
*   **Scoped Access**: Applications only receive permissions for specific actions (e.g., read-only access), minimizing potential damage from compromise.
*   **Temporary Credentials**: [[../concepts/access-token.md|Access tokens]] are short-lived (15 minutes), significantly reducing the window for an attacker to exploit a compromised token compared to long-lived session tokens.
*   **Revocable Access**: Users can revoke an application's access at any time.

## tastytrade API Integration

tastytrade supports two primary OAuth2 flows for API users:

1.  **Personal OAuth Applications**: For individual developers to access their own tastytrade account.
2.  **Trusted Partner Applications**: For applications that need to be authorized by other tastytrade users.

### 1. Personal OAuth Applications

This flow is designed for developers to integrate with their own tastytrade account without going through the full user authorization process.

#### 1.1. Create an OAuth Application

1.  Navigate to `my.tastytrade.com` > `Manage` tab > `My Profile` > `API` > `OAuth Applications`.
2.  Click `+ New OAuth client`.
3.  Provide a `Client Name` (pre-populated with your username).
4.  Specify `Redirect URI`s (full URIs, e.g., `https://www.my-redirect-uri.com`). Multiple URIs can be added.
5.  Select `Scopes` (e.g., `read`, `trade`, `openid`).
6.  Click `Create`.
7.  **Securely store the displayed `Client ID` and `Client Secret`**. The client secret is shown only once. If lost, it must be regenerated, which invalidates existing grants.

#### 1.2. Generate a Personal Grant

This step provides a [[../concepts/refresh-token.md|refresh token]] directly for your personal application.

1.  Navigate to `my.tastytrade.com` > `Manage` tab > `My Profile` > `API` > `OAuth Applications`.
2.  Locate your application and click `Manage`.
3.  Click `Create Grant`.
4.  **Securely store the displayed `Refresh Token`**. Refresh tokens are long-lived and do not expire. If compromised, delete the corresponding grant on the API page.

#### 1.3. Generate an Access Token

Use the `refresh_token` and `client_secret` to obtain a short-lived [[../concepts/access-token.md|access token]].

*   **Endpoint**: `POST https://api.tastyworks.com/oauth/token` (Sandbox: `https://api.cert.tastyworks.com/oauth/token`)
*   **Required Parameters (Form-encoded)**:
    *   `grant_type`: `refresh_token`
    *   `refresh_token`: Your personal grant's refresh token.
    *   `client_secret`: Your application's client secret.
*   **Response**: Includes `access_token` (valid for 15 minutes), `token_type` (`Bearer`), and `expires_in`.
*   **Usage**: The `access_token` must be sent as a Bearer token in the `Authorization` header of each API request (e.g., `Authorization: "Bearer <access token>"`).

### 2. Trusted Partner Applications (Authorization Code Grant Flow)

To allow other tastytrade users to connect to your application, you must complete tastytrade's trusted partner verification process. Contact `api.support@tastytrade.com` for details.

#### 2.1. User Authorization

After approval, direct users to authorize your application.

*   **Authorization Endpoint**: `https://my.tastytrade.com/auth.html` (Sandbox: `https://cert-my.staging-tasty.works/auth.html`)
*   **Required Query Parameters**:
    *   `client_id`: Your application's client ID.
    *   `redirect_uri`: The URI where the user will be redirected after authorization.
    *   `response_type`: `code`
*   **Optional Query Parameters**:
    *   `scope`: Requested permissions (e.g., `read`, `trade`, `openid`).
    *   `state`: An opaque value used to maintain state between the request and callback.
*   **User Experience**: Users will be prompted to log in to tastytrade and grant your application the requested permissions.
*   **Redirect**: Upon successful authorization, the user is redirected to your `redirect_uri` with `code` (authorization code) and `state` query parameters.

#### 2.2. Request an Access Token

Exchange the authorization `code` for an [[../concepts/access-token.md|access token]] and [[../concepts/refresh-token.md|refresh token]].

*   **Endpoint**: `POST https://api.tastyworks.com/oauth/token` (Sandbox: `https://api.cert.tastyworks.com/oauth/token`)
*   **Required Parameters (Form-encoded)**:
    *   `grant_type`: `authorization_code`
    *   `code`: The authorization code received from the redirect.
    *   `client_id`: Your application's client ID.
    *   `client_secret`: Your application's client secret.
    *   `redirect_uri`: The same redirect URI used in the authorization step.
*   **Response**: Includes `access_token`, `refresh_token` (never expires), `token_type` (`Bearer`), `expires_in`, and `id_token` (if `openid` scope was used).

#### 2.3. Refresh an Access Token

Use the `refresh_token` to obtain a new [[../concepts/access-token.md|access token]] when the current one expires.

*   **Endpoint**: `POST https://api.tastyworks.com/oauth/token` (Sandbox: `https://api.cert.tastyworks.com/oauth/token`)
*   **Required Parameters (Form-encoded)**:
    *   `grant_type`: `refresh_token`
    *   `refresh_token`: The refresh token obtained during the initial access token request.
    *   `client_secret`: Your application's client secret.
*   **Response**: Includes a new `access_token`.

## Two-Factor Authentication (2FA)

For sensitive scopes like `read` and `trade`, tastytrade requires users to have [[../concepts/two-factor-authentication.md|Two-Factor Authentication (2FA)]] enabled on their account. If 2FA is enabled (via Authenticator App or SMS), users will be prompted for a 2FA code during the authorization step.

## References

*   OAuth 2.0 Authorization Framework: [https://datatracker.ietf.org/doc/html/rfc6749](https://datatracker.ietf.org/doc/html/rfc6749)

---