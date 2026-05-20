---
tags: ["market-data", "instrument", "api"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# Market Data Instrument Types

The [[Market Data API (Tastyworks)|Tastyworks Market Data API]] supports fetching data for various financial [[Instrument Object|instrument types]]. These types are used both as query parameters in requests and as values within the [[MarketData Object]] and [[Instrument Object]] responses.

## Supported Types
*   `equity`: Common stock symbols (e.g., `AAPL`, `SPY`).
*   `equity-option`: Equity option symbols in OCC format (e.g., `AAPL  260619C00200000`).
*   `future`: Futures symbols (e.g., `/ESM6`).
*   `future-option`: Futures option symbols in tastytrade format.
*   `cryptocurrency`: Cryptocurrency symbols (e.g., `BTC/USD`).
*   `index`: Index symbols (e.g., `SPX`, `VIX`).
*   `Bond` (mentioned in `instrumentType` field description).
*   Other types may exist.

## Important Notes
*   **Parameter Naming:** When used as query parameters, these types must be in **singular hyphenated** form (e.g., `equity-option`, not `equity-options`). See [[API Naming Conventions]].
*   **Symbol Limit:** The combined total of symbols across all instrument type parameters cannot exceed 100 per request. See [[API Rate Limits]].

## Related
*   [[Market Data API (Tastyworks)]]
*   [[MarketData Object]]
*   [[Instrument Object]]
*   [[API Rate Limits]]
*   [[API Naming Conventions]]