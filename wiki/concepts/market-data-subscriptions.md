---
tags: ["market-data", "trading", "fintech", "data-feeds"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# Market Data Subscriptions

Market data subscriptions refer to paid services that provide access to real-time or historical financial data from exchanges and other data sources. These subscriptions are essential for traders, investors, and quantitative analysts who require up-to-date information to make informed decisions.

## Types of Market Data

*   **Real-time Data:** Live streaming prices, quotes, and trade data as they occur.
*   **Historical Data:** Past price and volume data, often used for backtesting and analysis.
*   **Level 1 Data:** Best bid and ask prices, along with the last traded price and volume.
*   **Level 2 Data:** Order book depth, showing multiple bid and ask prices and their corresponding sizes.
*   **Options Data:** Includes options chains, [Options Greeks](../concepts/options-greeks.md), and implied volatility.

## Common Feeds

*   **OPRA (Options Price Reporting Authority):** A consolidated feed for real-time options quotes and trades from all participating U.S. options exchanges.
*   **Bundle Feeds:** Packages that combine data from multiple exchanges or asset classes, often offered by brokers or data vendors.

## Cost and Providers

The cost of market data subscriptions varies widely depending on the exchanges covered, the level of data (Level 1, Level 2), and whether it's for professional or non-professional use. Brokers like [Interactive Brokers (IBKR) API](../entities/interactive-brokers-api.md) often require specific market data subscriptions to access real-time data, including [Options Greeks](../concepts/options-greeks.md), through their APIs. Dedicated data providers like [ThetaData](../entities/thetadata.md) and [Polygon.io](../entities/polygon-io.md) also offer their own subscription models.

Access to these subscriptions is a prerequisite for utilizing many [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md).

---