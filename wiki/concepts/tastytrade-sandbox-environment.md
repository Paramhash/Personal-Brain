---
tags: ["tastytrade", "api", "environments", "testing"]
created: 2023-10-27
reviewed: false
source_origin: "faq.md"
---
# tastytrade Sandbox Environment

The [[../entities/tastytrade.md|tastytrade]] Sandbox Environment is a testing environment for API development, separate from the live [[./tastytrade-production-environment.md|production environment]].

## Base URL

The base URL for the sandbox environment is `https://api.cert.tastyworks.com`.
For example, to fetch accounts, you would hit `https://api.cert.tastyworks.com/customers/me/accounts`.

## Credentials

*   Sandbox users require a separate set of credentials (username and password) from production users.
*   **Password Reset:** To reset your sandbox user password, navigate to the Sandbox page (on the tastytrade website) and look for the "Reset it here" link under the sign-in button. Enter your email address for further instructions.

## User Management

*   **Deletion:** Sandbox users **cannot** be deleted.
*   **Email Access Issues:** If you no longer have access to the email account associated with your sandbox user, contact `api.support@tastytrade.com`.

## Related Concepts

*   [[../entities/tastytrade.md|tastytrade]]
*   [[./tastytrade-production-environment.md|tastytrade Production Environment]]
*   [[./tastytrade-invalid-credentials-error.md|Invalid Credentials Error]]
*   [[./tastytrade-unconfirmed-user-error.md|Unconfirmed User Error]]

---
*This information is derived from the tastytrade API FAQ.*