---
tags: ["Option", "History", "OHLC", "Time Series"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History OHLC Endpoint

The `/option/history/ohlc` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides aggregated historical Open, High, Low, Close (OHLC) bars for a specified options contract over a given date range and at a defined [Time Interval](../../concepts/time-intervals.md).

## Endpoint Details:
*   **Path**: `/option/history/ohlc`
*   **Method**: `GET`
*   **Summary**: Open High Low Close
*   **Operation ID**: `option_history_ohlc`
*   **Minimum Subscription**: `value`
*   **History Access**: `true`
*   **Description**:
    *   Aggregated OHLC bars that use [SIP rules](/Articles/Data-And-Requests/OHLC-EOD.html) for each bar.
    *   The timestamp of the bar represents the opening time of the bar. For a trade to be part of the bar: `bar timestamp` <= `trade time` < `bar timestamp + interval`.
    *   Multi-day requests are limited to 1 month of data.

## Parameters:
*   `opt_date` (Optional): The date to fetch data for. If present, this overrides `start_date` and `end_date`. See [API Parameters](../../concepts/api-parameters.md#opt-date).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration_no_star` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration-no-star) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `interval` (Required): The size of the time interval. See [API Parameters](../../concepts/api-parameters.md#interval) and [Time Intervals](../../concepts/time-intervals.md).
*   `start_time` (Optional): The start time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#start-time).
*   `end_time` (Optional): The end time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#end-time).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).
*   `opt_start_date` (Optional): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-start-date).
*   `opt_end_date` (Optional): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-end-date).

## Responses:
*   **200 OK**: Returns OHLC for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
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
df = client.option_history_ohlc(
    symbol='AAPL',
    expiration=date(2023, 11, 3),
    interval='1m',
)
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Snapshot OHLC Endpoint](../concepts/option-snapshot-ohlc-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---