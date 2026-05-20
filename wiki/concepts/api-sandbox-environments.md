---
tags: ["api", "testing", "development", "sandbox", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# API Sandbox Environments

A sandbox environment is a crucial component for developers working with APIs, providing a safe and isolated space to test applications without affecting live production data or financial accounts. The [[../entities/tastytrade-open-api.md|tastytrade Open API]] offers a dedicated sandbox environment.

## tastytrade Sandbox Specifics
*   **Base URL**: `https://api.cert.tastyworks.com`
*   **Data Reset**: The sandbox environment typically resets every 24 hours, ensuring a fresh state for testing.
*   **Delayed Quotes**: Market data in the sandbox is usually delayed, not real-time.
*   **Service Limitations**: Not all production services may be available in the sandbox. For example, certain historical data (net-liq history), market metrics, or real-time market data streaming might be absent or limited.
*   **Account Creation**: Developers can create sandbox accounts to simulate trading activities.
*   **Password Reset**: Specific procedures are available for resetting sandbox account passwords.

Using the sandbox allows developers to:
*   Experiment with API calls and features.
*   Develop and debug trading algorithms.
*   Test integration with the tastytrade platform.
*   Understand API behavior and responses in a controlled setting.

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]