---
tags: ["option", "history", "quote", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Quote

## Summary
Quote

## Operation ID
`option_history_quote`

## Description
- Returns every NBBO quote reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html). 
- If the ``interval`` parameter is specified, the quote for each interval represents the last quote at the interval's timestamp.
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

## Minimum Subscription
`value`

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
*   [[../parameters/interval.md|interval]] (Required)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns every quote for an option contract

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
        *   `bid_size` (integer): The last NBBO bid size.
        *   `bid_exchange` (integer): The last NBBO bid [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html).
        *   `bid` (number): The last NBBO bid price.
        *   `bid_condition` (integer): The last NBBO bid [condition](/Articles/Errors-Exchanges-Conditions/Quote-Conditions.html).
        *   `ask_size` (integer): The last NBBO ask size.
        *   `ask_exchange` (integer): The last NBBO ask [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html).
        *   `ask` (number): The last NBBO ask price.
        *   `ask_condition` (integer): The last NBBO ask [condition](/Articles/Errors-Exchanges-Conditions/Quote-Conditions.html).

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":220.000,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"ask_size":0,"ask_condition":50,"bid_size":0,"ask_exchange":42,"bid_exchange":42,"ask":0.00,"bid":0.00,"bid_condition":50,"timestamp":"2024-11-04T09:30:00"},
        {"ask_size":424,"ask_condition":50,"bid_size":598,"ask_exchange":9,"bid_exchange":5,"ask":4.70,"bid":4.55,"bid_condition":50,"timestamp":"2024-11-04T09:31:00"},
        {"ask_size":221,"ask_condition":50,"bid_size":58,"ask_exchange":11,"bid_exchange":46,"ask":4.40,"bid":4.30,"bid_condition":50,"timestamp":"2024-11-04T09:32:00"},
        {"ask_size":45,"ask_condition":50,"bid_size":394,"ask_exchange":47,"bid_exchange":43,"ask":4.00,"bid":3.90,"bid_condition":50,"timestamp":"2024-11-04T09:33:00"},
        {"ask_size":121,"ask_condition":50,"bid_size":194,"ask_exchange":11,"bid_exchange":11,"ask":4.30,"bid":4.15,"bid_condition":50,"timestamp":"2024-11-04T09:34:00"}
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
df = client.option_history_quote(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='1m',
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_quote(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='1m',
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]