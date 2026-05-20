---
tags: ["oauth2", "permissions", "security", "api"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# OAuth2 Scopes

In [[../concepts/oauth2.md|OAuth2]], "scopes" define the specific permissions or access levels that a client application is requesting from a user's account on a service provider. They are a critical security mechanism that ensures applications only gain access to the data and functionality they truly need.

When a user authorizes an application, they are presented with the list of scopes the application is requesting. The user then explicitly grants or denies these permissions.

## Importance of Scopes

*   **Principle of Least Privilege**: Scopes enforce the principle of least privilege, meaning an application should only have the minimum necessary access to perform its function.
*   **User Control**: Users have clear visibility into what an application intends to do with their data, empowering them to make informed decisions about granting access.
*   **Security**: By limiting an application's access, scopes reduce the potential damage if an [[../concepts/oauth2-access-token.md|access token]] is compromised. An attacker can only access the resources defined by the token's granted scopes.

## tastytrade API Scopes

The tastytrade API defines specific scopes that can be requested for an OAuth2 application:

*   `read`: Grants read-only access to account data. This is a sensitive scope and may require [[../concepts/two-factor-authentication.md|Two-Factor Authentication]] for authorization.
*   `trade`: Grants permission to execute trades and potentially other write operations. This is a highly sensitive scope and requires [[../concepts/two-factor-authentication.md|Two-Factor Authentication]] for authorization.
*   `openid`: Used for OpenID Connect, an identity layer on top of OAuth2, to verify the identity of the end-user and obtain basic profile information.

When creating an OAuth2 application with tastytrade, you must specify the scopes your application requires. These scopes will then be presented to the user during the authorization process.

For more details on creating an OAuth2 application and requesting scopes with tastytrade, see [[../research/tastytrade-api-oauth2-integration.md|Tastytrade API OAuth2 Integration]].

---