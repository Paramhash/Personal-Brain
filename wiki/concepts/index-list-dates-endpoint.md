---
tags: ["Index", "List", "Dates", "Availability"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index List Dates Endpoint

The `/index/list/dates` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve a list of all dates for which data is available for a specified index symbol. This endpoint is updated overnight.

## Endpoint Details:
*   **Path**: `/index/list/dates`
*   **Method**: `GET`
*   **Summary**: Dates
*   **Operation ID**: `index_list_dates`
*   **Minimum Subscription**: `free`
*   **Description**:
    *   Lists all dates of data that are available for an index with a given symbol.
    *   This endpoint is updated overnight.

## Parameters:
*   `symbol` (Required): The index symbol. Specify `*` for all symbols or a comma-separated list. See [API Parameters](../../concepts/api-parameters.md#multi-symbol) and [Symbols](../../concepts/symbols.md).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns a list of all dates for an index for a given symbol.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `date`: The date formatted as YYYY-MM-DD.

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.index_list_dates(symbol=['SPX'])
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [Index List Symbols Endpoint](../concepts/index-list-symbols-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---