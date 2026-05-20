---
tags: ["data-model", "tastyworks-api", "equity-option", "option"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Equity Option Instrument Definition (tastyworks API)

The `EquityOption` data model describes a single equity option contract as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The OCC option symbol (e.g., `AAPL  260417C00200000`). Format: 6-char left-padded underlying + YYMMDD expiration + C/P + 8-digit strike (price × 1000) |
| `instrument-type` | string | Always `Equity Option` |
| `underlying-symbol` | string | The underlying equity symbol |
| `root-symbol` | string | The option root symbol (usually same as underlying, but differs for adjusted options like SPXW) |
| `option-type` | string | `C` for call, `P` for put |
| `strike-price` | number (double) | The strike price of the option |
| `expiration-date` | date | The expiration date of the option contract |
| `expiration-type` | string | The expiration type (e.g., `Regular`, `Weekly`, `Quarterly`, `End of Month`) |
| `expires-at` | datetime | The exact expiration timestamp |
| `exercise-style` | string | `American` or `European` |
| `settlement-type` | string | `Physical` (stock delivery) or `Cash` (cash-settled, e.g., index options) |
| `option-chain-type` | string | The option chain type classification |
| `shares-per-contract` | integer | Number of shares per contract (typically `100`, but can vary for adjusted options) |
| `days-to-expiration` | integer | Number of days until expiration |
| `active` | boolean | Whether the option contract is active |
| `is-closing-only` | boolean | Whether trading is restricted to closing only |
| `listed-market` | string | The exchange where the option is listed |
| `streamer-symbol` | string | The DXLink streaming symbol |
| `halted-at` | datetime | Timestamp when trading was halted |
| `stops-trading-at` | datetime | Timestamp when the option stops trading |
| `market-time-instrument-collection` | string | Market time collection |
| `old-security-number` | string | Legacy security number identifier |