---
tags: ["Option", "List", "Contracts", "Availability"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Contracts Endpoint

The `/option/list/contracts/{request_type}` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve a list of all options contracts that were traded or quoted on a particular date. This endpoint is updated in real-time.

## Endpoint Details:
*   **Path**: `/option/list/contracts/{request_type}`
*   **Method**: `GET`
*   **Summary**: Contracts
*   **Operation ID**: `option_list_contracts`
*   **Minimum Subscription**: `value`
*   **History Access**: `true`
*   **Description**:
    *   Lists all contracts that were traded or quoted on a particular date.
    *   If the `symbol` [API Parameter](../../concepts/api-parameters.md#opt-multi-symbol) is specified, the returned contracts will be filtered to match the symbol. Multiple symbols can be specified by separating them with commas (e.g., `symbol=AAPL,SPY,AMD`).
    *   This endpoint is updated real-time.

## Parameters:
*   `request_type` (Required): The request type (`trade` or `quote`). See [API Parameters](../../concepts/api-parameters.md#request-type).
*   `opt_multi_symbol` (Optional): The underlying stock symbol(s). See [API Parameters](../../concepts/api-parameters.md#opt-multi-symbol) and [Symbols](../../concepts/symbols.md).
*   `date` (Required): The date to fetch data for. See [API Parameters](../../concepts/api-parameters.md#date).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns a list of all contracts for an option trade with a given date.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_contracts(request_type='trade', date=date(2022, 9, 30))
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option List Symbols Endpoint](../concepts/option-list-symbols-endpoint.md)
*   [Option List Expirations Endpoint](../concepts/option-list-expirations-endpoint.md)
*   [Option List Strikes Endpoint](../concepts/option-list-strikes-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---