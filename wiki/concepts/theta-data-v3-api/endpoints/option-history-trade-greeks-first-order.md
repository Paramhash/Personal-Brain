---
tags: ["option", "history", "trade-greeks", "first-order-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History First Order Trade Greeks

## Summary
First Order Trade Greeks

## Operation ID
`option_history_trade_greeks_first_order`

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
**Description:** Returns first order trade greeks for an option contract

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
        *   `delta` (number): The delta.
        *   `theta` (string): The Theta.
        *   `vega` (number): The vega.
        *   `rho` (number): The rho.
        *   `epsilon` (string): The epsilon.
        *   `lambda` (number): The lambda.
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
        {"underlying_price":221.33,"delta":0.0025,"implied_vol":0.5749,"theta":-0.0134,"iv_error":0.0132,"epsilon":-0.0062,"sequence":156249981,"condition":125,"lambda":56.6408,"size":1,"price":0.01,"ext_condition2":255,"rho":0.0061,"ext_condition1":255,"ext_condition4":255,"exchange":9,"ext_condition3":255,"underlying_timestamp":"2024-11-04T09:53:54","vega":0.1858,"timestamp":"2024-11-04T09:53:54.069"}
      ]
    },
    {
      "contract": {"symbol":"AAPL","strike":140.000,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"underlying_price":221.22,"delta":0.9976,"implied_vol":1.5937,"theta":-0.0520,"iv_error":0.0000,"epsilon":-2.4186,"sequence":546105677,"condition":131,"lambda":2.7139,"size":2,"price":81.32,"ext_condition2":255,"rho":1.5274,"ext_condition1":255,"ext_condition4":255,"exchange":5,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:47:14","vega":0.1690,"timestamp":"2024-11-04T11:47:14.764"},
        {"underlying_price":221.18,"delta":1.0000,"implied_vol":0.0000,"theta":0.0000,"iv_error":0.0011,"epsilon":0.0000,"sequence":548097371,"condition":130,"lambda":0.0000,"size":3,"price":81.16,"ext_condition2":255,"rho":0.0000,"ext_condition1":255,"ext_condition4":255,"exchange":7,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:47:56","vega":0.0000,"timestamp":"2024-11-04T11:47:56.669"},
        {"underlying_price":221.16,"delta":0.9976,"implied_vol":1.5937,"theta":-0.0522,"iv_error":0.0000,"epsilon":-2.4179,"sequence":548397162,"condition":130,"lambda":2.7152,"size":3,"price":81.26,"ext_condition2":255,"rho":1.5274,"ext_condition1":255,"ext_condition4":255,"exchange":6,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:48:03","vega":0.1697,"timestamp":"2024-11-04T11:48:03.852"},
        {"underlying_price":221.19,"delta":0.9993,"implied_vol":1.3968,"theta":-0.0279,"iv_error":0.0000,"epsilon":-2.4223,"sequence":550463381,"condition":131,"lambda":2.7198,"size":1,"price":81.27,"ext_condition2":255,"rho":1.5317,"ext_condition1":255,"ext_condition4":255,"exchange":5,"ext_condition3":255,"underlying_timestamp":"2024-11-04T11:48:51","vega":0.0544,"timestamp":"2024-11-04T11:48:51.11"}
      ]
    }               
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_history_trade_greeks_first_order(symbol='AAPL', expiration=date(2024, 11, 8))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_trade_greeks_first_order(symbol='AAPL', expiration=date(2024, 11, 8))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]