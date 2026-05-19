---
tags: ["Option", "History", "End of Day"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History EOD Endpoint

The `/option/history/eod` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical End-of-Day (EOD) reports for specific options contracts over a given date range.

## Endpoint Details:
*   **Path**: `/option/history/eod`
*   **Method**: `GET`
*   **Summary**: End of Day
*   **Operation ID**: `option_history_eod`
*   **Minimum Subscription**: `free`
*   **History Access**: `true`
*   **Description**:
    *   Since [OPRA (Options Price Reporting Authority)](../../entities/opra.md) does not provide a national EOD report for options, Theta Data generates a national EOD report at 17:15 ET each day.
    *   `created` represents the datetime the report was generated and `last_trade` represents the datetime of the last trade.
    *   The quote in the response represents the last NBBO reported by OPRA at the time of report generation.
    *   More information about EOD & OHLC data can be found [here](/Articles/Data-And-Requests/OHLC-EOD.html).

## Parameters:
*   `start_date` (Required): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#start-date).
*   `end_date` (Required): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#end-date).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. Use `*` for all expirations (note: `expiration=*` must be requested day by day). See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
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
        *   `created`: The datetime the report was generated.
        *   `last_trade`: The last trade date.
        *   `open`: The opening trade price.
        *   `high`: The highest traded price.
        *   `low`: The lowest traded price.
        *   `close`: The closing traded price.
        *   `volume`: The amount of contracts / shares traded.
        *   `count`: The amount of trades.
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
df = client.option_history_eod(
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
    symbol='AAPL',
    expiration=date(2024, 11, 15),
)
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option History OHLC Endpoint](../concepts/option-history-ohlc-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)
*   [Trade Conditions](../concepts/trade-conditions.md)
*   [Quote Conditions](../concepts/quote-conditions.md)

---