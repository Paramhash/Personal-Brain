---
tags: ["Index", "History", "OHLC", "Time Series"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index History OHLC Endpoint

The `/index/history/ohlc` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides aggregated historical Open, High, Low, Close (OHLC) bars for a specified index symbol over a given date range and at a defined [Time Interval](../../concepts/time-intervals.md).

## Endpoint Details:
*   **Path**: `/index/history/ohlc`
*   **Method**: `GET`
*   **Summary**: Open High Low Close
*   **Operation ID**: `index_history_ohlc`
*   **Minimum Subscription**: `standard`
*   **History Access**: `true`
*   **Description**:
    *   Aggregated OHLC bars that use [SIP rules](/Articles/Data-And-Requests/OHLC-EOD.html) for each bar.
    *   The timestamp of the bar represents the opening time of the bar. For a trade to be part of the bar: `bar timestamp` <= `trade time` < `bar timestamp + interval`.
    *   [Exchanges](../../concepts/exchanges.md) typically generate a price report every second for popular indices like SPX.

## Parameters:
*   `symbol` (Required): The index symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `start_date` (Required): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#start-date).
*   `end_date` (Required): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#end-date).
*   `interval` (Required): The size of the time interval. See [API Parameters](../../concepts/api-parameters.md#interval) and [Time Intervals](../../concepts/time-intervals.md).
*   `start_time` (Optional): The start time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#start-time).
*   `end_time` (Optional): The end time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#end-time).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns OHLC for a given symbol between specified dates (inclusive) with a one minute interval.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `open`: The opening trade price.
        *   `high`: The highest traded price.
        *   `low`: The lowest traded price.
        *   `close`: The closing traded price.
        *   `volume`: The amount of contracts / shares traded.
        *   `count`: The amount of trades.
        *   `vwap`: The volume weighted average price of the trading session.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.index_history_ohlc(
    symbol='SPX',
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
    interval='1m',
)
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [Index Snapshot OHLC Endpoint](../concepts/index-snapshot-ohlc-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---