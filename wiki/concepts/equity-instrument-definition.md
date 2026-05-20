---
tags: ["data-model", "tastyworks-api", "equity", "stock", "etf"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Equity Instrument Definition (tastyworks API)

The `Equity` data model describes an equity (stock or ETF) instrument as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The ticker symbol (e.g., `AAPL`) |
| `instrument-type` | string | Always `Equity` for stocks/ETFs |
| `instrument-sub-type` | string | Sub-type classification (e.g., `Common Stock`, `ADR`) |
| `description` | string | Full name/description of the equity (e.g., `Apple Inc.`) |
| `short-description` | string | Abbreviated description |
| `active` | boolean | Whether the instrument is currently active and tradeable |
| `is-closing-only` | boolean | Whether trading is restricted to closing transactions only |
| `is-options-closing-only` | boolean | Whether options on this equity are restricted to closing only |
| `is-etf` | boolean | Whether the instrument is an ETF |
| `is-index` | boolean | Whether the instrument is an index |
| `is-fractional-quantity-eligible` | boolean | Whether fractional share orders are supported |
| `is-illiquid` | boolean | Whether the instrument is classified as illiquid |
| `listed-market` | string | The exchange where the equity is listed |
| `streamer-symbol` | string | The symbol to use for DXLink streaming market data |
| `lendability` | string | Short-selling availability: `Easy To Borrow`, `Locate Required`, or `Preborrow` |
| `borrow-rate` | number (double) | The current borrow rate for short selling |
| `halted-at` | datetime | Timestamp when trading was halted (null if not halted) |
| `stops-trading-at` | datetime | Timestamp when the instrument stops trading |
| `market-time-instrument-collection` | string | The market time collection this instrument belongs to |
| `country-of-incorporation` | string | Country where the company is incorporated |
| `country-of-taxation` | string | Country of taxation |
| `underlying-product-type` | string | The underlying product type classification |
| `overnight-trading-permitted` | boolean | Whether overnight/extended-hours trading is permitted |
| `bypass-manual-review` | boolean | Whether orders can bypass manual review |
| `tick-sizes` | object | Tick size rules for the equity |
| `option-tick-sizes` | object | Tick size rules for options on this equity |