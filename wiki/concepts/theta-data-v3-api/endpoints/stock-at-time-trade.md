---
tags: ["stock", "at-time", "trade", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock At-Time Trade

## Summary
Trade

## Operation ID
`stock_at_time_trade`

## Description
#### Real-time request:
- Returns a real-time session from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs.html#nasdaq-basic) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Returns a 15-minute delayed session from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.

#### Historical request:
Returns the last trade reported by [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) at a specified millisecond of the day.
Trade condition mappings can be found [here](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).

## Minimum Subscription
`standard`

## History Access
`true`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/start-date.md|start_date]] (Required)
*   [[../parameters/end-date.md|end_date]] (Required)
*   [[../parameters/time-of-day.md|time_of_day]] (Required)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns the last trade for a given symbol and specified time of day

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
      {"sequence":405549,"condition":115,"size":1,"price":475.280,"ext_condition2":255,"ext_condition1":255,"ext_condition4":115,"exchange":57,"ext_condition3":255,"timestamp":"2024-01-16T09:30:00.088"}                  
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.stock_at_time_trade(
    symbol='SPY',
    start_date=date(2024, 1, 16),
    end_date=date(2024, 1, 16),
    time_of_day='09:30:00.100',
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.stock_at_time_trade(
    symbol='SPY',
    start_date=date(2024, 1, 16),
    end_date=date(2024, 1, 16),
    time_of_day='09:30:00.100',
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]