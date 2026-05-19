---
tags: ["Index", "Snapshot", "Price", "Real-time Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index Snapshot Price Endpoint

The `/index/snapshot/price` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API retrieves the real-time last index price for specified index symbols. This provides an immediate view of the current value of an index.

## Endpoint Details:
*   **Path**: `/index/snapshot/price`
*   **Method**: `GET`
*   **Summary**: Price
*   **Operation ID**: `index_snapshot_price`
*   **Minimum Subscription**: `standard`
*   **Description**:
    *   Retrieves a real-time last index price.
    *   [Exchanges](../../concepts/exchanges.md) typically generate a price report every second for popular indices like SPX.

## Parameters:
*   `symbol` (Required): The index symbol. Specify `*` for all symbols or a comma-separated list. See [API Parameters](../../concepts/api-parameters.md#multi-symbol) and [Symbols](../../concepts/symbols.md).
*   `min_time` (Optional): Filters snapshots to include only data with a timestamp greater or equal to the specified value (HH:mm:ss.SSS format). See [API Parameters](../../concepts/api-parameters.md#min-time).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns last index price.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `symbol`: The symbol of the contract, or stock / underlying asset / option / index.
        *   `price`: The trade price.

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.index_snapshot_price(symbol=['SPX'])
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [Index History Price Endpoint](../concepts/index-history-price-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---