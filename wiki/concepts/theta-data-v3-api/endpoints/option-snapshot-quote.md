---
tags: ["option", "snapshot", "quote", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Quote

## Summary
Quote

## Operation ID
`option_snapshot_quote`

## Description
- Retrieve a real-time last NBBO quote of an option contract.
- You might need to change the default expiration date to a different date if it is past the current date.
- This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

## Minimum Subscription
`value`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/min-time.md|min_time]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns last NBBO quote for an option contract

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `timestamp` (string, format: `date-time`): The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
        *   `expiration` (string, format: `date`): Expiration date of the contract in YYYY-MM-DD format.
        *   `strike` (number): Strike price of the contract in dollars 180.00
        *   `right` (string): Indicates whether the contract is a call or put option.
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
      "contract": {"symbol":"AAPL","strike":275.000,"right":"CALL","expiration":"2026-01-16"},
      "data": [
        {"ask_size":25,"ask_condition":50,"bid_size":5,"ask_exchange":6,"bid_exchange":6,"ask":1.50,"bid":1.47,"bid_condition":50,"timestamp":"2025-08-20T15:59:59.805"}
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
df = client.option_snapshot_quote(symbol='AAPL', expiration=date(2027, 1, 15))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_snapshot_quote(symbol='AAPL', expiration=date(2027, 1, 15))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]