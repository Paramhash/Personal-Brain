---
tags: ["data-model", "tastyworks-api", "order-quantity", "precision"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Quantity Decimal Precision (tastyworks API)

The `QuantityDecimalPrecision` data model defines the minimum order quantity precision rules for an instrument type, as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]]. This is crucial for determining the minimum order quantity increment for various instruments, especially for cryptocurrency and fractional equity orders.

| Field | Type | Description |
|-------|------|-------------|
| `instrument-type` | string | The instrument type this rule applies to |
| `symbol` | string | The specific symbol (if the rule is symbol-specific) |
| `value` | integer | The number of decimal places allowed in order quantities |
| `minimum-increment-precision` | integer | The minimum increment precision for quantities |