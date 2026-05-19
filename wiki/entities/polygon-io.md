yaml
---
tags: ["data-provider", "financial-data", "options-data", "market-data"]
created: 2023-10-27
reviewed: false
source_origin: "maopm_horizon_spread_blueprint.md"
---
```
# Polygon.io

**Polygon.io** is a financial data provider offering real-time and historical market data, including options, equities, and forex. It is known for providing raw, granular tick-level data feeds.

Key features and characteristics of Polygon.io include:
*   **Data Feed Type:** Delivers tick-level trades and quotes primarily via WebSockets for real-time streaming.
*   **Granularity:** Provides millisecond-level tick data, offering a very fine-grained view of market activity.
*   **Chain Architecture:** Emits individual tick events per contract identifier in flat message streams, requiring the client to reconstruct order book and chain context.
*   **Implied Volatility / Greek Engines:** Provides raw data. Users are responsible for calculating implied volatility surfaces, performing interpolation, and computing Greeks locally.
*   **Compute Overhead for Client:** High, as the client must construct the entire order book and IV surface from raw ticks manually.

For systems like the [MAOPM architecture for signal fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md), Polygon.io is recommended for users who desire a pure, un-opinionated, ultra-low-latency raw firehose and have the dedicated compute infrastructure (e.g., a 64-core cluster with an in-memory database) to build their own custom SABR or local volatility surface models from raw ticks.

---