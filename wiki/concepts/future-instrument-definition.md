---
tags: ["data-model", "tastyworks-api", "future", "futures-contract"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Future Instrument Definition (tastyworks API)

The `Future` data model describes a single futures contract as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The futures symbol (e.g., `/ESM6`, `/NQU6`). Uses tastytrade symbology with `/` prefix |
| `product-code` | string | The product code (e.g., `ES`, `NQ`, `CL`, `GC`) |
| `product-group` | string | The product group classification |
| `exchange` | string | The exchange (e.g., `CME`, `CFE`) |
| `streamer-symbol` | string | The DXLink streaming symbol |
| `streamer-exchange-code` | string | The exchange code used in the DXLink streamer |
| `active` | boolean | Whether the contract is currently active |
| `active-month` | boolean | Whether this is the active (front-month) contract |
| `next-active-month` | boolean | Whether this is the next active month contract |
| `is-closing-only` | boolean | Whether trading is restricted to closing only |
| `is-tradeable` | boolean | Whether the contract can be traded |
| `expiration-date` | date | The contract expiration date |
| `expires-at` | datetime | The exact expiration timestamp |
| `last-trade-date` | date | The last date the contract can be traded |
| `first-notice-date` | date | The first notice date for physical delivery contracts |
| `closing-only-date` | date | The date when the contract becomes closing-only |
| `stops-trading-at` | datetime | Timestamp when the contract stops trading |
| `contract-size` | number (double) | The contract size |
| `notional-multiplier` | number (double) | The notional multiplier (used to calculate notional value) |
| `tick-size` | number (double) | The minimum price increment |
| `display-factor` | number (double) | Factor for converting internal prices to display prices |
| `main-fraction` | number (double) | Main fraction for price display (used in fractional pricing like bonds/treasuries) |
| `sub-fraction` | number (double) | Sub-fraction for price display |
| `security-id` | string | The security identifier |
| `true-underlying-symbol` | string | The true underlying symbol for the futures contract |
| `roll-target-symbol` | string | The symbol of the next contract for roll purposes |
| `back-month-first-calendar-symbol` | boolean | Whether this is the first calendar symbol for back months |
| `future-product` | object | Nested [[../concepts/future-product-definition.md|FutureProduct]] object with product-level metadata |
| `future-etf-equivalent` | object | ETF equivalent information (if applicable) |
| `tick-sizes` | object | Detailed tick size rules |
| `option-tick-sizes` | object | Tick size rules for options on this future |
| `spread-tick-sizes` | object | Tick size rules for spread orders |