---
tags: ["tastytrade", "api", "errors", "security", "timeout"]
created: 2023-10-27
reviewed: false
source_origin: "faq.md"
---
# IP Address Blocking and Request Timeouts (tastytrade API)

To protect user accounts from brute-force attacks, [[../entities/tastytrade.md|tastytrade]] implements a security measure that blocks an IP address if too many failed login attempts are received within a short period.

## Symptoms

When an IP address is blocked, API requests originating from that IP will suddenly time out, and you will be unable to connect to any tastytrade endpoints.

## Duration

The IP address block typically lasts for **8 hours**.

## Resolution

*   **Wait:** The block will usually clear automatically after 8 hours.
*   **Contact Support:** If immediate unblocking is required, you can contact `api.support@tastytrade.com` to request an unblock.

## Related Concepts

*   [[../entities/tastytrade.md|tastytrade]]
*   [[./tastytrade-invalid-credentials-error.md|Invalid Credentials Error]]

---
*This information is derived from the tastytrade API FAQ.*