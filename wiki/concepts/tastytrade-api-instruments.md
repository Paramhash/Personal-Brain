---
tags: ["tastytrade", "API", "instruments", "securities", "trading"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Instruments

An instrument in the tastytrade API refers to any single tradeable security. Each instrument is uniquely identified by its [[../concepts/tastytrade-api-symbology.md|symbol]].

## Types of Instruments

The tastytrade API supports various types of instruments, including:

*   **Equities**: Stocks (e.g., AAPL).
*   **Equity Options**: Options contracts on individual stocks (e.g., AAPL call options).
*   **Futures**: Futures contracts (e.g., E-mini S&P 500 futures).
*   **Future Options**: Options contracts on futures (e.g., options on Crude Oil futures).
*   **Cryptocurrencies**: Digital assets (e.g., BTC/USD).

## Role in the API

*   **Identification**: The unique symbol of an instrument is used across the API for various operations.
*   **Order Submission**: When submitting an [[../concepts/tastytrade-api-orders.md|order]], you specify the instrument's symbol to indicate what you intend to trade.
*   **Position Tracking**: [[../concepts/tastytrade-api-positions.md|Positions]] are created and tracked based on the instrument's symbol.
*   **Market Data**: Instruments are the basis for retrieving market data, such as quotes and historical prices.

For more detailed information, refer to the tastytrade "Instruments Api Guide."

This concept is fundamental to [[../concepts/tastytrade-api-symbology.md|Symbology]], [[../concepts/tastytrade-api-orders.md|Orders]], and [[../concepts/tastytrade-api-positions.md|Positions]], and is a core part of the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].