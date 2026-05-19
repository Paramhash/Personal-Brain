---
tags: ["Option", "List", "Strikes", "Availability"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Strikes Endpoint

The `/option/list/strikes` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve a list of all available [Strike Prices](../concepts/strike-prices.md) for options contracts associated with a given underlying symbol and expiration date. This endpoint is updated overnight.

## Endpoint Details:
*   **Path**: `/option/list/strikes`
*   **Method**: `GET`
*   **Summary**: Strikes
*   **Operation ID**: `option_list_strikes`
*   **Minimum Subscription**: `free`
*   **Description**:
    *   Lists all strikes that are available for an option with a given symbol and expiration date.
    *   This endpoint is updated overnight.

## Parameters:
*   `symbol` (Required): The underlying stock symbol. Specify `*` for all symbols or a comma-separated list. See [API Parameters](../../concepts/api-parameters.md#multi-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration_no_star` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration-no-star) and [Expirations](../../concepts/expirations.md).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns a list of all strikes for an option with a given symbol and expiration date.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `strike`: Strike price of the contract in dollars (e.g., `180.000`).

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_strikes(symbol=['AAPL'], expiration=date(2022, 9, 30))
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Strike Prices](../concepts/strike-prices.md)
*   [Expirations](../concepts/expirations.md)
*   [Option List Symbols Endpoint](../concepts/option-list-symbols-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---