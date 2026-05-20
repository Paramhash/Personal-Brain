---
tags: ["data-model", "tastyworks-api", "option-chain", "nested-format"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Nested Option Chain Serializer (tastyworks API)

The `NestedOptionChainSerializer` data model provides a nested representation of an option chain, organized by expiration date, then by strike price, as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]]. This format minimizes redundant data by grouping shared attributes at the expiration level.

| Field | Type | Description |
|-------|------|-------------|
| `underlying-symbol` | string | The underlying equity symbol |
| `root-symbol` | string | The option root symbol |
| `option-chain-type` | string | The chain type |
| `shares-per-contract` | integer | Shares per contract |
| `tick-sizes` | object | Tick size rules |
| `deliverables` | object | Deliverable details |
| `expirations` | object | Nested object keyed by expiration date, each containing strikes with call/put option details |