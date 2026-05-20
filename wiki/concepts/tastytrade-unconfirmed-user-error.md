---
tags: ["tastytrade", "api", "errors", "email-confirmation"]
created: 2023-10-27
reviewed: false
source_origin: "faq.md"
---
# Unconfirmed User Error (tastytrade API)

The `unconfirmed_user` error indicates that a user's email address has not been confirmed within 3 days of signing up. This applies to both sandbox and production users.

## Resolution

To resolve this error, the user must request a confirmation email and follow the instructions:

1.  **Request a confirmation email:**
    ```bash
    curl -X POST https://api.cert.tastyworks.com/confirmation -H "Content-Type: application/json" -d '{ "email": "<insert your user email here>" }'
    ```
    (Note: The URL `api.cert.tastyworks.com` is for the sandbox environment. Adjust for production if necessary.)

2.  **Check your inbox:** Look for a confirmation link in the email address provided.

3.  **Click the link:** Once clicked, a success message should appear, confirming the email address.

## Related Concepts

*   [[../entities/tastytrade.md|tastytrade]]
*   [[./tastytrade-sandbox-environment.md|tastytrade Sandbox Environment]]
*   [[./tastytrade-production-environment.md|tastytrade Production Environment]]

---
*This information is derived from the tastytrade API FAQ.*