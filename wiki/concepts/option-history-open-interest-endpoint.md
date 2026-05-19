---
tags: ["Option", "History", "Open Interest"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Open Interest Endpoint

The `/option/history/open_interest` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical open interest data for specific options contracts over a given date range.

## Endpoint Details:
*   **Path**: `/option/history/open_interest`
*   **Method**: `GET`
*   **Summary**: Open Interest
*   **Operation ID**: `option_history_open_interest`
*   **Minimum Subscription**: `value`
*   **History Access**: `true`
*   **Description**:
    *   Open Interest is normally reported once per day by [OPRA (Options Price Reporting Authority)](../../entities/opra.md) at approximately 06:30 ET.
    *   A new open interest message might not be sent by OPRA if there is no open interest for the option contract.
    *   The reported open interest represents the open interest at the end of the previous trading day.

## Parameters:
*   `opt_date` (Optional): The date to fetch data for. If present, this overrides `start_date` and `end_date`. See [API Parameters](../../concepts/api-parameters.md#opt-date).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).
*   `opt_start_date` (Optional): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-start-date).
*   `opt_end_date` (Optional): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-end-date).

## Responses:
*   **200 OK**: Returns open interest for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `open_interest`: The total amount of outstanding contracts.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_history_open_interest(symbol='AAPL', expiration=date(2024, 11, 8))
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Snapshot Open Interest Endpoint](../concepts/option-snapshot-open-interest-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---