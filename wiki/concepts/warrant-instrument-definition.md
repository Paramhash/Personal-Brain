---
tags: ["data-model", "tastyworks-api", "warrant"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Warrant Instrument Definition (tastyworks API)

The `Warrant` data model describes a warrant instrument as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `symbol` | string | The warrant symbol (e.g., `RGTIW`) |
| `instrument-type` | string | Always `Warrant` |
| `description` | string | Description of the warrant |
| `cusip` | string | The CUSIP identifier |
| `listed-market` | string | The exchange where the warrant is listed |
| `active` | boolean | Whether the warrant is active |
| `is-closing-only` | boolean | Whether restricted to closing only |