---
tags: ["data-model", "tastyworks-api", "option-chain", "compact-format"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Compact Option Chain Serializer (tastyworks API)

The `CompactOptionChainSerializer` data model provides a compact representation of an option chain, designed to minimize response size, as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]]. Symbols and streamer symbols are returned as delimited strings rather than full objects.

| Field | Type | Description |
|-------|------|-------------|
| `underlying-symbol` | string | The underlying equity symbol |
| `root-symbol` | string | The option root symbol |
| `option-chain-type` | string | The chain type |
| `settlement-type` | string | `Physical` or `Cash` |
| `shares-per-contract` | integer | Shares per contract |
| `expiration-type` | string | The expiration type |
| `deliverables` | object | Deliverable details |
| `symbols` | string | Delimited string of all option symbols in the chain |
| `streamer-symbols` | string | Delimited string of all DXLink streamer symbols |