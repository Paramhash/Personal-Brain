---
tags: ["option", "history", "trade", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Trade

## Summary
Trade

## Operation ID
`option_history_trade`

## Description
- Returns every trade reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html). 
- Trade condition mappings can be found [here](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
- Extended trade conditions are not reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) for options, so they can be ignored.
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

## Minimum Subscription
`standard`

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
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns every trade for an option contract

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

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":220.000,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"sequence":18902138,"condition":130,"size":2,"price":3.90,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":22,"ext_condition3":255,"timestamp":"2024-11-04T09:30:00.471"},
        {"sequence":19368856,"condition":130,"size":1,"price":4.25,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":6,"ext_condition3":255,"timestamp":"2024-11-04T09:30:01.626"},
        {"sequence":19403970,"condition":130,"size":1,"price":4.22,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":6,"ext_condition3":255,"timestamp":"2024-11-04T09:30:01.698"},
        {"sequence":19598457,"condition":18,"size":1,"price":4.15,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":5,"ext_condition3":255,"timestamp":"2024-11-04T09:30:02.064"},
        {"sequence":19598464,"condition":18,"size":1,"price":4.15,"ext_condition2":255,"ext_condition1":255,"ext_condition4":255,"exchange":5,"ext_condition3":255,"timestamp":"2024-11-04T09:30:02.064"}
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
df = client.option_history_trade(symbol='AAPL', expiration=date(2024, 11, 8))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_trade(symbol='AAPL', expiration=date(2024, 11, 8))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]