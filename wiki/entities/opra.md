---
tags: ["Data Feed", "Options Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# OPRA (Options Price Reporting Authority)

OPRA, or the Options Price Reporting Authority, is a data feed responsible for disseminating last sale and quotation information for options contracts traded on participating U.S. options exchanges. In the context of the [Theta Data v3](../../entities/theta-data-v3.md) API, OPRA is the primary source for options market data.

## Key Characteristics:
*   **Options Data**: Provides comprehensive data for options contracts.
*   **Open Interest Reporting**: Reports open interest messages around 06:30 ET each morning, reflecting the previous trading day's open interest.
*   **Trade Conditions**: Specific trade conditions are reported by OPRA, though extended trade conditions are generally not applicable for options data from this feed.
*   **EOD Reports**: Theta Data generates its own End-of-Day (EOD) reports for options at 17:15 ET, as OPRA does not provide a national EOD report for options.

## Usage in Theta Data v3:
*   All [Option Data](../../concepts/option-data.md) endpoints, including historical trades, quotes, and Greeks calculations, rely on data sourced from OPRA.

## Related Concepts:
*   [Data Feeds](../../concepts/data-feeds.md)
*   [Exchanges](../../concepts/exchanges.md)
*   [Option Data](../../concepts/option-data.md)
*   [Trade Conditions](../../concepts/trade-conditions.md)
*   [Quote Conditions](../../concepts/quote-conditions.md)

---