---
tags: ["Index", "History", "Price", "Time Series"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index History Price Endpoint

The `/index/history/price` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical index price reports for a specified index symbol over a given date range and at a defined [Time Interval](../../concepts/time-intervals.md).

## Endpoint Details:
*   **Path**: `/index/history/price`
*   **Method**: `GET`
*   **Summary**: Price
*   **Operation ID**: `index_history_price`
*   **Minimum Subscription**: `value`
*   **History Access**: `true`
*   **Description**:
    *   Retrieves historical indices price reports. [Exchanges](../../concepts/exchanges.md) typically generate a price report every second for popular indices like SPX.
    *   When the `interval` [API Parameter](../../concepts/api-parameters.md#interval) is specified, the returned data represents the price at the exact time of each timestamp. If the timestamp in the response is 10:30:00, the price field represents the price at that exact time of the day.
    *   A price update from the exchange is omitted if the price remained the same from the previous update.
    *   Multi-day requests are limited to 1 month of data.

## Parameters:
*   `date` (Optional): The date to fetch data for. If present, this overrides `start_date` and `end_date`. See [API Parameters](../../concepts/api-parameters.md#opt-date).
*   `symbol` (Required): The index symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `start_time` (Optional): The start time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#start-time).
*   `end_time` (Optional): The end time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#end-time).
*   `interval` (Required): The size of the time interval. See [API Parameters](../../concepts/api-parameters.md#interval) and [Time Intervals](../../concepts/time-intervals.md).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).
*   `opt_start_date` (Optional): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-start-date).
*   `opt_end_date` (Optional): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-end-date).

## Responses:
*   **200 OK**: Returns historical index price reports.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `price`: The trade price.

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.index_history_price(symbol='SPX', interval='1m')
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [Index Snapshot Price Endpoint](../concepts/index-snapshot-price-endpoint.md)
*   [Index At-Time Price Endpoint](../concepts/index-at-time-price-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---