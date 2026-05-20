---
tags: ["tastytrade", "API", "authorization", "authentication", "oauth2", "access-token"]
created: 2023-10-27
reviewed: false
source_origin: "getting-started.md"
---
# tastytrade API: Authorization & Authentication

To interact with the [tastytrade API](../entities/tastytrade.md), every request you make must include an `Authorization` header containing a valid access token. This token is crucial for authenticating your identity and authorizing your access to specific API resources.

## OAuth2 Access Token

The tastytrade API utilizes OAuth2 for authorization. This means you will need to:

1.  **Obtain an OAuth2 access token**: This token is generated after successfully authenticating your credentials (e.g., username and password) with the tastytrade authentication service.
2.  **Include the token in the `Authorization` header**: For every subsequent API request, this token must be passed in the `Authorization` header, typically in the format `Bearer <your_access_token>`.

For more detailed information on session management and the structure of the `Authorization` header, consult the Auth Patterns Overview documentation provided by tastytrade.

This is a critical step in the [tastytrade API: Getting Started Guide](./tastytrade-api-getting-started.md).