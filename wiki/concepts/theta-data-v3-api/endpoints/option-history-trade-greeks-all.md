---
tags: ["option", "history", "trade-greeks", "all-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History All Trade Greeks

## Summary
All Trade Greeks

## Operation ID
`option_history_trade_greeks_all`

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
**Description:** Returns all trade greeks for an option contract

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
        *   `sequence` (string): The exchange [sequence](/Articles/Data-And-Requests/Making-Requests.html#trade-sequences).
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
        *   `gamma` (number): The gamma.
        *   `vanna` (number): The vanna.
        *   `charm` (string): The charm.
        *   `vomma` (number): The vomma.
        *   `veta` (number): The veta.
        *   `vera` (number): The vera.
        *   `speed` (number): The speed.
        *   `zomma` (number): The zomma.
        *   `color` (string): The color.
        *   `ultima` (string): The ultima.
        *   `d1` (string): The d1.
        *   `d2` (string): The d2.
        *   `dual_delta` (string): The dual delta.
        *   `dual_gamma` (number): The dual gamma.
        *   `implied_vol` (number): The implied volatiltiy calculated using the trade price.
        *   `iv_error` (string): IV Error: the value of the option calculated using the implied volatiltiy divided by the actual value reported in the quote. This value will increase as the strike price recedes from the underlying price.
        *   `underlying_timestamp` (string, format: `date-time`): The underlying date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price` (number): The midpoint of the underlying at the time of the option trade.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":187.500,"right":"CALL","expiration":"2023-11-17"},
      "data": [
        {"dual_delta":-0.2213,"color":-0.0129,"zomma":0.0000,"delta":0.2289,"implied_vol":0.1762,"theta":-0.1031,"d1":-0.7424,"speed":0.0000,"d2":-0.7668,"epsilon":-0.8073,"lambda":71.4109,"price":0.59,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"vomma":24.9086,"ext_condition3":255,"underlying_timestamp":"2023-11-10T09:30:00","timestamp":"2023-11-10T09:30:00.004","underlying_price":183.89,"vera":0.0000,"veta":0.3553,"iv_error":-0.0008,"ultima":-100.0000,"sequence":-1391330475,"condition":18,"size":1,"charm":-6.7146,"rho":0.7960,"exchange":9,"vanna":1.3174,"dual_gamma":0.0000,"vega":7.7122,"gamma":0.0674},
        {"dual_delta":-0.2213,"color":-0.0129,"zomma":0.0000,"delta":0.2289,"implied_vol":0.1762,"theta":-0.1031,"d1":-0.7424,"speed":0.0000,"d2":-0.7668,"epsilon":-0.8073,"lambda":71.4109,"price":0.59,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"vomma":24.9086,"ext_condition3":255,"underlying_timestamp":"2023-11-10T09:30:00","timestamp":"2023-11-10T09:30:00.154","underlying_price":183.89,"vera":0.0000,"veta":0.3553,"iv_error":-0.0008,"ultima":-100.0000,"sequence":-1391317465,"condition":18,"size":1,"charm":-6.7146,"rho":0.7960,"exchange":47,"vanna":1.3174,"dual_gamma":0.0000,"vega":7.7122,"gamma":0.0674},
        {"dual_delta":-0.2093,"color":-0.0118,"zomma":0.0000,"delta":0.2162,"implied_vol":0.1669,"theta":-0.0947,"d1":-0.7849,"speed":0.0000,"d2":-0.8081,"epsilon":-0.7625,"lambda":76.6064,"price":0.52,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"vomma":28.3594,"ext_condition3":255,"underlying_timestamp":"2023-11-10T09:30:00","timestamp":"2023-11-10T09:30:00.22","underlying_price":183.89,"vera":0.0000,"veta":0.3755,"iv_error":-0.0018,"ultima":-100.0000,"sequence":-1391313694,"condition":18,"size":8,"charm":-6.8508,"rho":0.7526,"exchange":6,"vanna":1.4186,"dual_gamma":0.0000,"vega":7.4656,"gamma":0.0689},
        {"dual_delta":-0.2182,"color":-0.0126,"zomma":0.0000,"delta":0.2256,"implied_vol":0.1738,"theta":-0.1009,"d1":-0.7531,"speed":0.0000,"d2":-0.7772,"epsilon":-0.7958,"lambda":72.7109,"price":0.57,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"vomma":25.7650,"ext_condition3":255,"underlying_timestamp":"2023-11-10T09:30:00","timestamp":"2023-11-10T09:30:00.221","underlying_price":183.89,"vera":0.0000,"veta":0.3605,"iv_error":0.0012,"ultima":-100.0000,"sequence":-1391313652,"condition":130,"size":1,"charm":-6.7516,"rho":0.7849,"exchange":6,"vanna":1.3432,"dual_gamma":0.0000,"vega":7.6504,"gamma":0.0678},
        {"dual_delta":-0.2231,"color":-0.0130,"zomma":0.0000,"delta":0.2308,"implied_vol":0.1777,"theta":-0.1044,"d1":-0.7360,"speed":0.0000,"d2":-0.7607,"epsilon":-0.8140,"lambda":70.6522,"price":0.60,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"vomma":24.4114,"ext_condition3":255,"underlying_timestamp":"2023-11-10T09:30:00","timestamp":"2023-11-10T09:30:00.452","underlying_price":183.89,"vera":0.0000,"veta":0.3523,"iv_error":0.0013,"ultima":-100.0000,"sequence":-1391297309,"condition":18,"size":6,"charm":-6.6920,"rho":0.8025,"exchange":31,"vanna":1.3022,"dual_gamma":0.0000,"vega":7.7484,"gamma":0.0672}
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
df = client.option_history_trade_greeks_all(symbol='AAPL', expiration=date(2023, 11, 17))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_trade_greeks_all(symbol='AAPL', expiration=date(2023, 11, 17))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]