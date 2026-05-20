---
tags: ["source", "oauth2", "standard", "ietf"]
created: 2023-10-27
reviewed: false
source_origin: "api-guides.md"
---
# RFC 6749: The OAuth 2.0 Authorization Framework

**Title:** The OAuth 2.0 Authorization Framework
**Author(s):** D. Hardt
**Published:** October 2012
**URL:** [https://datatracker.ietf.org/doc/html/rfc6749](https://datatracker.ietf.org/doc/html/rfc6749)

## Description

RFC 6749 defines the OAuth 2.0 Authorization Framework, an industry-standard protocol for authorization. It describes how a user can grant a third-party application limited access to their resources on another service without sharing their credentials.

This document outlines the various roles, abstract protocol flows, and specific grant types (such as the [[../concepts/oauth2-authorization-code-grant.md|Authorization Code Grant]]) that form the foundation of OAuth 2.0. It details the use of [[../concepts/oauth2-access-token.md|access tokens]] and [[../concepts/oauth2-refresh-token.md|refresh tokens]], as well as the roles of the client, resource owner, authorization server, and resource server.

## Key Sections Referenced

*   **Section 4.1.1 (Authorization Request)**: Details the parameters for initiating an authorization request in the authorization code grant flow.
*   **Section 4.1.2 (Authorization Response)**: Describes the parameters returned to the client's redirect URI after user authorization.
*   **Section 4.1.3 (Access Token Request)**: Specifies the parameters for exchanging an authorization code for an access token.
*   **Section 5.1 (Access Token Response)**: Outlines the expected response when an access token is successfully issued.
*   **Section 6 (Refreshing an Access Token)**: Describes the process and parameters for using a refresh token to obtain a new access token.

## Relevance

RFC 6749 serves as the foundational specification for all implementations of [[../concepts/oauth2.md|OAuth2]], including its use in the [[../entities/tastytrade.md|tastytrade]] API. Understanding this RFC is crucial for anyone developing or integrating with OAuth2-based systems to ensure compliance and security.

---