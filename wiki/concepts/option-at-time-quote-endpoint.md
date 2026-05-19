---
tags: ["Option", "At-Time", "Quote", "Historical Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option At-Time Quote Endpoint

The `/option/at_time/quote` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API retrieves the last National Best Bid and Offer (NBBO) quote reported by [OPRA (Options Price Reporting Authority)](../../entities/opra.md) at a specified millisecond of the day, for a given options contract and date range.

## Endpoint Details:
*   **Path**: `/option/at_time/quote`
*   **Method**: `GET`
*   **Summary**: Quote
*   **Operation ID**: `option_at_time_quote`
*   **Minimum Subscription**: `value`
*   **History Access**: `true`
*   **Description**:
    *   Returns the last NBBO quote reported by [OPRA (Options Price Reporting Authority)](../../entities/opra.md) at a specified millisecond of the day.
    *   The `time_of_day` [API Parameter](../../concepts/api-parameters.md#time-of-day) represents the 00:00:00.000 ET that the quote should be provided for.

## Parameters:
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `start_date` (Required): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#start-date).
*   `end_date` (Required): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#end-date).
*   `time_of_day` (Required): The time of the day to fetch data for (HH:mm:ss.SSS format); assumed to be America/New_York. See [API Parameters](../../concepts/api-parameters.md#time-of-day).
*   `expiration` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns the last quote for an option contract.
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
df = client.option_at_time_quote(
    symbol='AAPL',
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
    time_of_day='09:30:01.000',
    expiration=date(2024, 11, 8),
)
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option History Quote Endpoint](../concepts/option-history-quote-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)
*   [Quote Conditions](../concepts/quote-conditions.md)

---