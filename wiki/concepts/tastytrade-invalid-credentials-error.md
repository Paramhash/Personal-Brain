---
tags: ["tastytrade", "api", "errors", "authentication"]
created: 2023-10-27
reviewed: false
source_origin: "faq.md"
---
# Invalid Credentials Error (tastytrade API)

The `invalid_credentials` error occurs when the username or password provided during login is incorrect. A common cause is attempting to log into the wrong environment (e.g., using sandbox credentials for the production environment, or vice-versa).

## Diagnosis and Resolution

1.  **Check the environment URL:**
    *   **Sandbox Environment:** The base URL is `https://api.cert.tastyworks.com`.
    *   **Production Environment:** The base URL is `https://api.tastyworks.com`.
    Ensure your request is targeting the correct environment for your credentials.

2.  **Separate Credentials:** Remember that the [[./tastytrade-sandbox-environment.md|tastytrade Sandbox Environment]] and [[./tastytrade-production-environment.md|tastytrade Production Environment]] require separate sets of credentials (username and password).

3.  **Reset Password:**
    *   **Production Password:** Can be reset at [tastytrade.com](https://tastytrade.com).
    *   **Sandbox Password:** Can be reset via the [[./tastytrade-sandbox-environment.md|Sandbox page]] by looking for the "Reset it here" link under the sign-in button and entering your email address.

## Related Concepts

*   [[../entities/tastytrade.md|tastytrade]]
*   [[./tastytrade-sandbox-environment.md|tastytrade Sandbox Environment]]
*   [[./tastytrade-production-environment.md|tastytrade Production Environment]]
*   [[./tastytrade-auth-patterns.md|tastytrade Auth Patterns]]

---
*This information is derived from the tastytrade API FAQ.*