---
tags: ["data-model", "tastyworks-api", "future-option-product", "futures-options"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# Future Option Product Definition (tastyworks API)

The `FutureOptionProduct` data model describes a futures option product family as returned by the [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]].

| Field | Type | Description |
|-------|------|-------------|
| `root-symbol` | string | The root symbol for the futures option product |
| `code` | string | The product code |
| `exchange` | string | The exchange |
| `product-type` | string | The product type |
| `product-subtype` | string | The product sub-type |
| `market-sector` | string | The market sector |
| `expiration-type` | string | The expiration type |
| `settlement-delay-days` | integer | Number of days between expiration and settlement |
| `display-factor` | number (double) | Display factor for price conversion |
| `cash-settled` | boolean | Whether the product is cash-settled |
| `is-am-settled` | boolean | Whether settlement occurs at the AM opening price |
| `itm-rule` | string | The in-the-money exercise rule |
| `supported` | boolean | Whether the product is supported on tastytrade |