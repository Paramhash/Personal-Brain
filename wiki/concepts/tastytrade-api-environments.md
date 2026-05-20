---
tags: ["tastytrade", "API", "environment", "sandbox", "production"]
created: 2023-10-27
reviewed: false
source_origin: "getting-started.md"
---
# tastytrade API: Environments (Sandbox & Production)

The [tastytrade API](../entities/tastytrade.md) provides two distinct environments for development and live trading: Sandbox and Production. Each environment operates independently and requires separate credentials.

## Sandbox Environment

*   **Purpose**: A dedicated test environment designed for developing and testing applications without financial risk. All trades and data within Sandbox are simulated and do not involve real money.
*   **URL**: `https://api.cert.tastyworks.com`
*   **Recommendation**: It is highly recommended to thoroughly test your application in the Sandbox environment before deploying to Production. The Sandbox environment also features custom logic for simulating various order fill scenarios.

## Production Environment

*   **Purpose**: The live environment where all trades are real and involve actual funds.
*   **URL**: `https://api.tastyworks.com`
*   **Readiness**: You should only begin using the Production environment once you are confident in your application's functionality, having completed extensive testing in Sandbox.

For initial setup, refer back to the [tastytrade API: Getting Started Guide](./tastytrade-api-getting-started.md).