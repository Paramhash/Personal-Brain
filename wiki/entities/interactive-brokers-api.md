---
tags: ["broker-api", "options", "greeks", "trading", "fintech"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# Interactive Brokers (IBKR) API

The Interactive Brokers (IBKR) API allows traders who already use IBKR for brokerage services to pull real-time [Options Greeks](../concepts/options-greeks.md) directly from their Trader Workstation (TWS) platform. This offers a highly integrated solution for both data acquisition and trade execution.

## Model

Using the `reqMktData()` function within the IBKR API, users can request specific "tick types" (e.g., 10, 11, 12) to receive real-time Delta, Gamma, Vega, and Theta values for options contracts.

## Key Features & Benefits

*   **Integrated Solution:** Combines market data access with trading capabilities through a single platform.
*   **Cost-Effective:** Greeks data is "free" if the user has the necessary [Market Data Subscriptions](../concepts/market-data-subscriptions.md) (such as OPRA/Bundle feeds), which typically cost around $15–$30/month.
*   **Direct Broker Access:** Eliminates the need for a separate data provider if already trading with IBKR.

## Limitations & Warnings

*   **API Clunkiness:** The IBKR API is often described as less modern and more "clunky" compared to contemporary REST or [WebSocket](../concepts/websockets.md) APIs offered by dedicated data providers like [ThetaData](../entities/thetadata.md) or [Polygon.io](../entities/polygon-io.md). This can sometimes lead to a steeper learning curve or more complex development.

## Suitability

The IBKR API is best suited for traders who are already integrated into the IBKR ecosystem and prioritize a unified platform for both analysis and execution. It allows for calculating custom metrics like [Regime Detection](../concepts/regime-detection.md) and executing trades through the same pipeline.

It is discussed as a "Direct-to-Broker" option in [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md).

---