---
tags: ["data-model", "tastyworks-api", "cryptocurrency", "crypto"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Cryptocurrency Instrument Definition (tastyworks API)

The `Cryptocurrency` data model describes a cryptocurrency instrument as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Internal identifier |
| `symbol` | string | The crypto trading pair (e.g., `BTC/USD`, `ETH/USD`) |
| `instrument-type` | string | Always `Cryptocurrency` |
| `description` | string | Full name (e.g., `Bitcoin`) |
| `short-description` | string | Abbreviated description |
| `active` | boolean | Whether the instrument is active |
| `is-closing-only` | boolean | Whether restricted to closing only |
| `streamer-symbol` | string | The DXLink streaming symbol |
| `tick-size` | number (double) | The minimum price increment |