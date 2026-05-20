---
tags: ["api", "market-data", "rest", "trading"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# Market Data API (Tastyworks)

The [[Tastyworks]] Market Data API is a [[REST API]] endpoint designed for fetching point-in-time market data snapshots for multiple symbols across various [[Market Data Instrument Types|instrument types]].

It is a non-streaming alternative to the [[DXLink]] [[WebSocket API]], suitable for scenarios requiring a one-time quote rather than continuous real-time data.

## Key Features
*   **Snapshot Data:** Provides current market data at the moment of the request.
*   **Multiple Instrument Types:** Supports equities, options, futures, cryptocurrencies, and indices.
*   **Batch Requests:** Allows fetching data for up to 100 symbols in a single request, combining different [[Market Data Instrument Types|instrument types]].
*   **Authentication:** Requires a valid session token via the `Authorization` header. See [[API Authentication]].

## Endpoints
*   `GET /market-data/by-type`: Fetches market data for multiple symbols, organized by instrument type.

## Data Models
The API primarily returns data in the form of [[MarketData Object]]s, which may contain nested [[Instrument Object]]s.

## Use Cases
*   Portfolio mark-to-market valuation.
*   Pre-trade pricing for limit orders.
*   Batch retrieval of quotes for various assets.
*   Detection of [[Trading Halts]].

## Important Notes
*   **Symbol Limit:** A maximum of 100 symbols per request across all instrument types. See [[API Rate Limits]].
*   **Parameter Naming:** Uses singular, hyphenated parameter names (e.g., `equity-option`). See [[API Naming Conventions]].
*   **Field Naming:** Uses camelCase for field names, which differs from other [[Tastyworks]] APIs that often use kebab-case. See [[API Naming Conventions]].
*   **Timestamps:** Uses epoch milliseconds for certain timestamps (e.g., `lastTradeTime`).

## Related
*   [[Tastyworks]]
*   [[REST API]]
*   [[WebSocket API]]
*   [[DXLink]]
*   [[MarketData Object]]
*   [[Instrument Object]]
*   [[API Authentication]]
*   [[Market Data Instrument Types]]
*   [[API Rate Limits]]
*   [[API Naming Conventions]]
*   [[Trading Halts]]