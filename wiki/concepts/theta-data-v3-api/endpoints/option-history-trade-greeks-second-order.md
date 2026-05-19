---
tags: ["option", "history", "trade-greeks", "second-order-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Second Order Trade Greeks

## Summary
Second Order Trade Greeks

## Operation ID
`option_history_trade_greeks_second_order`

## Description
- Returns the data for all contracts that share the same provided symbol and expiration.
- Calculates greeks for every trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html).
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

## Minimum Subscription
`professional`

## History Access
`true`

## Parameters
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/start-time.md|start_time]] (Optional)
*   [[../parameters/end-time.md|end_time]] (Optional)
*   [[../parameters/annual-dividend.md|annual_dividend]] (Optional)
*   [[../parameters/rate-type.md|rate_type]] (Optional)
*   [[../parameters/rate-value.md|rate_value]] (Optional)
*   [[../parameters/greeks-version.md|version]] (Optional)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns second order trade greeks for an option contract

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
        *   `expiration` (string, format: `date`): Expiration date of the contract in YYYY-MM-DD format.
        *   `strike` (number): Strike price of the contract in dollars 180.00
        *   `right` (string): Indicates whether the contract is a call or put option.
        *   `timestamp` (string, format: `date-time`): The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `sequence` (integer): The exchange [sequence](/Articles/Data-And-Requests/Making-Requests.html#trade-sequences).
        *   `ext_condition1` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `ext_condition2` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `ext_condition3` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `ext_condition4` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `condition` (integer): The trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
        *   `size` (integer): The amount of contracts / shares traded.
        *   `exchange` (integer): The [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html) the trade was executed.
        *   `price` (number): The trade price.
        *   `gamma` (number): The gamma.
        *   `vanna` (number): The vanna.
        *   `charm` (string): The charm.
        *   `vomma` (number): The vomma.
        *   `veta` (number): The veta.
        *   `implied_vol` (number): The implied volatiltiy calculated using the trade price.
        *   `iv_error` (number): IV Error: the value of the option calculated using the implied volatiltiy divided by the actual value reported in the quote. This value will increase as the strike price recedes from the underlying price.
        *   `underlying_timestamp` (string, format: `date-time`): The underlying date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price` (number): The midpoint of the underlying at the time of the option trade.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":262.500,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"underlying_price":221.33,"veta":0.0137,"implied_vol":0.5749,"iv_error":0.0132,"sequence":156249981,"condition":125,"size":1,"charm":-1.0514,"price":0.01,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":9,"vanna":0.0398,"vomma":2.5798,"ext_condition3":255,"underlying_timestamp":"2024-11-04T09:53:54","gamma":0.0006,"timestamp":"2024-11-04T09:53:54.069"}
      ]
    },
    {
      "contract": {"symbol":"AAPL","strike":140.000,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"underlying_price":221.22,"veta":0.0063,"implied_vol":1.5937,"iv_error":0.0000,"sequence":546105677,"condition":131,"size":2,"charm":0.8843,"price":81.32,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":5,"vanna":-0.0121,"vomma":0.7986,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:47:14","gamma":0.0001,"timestamp":"2024-11-04T11:47:14.764"},
        {"underlying_price":221.18,"veta":0.0000,"implied_vol":0.0000,"iv_error":0.0011,"sequence":548097371,"condition":130,"size":3,"charm":0.0000,"price":81.16,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":7,"vanna":0.0000,"vomma":0.0000,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:47:56","gamma":0.0000,"timestamp":"2024-11-04T11:47:56.669"},
        {"underlying_price":221.16,"veta":0.0064,"implied_vol":1.5937,"iv_error":0.0000,"sequence":548397162,"condition":130,"lambda":2.7152,"size":3,"price":81.26,"ext_condition2":255,"rho":1.5274,"ext_condition1":255,"ext_condition4":255,"exchange":6,"vanna":-0.0122,"vomma":0.8011,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:48:03","gamma":0.0001,"timestamp":"2024-11-04T11:48:03.852"},
        {"underlying_price":221.19,"veta":0.0025,"implied_vol":1.3968,"iv_error":0.0000,"sequence":550463381,"condition":131,"size":1,"charm":0.3271,"price":81.27,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":5,"vanna":-0.0051,"vomma":0.3817,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:48:51","gamma":0.0000,"timestamp":"2024-11-04T11:48:51.11"}
      ]
    }
  ]
}
```

## Code Samples

### Python