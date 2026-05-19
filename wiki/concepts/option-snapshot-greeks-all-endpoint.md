---
tags: ["Option", "Snapshot", "Greeks", "All Greeks", "Real-time Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Greeks All Endpoint

The `/option/snapshot/greeks/all` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides real-time snapshot calculations for all [Option Greeks](../concepts/option-greeks.md) for options contracts. This data is returned for all contracts that lie on a provided expiration.

## Endpoint Details:
*   **Path**: `/option/snapshot/greeks/all`
*   **Method**: `GET`
*   **Summary**: All Greeks
*   **Operation ID**: `option_snapshot_greeks_all`
*   **Minimum Subscription**: `professional`
*   **Description**:
    *   Retrieves a real-time last Greeks calculation for all option contracts that lie on a provided expiration.
    *   You might need to change the default expiration date to a different date if it is past the current date. Some quotes are omitted in the example to reduce the space of the sample output.
    *   Make `expiration` `*` if you want to get the snapshot for every expiration chain for the underlying.
    *   This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

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
*   **200 OK**: Returns all Greeks for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `bid`: The last NBBO bid price.
        *   `ask`: The last NBBO ask price.
        *   `delta`, `theta`, `vega`, `rho`, `epsilon`, `lambda`, `gamma`, `vanna`, `charm`, `vomma`, `veta`, `vera`, `speed`, `zomma`, `color`, `ultima`, `d1`, `d2`, `dual_delta`, `dual_gamma`, `implied_vol`, `iv_error`: Various [Option Greeks](../concepts/option-greeks.md) and related metrics.
        *   `underlying_timestamp`: The underlying date formatted as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price`: The midpoint of the underlying at the time of the option trade.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_snapshot_greeks_all(symbol='AAPL', expiration=date(2026, 5, 15))
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Greeks](../concepts/option-greeks.md)
*   [Option Snapshot Greeks First Order Endpoint](../concepts/option-snapshot-greeks-first-order-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---