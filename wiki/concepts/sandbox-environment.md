yaml
---
tags: ["api", "testing", "development", "tastyworks", "environment"]
created: 2023-10-27
reviewed: false
source_origin: "sandbox.md"
---
# Sandbox Environment

The Sandbox Environment is a controlled system designed for open-API users to test and develop against the [[../entities/tastyworks.md|Tastyworks]] API without affecting live trading accounts.

## Key Characteristics

*   **Purpose**: Provides a safe, isolated space for API development and testing.
*   **Reset Cycle**: The system undergoes a full reset every 24 hours. This process deletes all trades, transactions, and positions, and clears out account balances.
*   **Persistent Data**: User, customer, and account records are *not* affected by the daily reset.
*   **Authentication**: Requires signing in with specific sandbox user credentials. All subsequent actions (e.g., customer or account creation) are tied to this sandbox user.
*   **Base API URL**: `api.cert.tastyworks.com`
*   **Websocket URL**: `streamer.cert.tastyworks.com` (for account streamer updates)
*   **Market Data**: Quotes in the sandbox environment are always 15-minutes delayed.
*   **Instrumentation Lag**: The sandbox environment's instrumentation may occasionally lag behind the live trading environment. This can sometimes lead to valid symbols failing with `422` error codes. Users experiencing this should contact `api.support@tastytrade.com` for assistance.

## Service Limitations

Not all services available in the live trading system are currently accessible in the sandbox environment. The following services are exclusively available in the live system:

*   Net liquidating value history
*   Market metrics
*   Real-time market-data (streaming market-data is available via a delayed feed in the sandbox)

## OAuth2 Support

[[./oauth2-tastyworks-sandbox.md|OAuth2]] is fully supported within the Sandbox Environment. Users can create and manage personal applications using dedicated tools available after logging in with their sandbox user. It is important to note that the client secret for an application is displayed only once upon creation; if lost, it must be regenerated.

---
### Related Notes
*   [[../entities/tastyworks.md]]
*   [[./oauth2-tastyworks-sandbox.md]]