---
tags: ["tastytrade", "API", "account", "balance", "positions", "streaming"]
created: 2023-10-27
reviewed: false
source_origin: "getting-started.md"
---
# tastytrade API: Account Balances, Positions & Updates

The [tastytrade API](../entities/tastytrade.md) provides comprehensive access to your account-specific data, including balances, open positions, and real-time updates.

## Fetching Account Balances

To view the current financial status of your account, you can use the **List Account Balances endpoint**. This will provide details on your cash, buying power, and other relevant balance metrics.

## Fetching Account Positions

Once an order fills (as described in [Order Submission & Management](./tastytrade-api-order-submission.md)), a new position will be created in your account. To retrieve a list of all your current holdings, use the **List Account Positions endpoint**. This will detail each instrument you hold, along with quantities and other relevant position data.

## Streaming Account Updates

For real-time notifications regarding changes to your account, such as new orders, fills, or balance adjustments, you can subscribe to **Streaming Account Data**. This allows your application to react instantly to events without needing to constantly poll the API.

Accessing account data is a fundamental step outlined in the [tastytrade API: Getting Started Guide](./tastytrade-api-getting-started.md).