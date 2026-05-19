---
tags: ["Option", "History", "Quote", "NBBO", "Time Series"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Quote Endpoint

The `/option/history/quote` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical National Best Bid and Offer (NBBO) quotes for specified options contracts over a given date range and at a defined [Time Interval](../../concepts/time-intervals.md).

## Endpoint Details:
*   **Path**: `/option/history/quote`
*   **Method**: `GET`
*   **Summary**: Quote
*   **Operation ID**: `option_history_quote`
*   **Minimum Subscription**: `value`
*   **History Access**: `true`
*   **Description**:
    *   Returns every NBBO quote reported by [OPRA (Options Price Reporting Authority)](../../entities/opra.md).
    *   If the `interval` [API Parameter](../../concepts/api-parameters.md#interval) is specified, the quote for each interval represents the last quote at the interval's timestamp.
    *   Multi-day requests are limited to 1 month of data, and must specify an expiration.

## Parameters:
*   `opt_date` (Optional): The date to fetch data for. If present, this overrides `start_date` and `end_date`. See [API Parameters](../../concepts/api-parameters.md#opt-date).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `start_time` (Optional): The start time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#start-time).
*   `end_time` (Optional): The end time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#end-time).
*   `interval` (Required): The size of the time interval. See [API Parameters](../../concepts/api-parameters.md#interval) and [Time Intervals](../../concepts/time-intervals.md).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).
*   `opt_start_date` (Optional): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-start-date).
*   `opt_end_date` (Optional): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-end-date).

## Responses:
*   **200 OK**: Returns every quote for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `bid_size`: The last NBBO bid size.
        *   `bid_exchange`: The last NBBO bid [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html).
        *   `bid`: The last NBBO bid price.
        *   `bid_condition`: The last NBBO bid [condition](/Articles/Errors-Exchanges-Conditions/Quote-Conditions.html).
        *   `ask_size`: The last NBBO ask size.
        *   `ask_exchange`: The last NBBO ask [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html).
        *   `ask`: The last NBBO ask price.
        *   `ask_condition`: The last NBBO ask [condition](/Articles/Errors-Exchanges-Conditions/Quote-Conditions.html).

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_history_quote(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='1m',
)
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Snapshot Quote Endpoint](../concepts/option-snapshot-quote-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)
*   [Quote Conditions](../concepts/quote-conditions.md)

---