---
tags: ["stock", "history", "trade", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock History Trade

## Summary
Trade

## Operation ID
`stock_history_trade`

## Description
Returns every trade reported by [UTP & CTA](/Articles/Data-And-Requests/The-SIPs). Set the ``venue`` parameter to ``nqb`` to access current-day real-time historic data from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Multi-day requests are limited to 1 month of data.

## Minimum Subscription
`standard`

## History Access
`true`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/start-time.md|start_time]] (Optional)
*   [[../parameters/end-time.md|end_time]] (Optional)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns every trade for a given symbol between specified dates (inclusive) with a one minute interval

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
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
    {"sequence":14920,"condition":1,"size":2,"price":187.1800,"ext_condition2":95,"ext_condition1":32,"ext_condition4":115,"exchange":7,"ext_condition3":1,"timestamp":"2024-01-02T09:30:00.011"},
    {"sequence":8931,"condition":1,"size":1,"price":187.1800,"ext_condition2":255,"ext_condition1":32,"ext_condition4":115,"exchange":1,"ext_condition3":1,"timestamp":"2024-01-02T09:30:00.014"},
    {"sequence":8932,"condition":1,"size":5,"price":187.1800,"ext_condition2":255,"ext_condition1":32,"ext_condition4":115,"exchange":1,"ext_condition3":1,"timestamp":"2024-01-02T09:30:00.014"},
    {"sequence":8933,"condition":1,"size":3,"price":187.1900,"ext_condition2":255,"ext_condition1":32,"ext_condition4":115,"exchange":1,"ext_condition3":1,"timestamp":"2024-01-02T09:30:00.014"},
    {"sequence":8934,"condition":1,"size":91,"price":187.1900,"ext_condition2":255,"ext_condition1":32,"ext_condition4":115,"exchange":1,"ext_condition3":1,"timestamp":"2024-01-02T09:30:00.014"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_history_trade(symbol='AAPL')
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_history_trade(symbol='AAPL')
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]