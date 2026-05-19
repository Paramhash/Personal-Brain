---
tags: ["Option", "History", "Trade Quote", "NBBO"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Trade Quote Endpoint

The `/option/history/trade_quote` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical trade data paired with the corresponding National Best Bid and Offer (NBBO) quote at the time of the trade, for specified options contracts over a given date range.

## Endpoint Details:
*   **Path**: `/option/history/trade_quote`
*   **Method**: `GET`
*   **Summary**: Trade Quote
*   **Operation ID**: `option_history_trade_quote`
*   **Minimum Subscription**: `standard`
*   **History Access**: `true`
*   **Description**:
    *   Returns every [trade](/operations/option_history_trade.html) reported by [OPRA (Options Price Reporting Authority)](../../entities/opra.md) paired with the last NBBO quote reported by OPRA at the time of trade.
    *   A quote is matched with a trade if its timestamp `<= ` the trade timestamp.
    *   To match trades with quotes timestamps that are `<` the trade timestamp, specify the `exclusive` [API Parameter](../../concepts/api-parameters.md#exclusive) to `true`. After thorough testing, using `exclusive=true` might yield better results for various applications.
    *   Multi-day requests are limited to 1 month of data, and must specify an expiration.

## Parameters:
*   `opt_date` (Optional): The date to fetch data for. If present, this overrides `start_date` and `end_date`. See [API Parameters](../../concepts/api-parameters.md#opt-date).
*   `symbol` (Required): The underlying stock symbol. See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `expiration` (Required): The expiration date of the contract. See [API Parameters](../../concepts/api-parameters.md#expiration) and [Expirations](../../concepts/expirations.md).
*   `strike` (Optional): The strike price of the contract. See [API Parameters](../../concepts/api-parameters.md#strike) and [Strike Prices](../../concepts/strike-prices.md).
*   `right` (Optional): The right (call or put) of the contract. See [API Parameters](../../concepts/api-parameters.md#right).
*   `start_time` (Optional): The start time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#start-time).
*   `end_time` (Optional): The end time (inclusive) in the specified day. See [API Parameters](../../concepts/api-parameters.md#end-time).
*   `exclusive` (Optional): If `true`, matches quotes with timestamps `<` the trade timestamp. See [API Parameters](../../concepts/api-parameters.md#exclusive).
*   `max_dte` (Optional): Filters contracts by Days to Expiration. See [API Parameters](../../concepts/api-parameters.md#max-dte).
*   `strike_range` (Optional): Limits the number of contracts returned relative to the underlying's spot price. See [API Parameters](../../concepts/api-parameters.md#strike-range).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).
*   `opt_start_date` (Optional): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-start-date).
*   `opt_end_date` (Optional): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#opt-end-date).

## Responses:
*   **200 OK**: Returns every trade quote for an option contract.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `symbol`: The underlying symbol.
        *   `expiration`: Expiration date in YYYY-MM-DD format.
        *   `strike`: Strike price.
        *   `right`: Call or Put.
        *   `trade_timestamp`: The trade date formatted as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `quote_timestamp`: The quote date formatted as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `sequence`: The exchange [sequence](/Articles/Data-And-Requests/Making-Requests.html#trade-sequences).
        *   `ext_condition1` to `ext_condition4`: Additional trade [conditions](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `condition`: The trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
        *   `size`: The amount of contracts / shares traded.
        *   `exchange`: The [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html) the trade was executed.
        *   `price`: The trade price.
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
df = client.option_history_trade_quote(symbol='AAPL', expiration=date(2024, 11, 8))
```

## Related Concepts:
*   [Option Data](../concepts/option-data.md)
*   [Option History Trade Endpoint](../concepts/option-history-trade-endpoint.md)
*   [Option History Quote Endpoint](../concepts/option-history-quote-endpoint.md)
*   [API Endpoints](../concepts/api-endpoints.md)
*   [Trade Conditions](../concepts/trade-conditions.md)
*   [Quote Conditions](../concepts/quote-conditions.md)

---