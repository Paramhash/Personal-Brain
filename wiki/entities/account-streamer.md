---
tags: ["entity", "tool", "api", "real-time"]
created: 2023-10-27
reviewed: false
source_origin: "order-management.md"
---
# Account Streamer

The Account Streamer is a tool or service designed to provide real-time updates for account-related activities, particularly [[../concepts/order-status.md|order status]] changes.

It is explicitly recommended as the preferred method for receiving real-time order updates, as opposed to repeatedly polling API endpoints like [[../concepts/live-orders.md|Live Orders]]. The streamer offers lower latency and avoids potential rate-limit issues that can arise from frequent polling, which can degrade platform performance.

## Key Benefits
*   **Real-time Updates**: Delivers information as it occurs.
*   **Lower Latency**: Faster delivery of critical updates.
*   **No Rate-Limit Issues**: Designed for continuous, high-frequency updates without throttling.
*   **Improved Performance**: Prevents degradation of the overall platform by reducing API polling load.

## Related
*   [[../concepts/order-management.md|Order Management]]
*   [[../concepts/live-orders.md|Live Orders]]
*   [[../concepts/order-status.md|Order Status]]