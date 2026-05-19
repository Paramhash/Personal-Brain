---
tags: ["Option", "History", "Trade", "Time Series"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Trade Endpoint

The `/option/history/trade` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical trade data for specified options contracts over a given date range. It returns every trade reported by [OPRA (Options Price Reporting Authority)](../../entities/opra.md).

## Endpoint Details:
*   **Path**: `/option/history/trade`
*   **Method**: `GET`
*   **Summary**: Trade
*   **Operation ID**: `option_history_trade`
*   **Minimum Subscription**: `standard`
*   **History Access**: `true`
*   **Description**:
    *   Returns every trade reported by [OPRA (Options Price Reporting Authority)](../../entities/opra.md).
    *   [Trade Condition Mappings](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html) can be found in the documentation.
    *   Extended trade conditions are not reported by OPRA for options, so they can be ignored.
    *   Multi-day requests are limited to 1 month of data, and must specify an expiration.

## Parameters:
*   `opt_date` (Optional): The date to fetch data for. If present, this overrides `start_date` and `end_date`. See [API Parameters](../../concepts/api-parameters.md#opt-date).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `start_time` (Optional): The start time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#start-time).
*   `end_time` (Optional): The end time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#end-time).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).
*   `opt_start_date` (Optional): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-start-date).
*   `opt_end_date` (Optional): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-end-date).

## Responses:
*   **200 OK**: Returns every trade for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `sequence`: The exchange [sequence](/Articles/Data-And-Requests/Making-Requests.html#trade-sequences).
        *   `ext_condition1` to `ext_condition4`: Additional trade [conditions](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `condition`: The trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
        *   `size`: The amount of contracts / shares traded.
        *   `exchange`: The [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html) the trade was executed.
        *   `price`: The trade price.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_history_trade(symbol='AAPL', expiration=date(2024, 11, 8))
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Snapshot Trade Endpoint](../concepts/option-snapshot-trade-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)
*   [Trade Conditions](../concepts/trade-conditions.md)

---