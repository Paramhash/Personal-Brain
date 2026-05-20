---
tags: ["data-model", "tastyworks-api", "future-product", "futures"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Future Product Definition (tastyworks API)

The `FutureProduct` data model describes a futures product family (e.g., E-mini S&P 500), not an individual contract, as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `code` | string | The product code (e.g., `ES`, `NQ`, `CL`) |
| `root-symbol` | string | The root symbol for the product |
| `exchange` | string | The exchange (e.g., `CME`, `CFE`) |
| `description` | string | Product description (e.g., `E-mini S&P 500`) |
| `underlying-description` | string | Description of the underlying |
| `underlying-identifier` | string | Identifier for the underlying |
| `true-underlying-code` | string | The true underlying product code |
| `product-type` | string | The product type classification |
| `product-subtype` | string | The product sub-type |
| `market-sector` | string | The market sector (e.g., `Equity`, `Energy`, `Metals`) |
| `listed-months` | string | The months in which contracts are listed (e.g., `HMUZ` for March, June, September, December) |
| `active-months` | string | The currently active contract months |
| `notional-multiplier` | number (double) | The dollar multiplier per point move |
| `tick-size` | number (double) | The minimum price increment |
| `display-factor` | number (double) | Factor for display price conversion |
| `streamer-exchange-code` | string | Exchange code for the DXLink streamer |
| `small-notional` | boolean | Whether this is a small-notional (micro) product |
| `base-tick` | integer | The base tick value |
| `sub-tick` | integer | The sub-tick value |
| `price-format` | string | The price format notation |
| `security-group` | string | The security group |
| `contract-limit` | integer | Maximum number of contracts that can be held |
| `cash-settled` | boolean | Whether the product is cash-settled |
| `first-notice` | boolean | Whether the product has a first-notice date |
| `supported` | boolean | Whether the product is supported for trading on tastytrade |
| `back-month-first-calendar-symbol` | boolean | First calendar symbol for back months |