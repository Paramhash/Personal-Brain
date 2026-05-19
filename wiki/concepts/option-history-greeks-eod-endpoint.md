---
tags: ["Option", "History", "Greeks", "End of Day"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Greeks EOD Endpoint

The `/option/history/greeks/eod` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides End-of-Day (EOD) calculations for [Option Greeks](../concepts/option-greeks.md) for options contracts. This data is returned for all contracts that share the same provided symbol and expiration, using the closing option and underlying prices.

## Endpoint Details:
*   **Path**: `/option/history/greeks/eod`
*   **Method**: `GET`
*   **Summary**: End of Day Greeks
*   **Operation ID**: `option_history_greeks_eod`
*   **Minimum Subscription**: `standard`
*   **History Access**: `true`
*   **Description**:
    *   Returns the data for all contracts that share the same provided symbol and expiration.
    *   Uses Theta Data's EOD reports that get generated at 17:15 ET each day. The closing option price and closing underlying price are used for the Greeks calculation.
    *   Set `expiration` to `*` if you want to retrieve data for every option that shares the same `symbol`. (Note: Any `expiration=*` must be requested day by day).

## Parameters:
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. Use `*` for all expirations. See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `start_date` (Required): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#start-date).
*   `end_date` (Required): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#end-date).
*   `annual_dividend` (Optional): The annualized expected dividend amount. See [API Parameters](../../concepts/api-parameters.md#annual-dividend).
*   `rate_type` (Optional): The interest rate type. See [API Parameters](../../concepts/api-parameters.md#rate-type).
*   `rate_value` (Optional): The interest rate value. See [API Parameters](../../concepts/api-parameters.md#rate-value).
*   `greeks_version` (Optional): Greeks calculation methodology version. See [API Parameters](../../concepts/api-parameters.md#greeks-version).
*   `underlyer_use_nbbo` (Optional): Selects underlyer pricing for Greeks calculation. See [API Parameters](../../concepts/api-parameters.md#underlyer-use-nbbo).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns EOD report for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `timestamp`: The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `open`, `high`, `low`, `close`, `volume`, `count`: OHLC and trade volume/count.
        *   `bid_size`, `bid_exchange`, `bid`, `bid_condition`, `ask_size`, `ask_exchange`, `ask`, `ask_condition`: NBBO quote details.
        *   `delta`, `theta`, `vega`, `rho`, `epsilon`, `lambda`, `gamma`, `vanna`, `charm`, `vomma`, `veta`, `vera`, `speed`, `zomma`, `color`, `ultima`, `d1`, `d2`, `dual_delta`, `dual_gamma`, `implied_vol`, `iv_error`: Various [Option Greeks](../concepts/option-greeks.md) and related metrics.
        *   `underlying_timestamp`: The underlying date formatted as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price`: The midpoint of the underlying at the time of the option trade.

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_history_greeks_eod(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
)
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option Greeks](../concepts/option-greeks.md)
*   [Option History EOD Endpoint](../concepts/option-history-eod-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---