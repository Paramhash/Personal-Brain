---
tags: ["Index", "History", "End of Day"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index History EOD Endpoint

The `/index/history/eod` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical End-of-Day (EOD) reports for a specified index symbol over a given date range.

## Endpoint Details:
*   **Path**: `/index/history/eod`
*   **Method**: `GET`
*   **Summary**: End of Day
*   **Operation ID**: `index_history_eod`
*   **Minimum Subscription**: `free`
*   **History Access**: `true`
*   **Description**:
    *   Since the indices feeds do not provide a national EOD report, Theta Data generates a national EOD report at 17:15 ET each day.

## Parameters:
*   `symbol` (Required): The index symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `start_date` (Required): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#start-date).
*   `end_date` (Required): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#end-date).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns EOD report for a given symbol between specified dates (inclusive).
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `created`: The datetime the report was generated (YYYY-MM-DDTHH:mm:ss.SSS format).
        *   `last_trade`: The datetime of the last trade (YYYY-MM-DDTHH:mm:ss.SSS format).
        *   `open`: The opening trade price.
        *   `high`: The highest traded price.
        *   `low`: The lowest traded price.
        *   `close`: The closing traded price.
        *   `volume`: The amount of contracts / shares traded.
        *   `count`: The amount of trades.
        *   `bid_size`: The last NBBO bid size.
        *   `bid_exchange`: The last NBBO bid [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html).
        *   `bid`: The last NBBO bid price.
        *   `bid_condition`: The last NBBO bid [condition](/Articles/Errors-Exchanges-Conditions/Quote-Conditions.html).
        *   `ask_size`: The last NBBO ask size.
        *   `ask_exchange`: The last NBBO ask [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html).
        *   `ask`: The last NBBO ask price.
        *   `ask_condition`: The last NBBO ask [condition](/Articles/Errors-Exchanges-Conditions/Quote-Conditions.html).

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.index_history_eod(
    symbol='SPX',
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 8),
)
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [API Endpoints](../concepts/api-endpoints.md)
*   [Trade Conditions](../concepts/trade-conditions.md)
*   [Quote Conditions](../concepts/quote-conditions.md)

---