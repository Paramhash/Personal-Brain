yaml
---
tags: ["data-provider", "financial-data", "options-data", "market-data"]
created: 2023-10-27
reviewed: false
source_origin: "maopm_horizon_spread_blueprint.md"
---
```
# ThetaData

**ThetaData** is a financial data provider specializing in options market data. It offers services tailored for quantitative analysis and trading systems, particularly those requiring pre-processed or high-level derivatives data.

Key features and characteristics of ThetaData include:
*   **Data Feed Type:** Primarily offers a Rest API for historical data and specialized binary WebSockets for streaming real-time data.
*   **Granularity:** Provides nanosecond/microsecond-level contract events.
*   **Chain Architecture:** Utilizes hierarchical framing, allowing users to structure queries by underlying or root symbol, which can simplify data ingestion for complex option chains.
*   **Implied Volatility / Greek Engines:** A significant advantage is that ThetaData provides pre-calculated real-time Greeks and implied volatility (IV) surfaces directly within its data tier. This offloads substantial computational burden from the client.
*   **Compute Overhead for Client:** Relatively low, as the provider handles the compute-heavy step of building the IV surface and calculating real-time Greeks on their servers.

For systems like the [MAOPM architecture for signal fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md), ThetaData is recommended when the goal is to minimize immediate infrastructure overhead, allowing the MAOPM data ingestion agent to pull clean, pre-filtered constant-maturity variance profiles directly.

---