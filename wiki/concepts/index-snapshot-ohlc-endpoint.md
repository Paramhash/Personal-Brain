---
tags: ["Index", "Snapshot", "OHLC", "Real-time Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index Snapshot OHLC Endpoint

The `/index/snapshot/ohlc` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API retrieves the real-time current day's Open, High, Low, Close (OHLC) data for specified index symbols. This provides an immediate summary of an index's price action during the current trading session.

## Endpoint Details:
*   **Path**: `/index/snapshot/ohlc`
*   **Method**: `GET`
*   **Summary**: Open High Low Close
*   **Operation ID**: `index_snapshot_ohlc`
*   **Minimum Subscription**: `standard`
*   **Description**:
    *   Retrieves the real-time current day OHLC.
    *   [Exchanges](../../concepts/exchanges.md) typically generate a price report every second for popular indices like SPX.

## Parameters:
*   `symbol` (Required): The index symbol. Specify `*` for all symbols or a comma-separated list. See [API Parameters](../../concepts/api-parameters.md#multi-symbol) and [Symbols](../../concepts/symbols.md).
*   `min_time` (Optional): Filters snapshots to include only data with a timestamp greater or equal to the specified value (HH:mm:ss.SSS format). See [API Parameters](../../concepts/api-parameters.md#min-time).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns OHLC for a given index price change.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `symbol`: The symbol of the contract, or stock / underlying asset / option / index.
        *   `open`: The opening trade price.
        *   `high`: The highest traded price.
        *   `low`: The lowest traded price.
        *   `close`: The closing traded price.
        *   `volume`: The amount of contracts / shares traded.
        *   `count`: The amount of trades.

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.index_snapshot_ohlc(symbol=['SPX'])
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [Index History OHLC Endpoint](../concepts/index-history-ohlc-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---