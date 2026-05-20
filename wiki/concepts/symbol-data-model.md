---
tags: ["data-model", "api", "instrument-data"]
created: 2023-10-27
reviewed: false
source_origin: "symbol-search.md"
---
# SymbolData Model

The `SymbolData` model represents a single financial instrument returned by the [[../entities/tastyworks-symbol-search-api.md|Tastyworks Symbol Search API]]. It provides essential information for identifying and categorizing an instrument.

## Fields

*   `symbol` (string): The full instrument symbol (e.g., `AAPL`, `SPY`).
*   `description` (string): Company name or instrument description (e.g., `Apple Inc.`, `S&P 500 ETF Trust`).
*   `listed-market` (string): The exchange where the instrument is listed (e.g., [[../entities/nasdaq.md|NASDAQ]], [[../entities/nyse.md|NYSE]]).
*   `instrument-type` (string): The type of financial instrument (e.g., [[../concepts/equity-instrument.md|Equity]], [[../concepts/futures-instrument.md|Future]], [[../concepts/options-instrument.md|Option]]).
*   `options` (boolean): Indicates whether the instrument has listed options available for trading.
*   `price-increments` (string): Human-readable description of the price increment (tick size) rules for the instrument.
*   `trading-hours` (string): Human-readable trading hours for the instrument.