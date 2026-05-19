---
tags: ["Option", "List", "Expirations", "Availability"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Expirations Endpoint

The `/option/list/expirations` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve a list of all available [Expirations](../concepts/expirations.md) for options contracts associated with a given underlying symbol. This endpoint is updated overnight.

## Endpoint Details:
*   **Path**: `/option/list/expirations`
*   **Method**: `GET`
*   **Summary**: Expirations
*   **Operation ID**: `option_list_expirations`
*   **Minimum Subscription**: `free`
*   **Description**:
    *   Lists all dates of expirations that are available for an option with a given symbol.
    *   This endpoint is updated overnight.

## Parameters:
*   `symbol` (Required): The underlying stock symbol. Specify `*` for all symbols or a comma-separated list. See [API Parameters](../../concepts/api-parameters.md#multi-symbol) and [Symbols](../../concepts/symbols.md).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns a list of all expirations for an option with a given symbol.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date of the contract in YYYY-MM-DD format.

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_expirations(symbol=['AAPL'])
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Expirations](../concepts/expirations.md)
*   [Option List Symbols Endpoint](../concepts/option-list-symbols-endpoint.md)
*   [Option List Dates Endpoint](../concepts/option-list-dates-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---