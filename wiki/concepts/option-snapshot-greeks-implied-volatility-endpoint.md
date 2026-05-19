---
tags: ["Option", "Snapshot", "Greeks", "Implied Volatility", "Real-time Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Greeks Implied Volatility Endpoint

The `/option/snapshot/greeks/implied_volatility` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides real-time snapshot implied volatilities for options contracts. These are calculated using the national best bid, mid, and ask prices of the option.

## Endpoint Details:
*   **Path**: `/option/snapshot/greeks/implied_volatility`
*   **Method**: `GET`
*   **Summary**: Implied Volatility
*   **Operation ID**: `option_snapshot_greeks_implied_volatility`
*   **Minimum Subscription**: `standard`
*   **Description**:
    *   Returns implied volatilities calculated using the national best bid, mid, and ask price of the option respectively.
    *   The underlying price represents whatever the last underlying price was at the `underlying_timestamp` field.
    *   More about how Theta Data calculates Greeks can be found [here](/Articles/Data-And-Requests/Option-Greeks.html).

## Parameters:
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. Use `*` for all expirations. See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `annual_dividend` (Optional): The annualized expected dividend amount. See [API Parameters](../../concepts/api-parameters.md#annual-dividend).
*   `rate_type` (Optional): The interest rate type. See [API Parameters](../../concepts/api-parameters.md#rate-type).
*   `rate_value` (Optional): The interest rate value. See [API Parameters](../../concepts/api-parameters.md#rate-value).
*   `stock_price` (Optional): The underlying stock price. See [API Parameters](../../concepts/api-parameters.md#stock-price).
*   `greeks_version` (Optional): Greeks calculation methodology version. See [API Parameters](../../concepts/api-parameters.md#greeks-version).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `min_time` (Optional): Filters snapshots to include only data with a timestamp greater or equal to the specified value. See [API Parameters](../../concepts/api-parameters.md#min-time).
*   `use_market_value` (Optional): Use the market value bid, ask, and price. See [API Parameters](../../concepts/api-parameters.md#use-market-value).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns implied volatility for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `bid`: The last NBBO bid price.
        *   `ask`: The last NBBO ask price.
        *   `implied_vol`: The implied volatility calculated using the trade price.
        *   `iv_error`: IV Error: the value of the option calculated using the implied volatility divided by the actual value reported in the quote.
        *   `underlying_timestamp`: The underlying date formatted as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price`: The midpoint of the underlying at the time of the option trade.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_snapshot_greeks_implied_volatility(symbol='AAPL', expiration=date(2027, 1, 15))
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Greeks](../concepts/option-greeks.md)
*   [Implied Volatility](../concepts/implied-volatility.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---