---
tags: ["data-model", "tastyworks-api", "future-option", "option"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Future Option Instrument Definition (tastyworks API)

The `FutureOption` data model describes a single futures option contract as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The tastytrade futures option symbol (e.g., `./ESZ9 EW4U9 190927P2975`) |
| `underlying-symbol` | string | The underlying futures contract symbol |
| `product-code` | string | The futures product code |
| `root-symbol` | string | The option root symbol |
| `option-root-symbol` | string | The option root symbol for the futures option series |
| `option-type` | string | `C` for call, `P` for put |
| `strike-price` | number (double) | The strike price |
| `strike-factor` | number (double) | Factor applied to the strike price |
| `expiration-date` | date | The expiration date |
| `expires-at` | datetime | The exact expiration timestamp |
| `days-to-expiration` | integer | Days until expiration |
| `exercise-style` | string | `American` or `European` |
| `settlement-type` | string | `Physical` or `Cash` |
| `exchange` | string | The exchange |
| `streamer-symbol` | string | The DXLink streaming symbol |
| `multiplier` | number (double) | The contract multiplier |
| `display-factor` | number (double) | Factor for display price conversion |
| `notional-value` | number (double) | The notional value of the contract |
| `future-price-ratio` | number (double) | Ratio between the option and underlying future price |
| `underlying-count` | number (double) | Number of underlying contracts per option |
| `active` | boolean | Whether the contract is active |
| `is-closing-only` | boolean | Whether restricted to closing only |
| `is-confirmed` | boolean | Whether the contract terms are confirmed |
| `is-exercisable-weekly` | boolean | Whether the option is exercisable weekly |
| `is-primary-deliverable` | boolean | Whether this is the primary deliverable |
| `is-vanilla` | boolean | Whether this is a vanilla (standard) option |
| `last-trade-time` | string | The last time the contract can be traded |
| `stops-trading-at` | datetime | Timestamp when the option stops trading |
| `maturity-date` | date | The maturity date |
| `security-id` | string | The security identifier |
| `future-option-product` | object | Nested [[../concepts/future-option-product-definition.md|FutureOptionProduct]] metadata |