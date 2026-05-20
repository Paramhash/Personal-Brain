---
tags: ["tastytrade", "API", "market-data", "quotes", "streaming", "option-chain", "dxlink"]
created: 2023-10-27
reviewed: false
source_origin: "getting-started.md"
---
# tastytrade API: Market Data & Option Chains

The [tastytrade API](../entities/tastytrade.md) offers various ways to access market data, including streaming real-time quotes and fetching detailed option chains.

## Streaming Market Data

You can subscribe to a stream of market data to receive quotes for various instruments.

*   **Sandbox Environment**: Quotes in the [Sandbox environment](../concepts/tastytrade-api-environments.md) are delayed.
*   **Production Environment**: Quotes in the Production environment are real-time.

The Streaming Market Data page provides all necessary information to fetch these quotes.

## Fetching Market Data via HTTP

In addition to streaming, you can also fetch a single quote or a snapshot of market data via HTTP requests. The Market Data Guide will assist you in getting started with this method.

## Fetching an Option Chain

To view a comprehensive option chain for a specific ticker symbol, utilize the **List Nested Option Chains section** of the API. This endpoint will return:

*   Every put and call symbol supported by tastytrade for the given ticker.
*   All available expiration dates.
*   The `streamer-symbol`, which is the identifier to use when subscribing to quote data from [DxLink](../entities/dxlink.md).

Accessing market data is a key capability highlighted in the [tastytrade API: Getting Started Guide](./tastytrade-api-getting-started.md).