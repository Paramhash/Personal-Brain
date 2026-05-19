---
tags: ["Index", "List", "Symbols", "Availability"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Index List Symbols Endpoint

The `/index/list/symbols` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve a list of all traded symbols for indices. This endpoint is updated overnight to reflect the latest available symbols.

## Endpoint Details:
*   **Path**: `/index/list/symbols`
*   **Method**: `GET`
*   **Summary**: Symbols
*   **Operation ID**: `index_list_symbols`
*   **Minimum Subscription**: `free`
*   **Description**:
    *   A symbol can be defined as a unique identifier for a stock / underlying asset. Common terms also include: root, ticker, and underlying.
    *   This endpoint returns all traded symbols for indices.
    *   This endpoint is updated overnight.

## Parameters:
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns a list of all symbols for indices.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The symbol of the contract, or stock / underlying asset / option / index.

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.index_list_symbols()
```

## Related Concepts:
*   [Index Data](../concepts/index-data.md)
*   [Symbols](../concepts/symbols.md)
*   [Index List Dates Endpoint](../concepts/index-list-dates-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---