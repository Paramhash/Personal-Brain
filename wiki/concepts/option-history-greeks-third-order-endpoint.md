---
tags: ["Option", "History", "Greeks", "Third Order", "Time Series"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Greeks Third Order Endpoint

The `/option/history/greeks/third_order` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical calculations for third-order [Option Greeks](../concepts/option-greeks.md) (Speed, Zomma, Color, Ultima, Implied Volatility, IV Error) for options contracts. This data is returned for all contracts that share the same provided symbol and expiration, at specified [Time Intervals](../../concepts/time-intervals.md).

## Endpoint Details:
*   **Path**: `/option/history/greeks/third_order`
*   **Method**: `GET`
*   **Summary**: Third Order Greeks
*   **Operation ID**: `option_history_greeks_third_order`
*   **Minimum Subscription**: `professional`
*   **History Access**: `true`
*   **Description**:
    *   Returns the data for all contracts that share the same provided symbol and expiration.
    *   Calculated using the option and underlying midpoint price. If an interval size is specified (*highly recommended*), the option quote used in the calculation follows the same rules as the [Option History Quote Endpoint](../concepts/option-history-quote-endpoint.md).
    *   The underlying price represents whatever the last underlying price was at the `timestamp` field.
    *   More about how Theta Data calculates Greeks can be found [here](/Articles/Data-And-Requests/Option-Greeks.html).
    *   Multi-day requests are limited to 1 month of data.

## Parameters:
*   `opt_date` (Optional): The date to fetch data for. If present, this overrides `start_date` and `end_date`. See [API Parameters](../../concepts/api-parameters.md#opt-date).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration_no_star` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration-no-star) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `start_time` (Optional): The start time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#start-time).
*   `end_time` (Optional): The end time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#end-time).
*   `interval` (Required): The size of the time interval. See [API Parameters](../../concepts/api-parameters.md#interval) and [Time Intervals](../../concepts/time-intervals.md).
*   `annual_dividend` (Optional): The annualized expected dividend amount. See [API Parameters](../../concepts/api-parameters.md#annual-dividend).
*   `rate_type` (Optional): The interest rate type. See [API Parameters](../../concepts/api-parameters.md#rate-type).
*   `rate_value` (Optional): The interest rate value. See [API Parameters](../../concepts/api-parameters.md#rate-value).
*   `greeks_version` (Optional): Greeks calculation methodology version. See [API Parameters](../../concepts/api-parameters.md#greeks-version).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).
*   `opt_start_date` (Optional): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-start-date).
*   `opt_end_date` (Optional): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-end-date).

## Responses:
*   **200 OK**: Returns third order Greeks for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `bid`: The last NBBO bid price.
        *   `ask`: The last NBBO ask price.
        *   `speed`, `zomma`, `color`, `ultima`, `implied_vol`, `iv_error`: Third-order [Option Greeks](../concepts/option-greeks.md) and related metrics.
        *   `underlying_timestamp`: The underlying date formatted as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price`: The midpoint of the underlying at the time of the option trade.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_history_greeks_third_order(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='1h',
)
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Greeks](../concepts/option-greeks.md)
*   [Option History Greeks All Endpoint](../concepts/option-history-greeks-all-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---