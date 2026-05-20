---
tags: ["data-model", "api", "market-data"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# Instrument Object

The `Instrument` object is a nested data structure found within the [[MarketData Object]] returned by the [[Market Data API (Tastyworks)|Tastyworks Market Data API]]. It provides metadata specific to the financial instrument.

## Structure and Fields
*   `symbol` (string): The instrument symbol.
*   `instrumentType` (string): The [[Market Data Instrument Types|instrument type]] (e.g., `EQUITY`, `FUTURE`).
*   `rootSymbol` (string): The root symbol (especially for options).
*   `exchange` (string): The exchange where the instrument trades (e.g., `CME`, `EQUITY`).
*   `instrumentKey` (object): A compound key containing `symbol` and `instrumentType`.
*   `underlyingInstrument` ([[Instrument Object|Instrument]]): For derivatives, this field contains the `Instrument` object of the underlying asset.

## Related
*   [[MarketData Object]]
*   [[Market Data API (Tastyworks)]]
*   [[Market Data Instrument Types]]