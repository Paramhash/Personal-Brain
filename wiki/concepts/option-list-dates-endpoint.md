---
tags: ["Option", "List", "Dates", "Availability"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Dates Endpoint

The `/option/list/dates/{request_type}` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve a list of all dates for which data is available for an options contract, given a specific underlying symbol, request type (trade or quote), and expiration. This endpoint is updated overnight.

## Endpoint Details:
*   **Path**: `/option/list/dates/{request_type}`
*   **Method**: `GET`
*   **Summary**: Dates
*   **Operation ID**: `option_list_dates`
*   **Minimum Subscription**: `free`
*   **Description**:
    *   Lists all dates of data that are available for an option with a given symbol, request type, and expiration.
    *   This endpoint is updated overnight.

## Parameters:
*   `request_type` (Required): The request type (`trade` or `quote`). See [API Parameters](../../concepts/api-parameters.md#request-type).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration_no_star` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration-no-star) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns a list of all dates for an option quote for a given symbol and expiration date.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `date`: The date formatted as YYYY-MM-DD.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_dates(
    request_type='quote',
    symbol='AAPL',
    expiration=date(2022, 9, 30),
)
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option List Symbols Endpoint](../concepts/option-list-symbols-endpoint.md)
*   [Option List Expirations Endpoint](../concepts/option-list-expirations-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---