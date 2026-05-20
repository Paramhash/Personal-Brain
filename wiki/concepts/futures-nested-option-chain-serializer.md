---
tags: ["data-model", "tastyworks-api", "futures-option-chain", "nested-format"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Futures Nested Option Chain Serializer (tastyworks API)

The `FuturesNestedOptionChainSerializer` data model provides a nested representation for futures option chains, organized by underlying future and expiration, as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `futures` | object | The underlying futures contracts |
| `option-chains` | object | Option chains nested by underlying future and expiration |