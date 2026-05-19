---
tags: ["Index", "At-Time", "Price", "Historical Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index At-Time Price Endpoint

The `/index/at_time/price` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical index price reports for a specified millisecond of the day, across a given date range. This allows for precise historical analysis of index values at specific points in time.

## Endpoint Details:
*   **Path**: `/index/at_time/price`
*   **Method**: `GET`
*   **Summary**: Price
*   **Operation ID**: `index_at_time_price`
*   **Minimum Subscription**: `value`
*   **History Access**: `true`
*   **Description**:
    *   Retrieves historical indices price reports. [Exchanges](../../concepts/exchanges.md) typically generate a price report every second for popular indices like SPX.
    *   The `time_of_day` [API Parameter](../../concepts/api-parameters.md#time-of-day) represents the 00:00:00.000 ET that the price should be provided for.

## Parameters:
*   `symbol` (Required): The index symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `start_date` (Required): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#start-date).
*   `end_date` (Required): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#end-date).
*   `time_of_day` (Required): The time of the day to fetch data for (HH:mm:ss.SSS format); assumed to be America/New_York. See [API Parameters](../../concepts/api-parameters.md#time-of-day).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns specific at-time historical index price reports.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `sequence`: The exchange [sequence](/Articles/Data-And-Requests/Making-Requests.html#trade-sequences).
        *   `ext_condition1` to `ext_condition4`: Additional trade [conditions](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `condition`: The trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
        *   `size`: The amount of contracts / shares traded.
        *   `exchange`: The [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html) the trade was executed.
        *   `price`: The trade price.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.index_at_time_price(
    symbol='SPX',
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 8),
    time_of_day='09:30:01.000',
)
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [Index History Price Endpoint](../concepts/index-history-price-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---