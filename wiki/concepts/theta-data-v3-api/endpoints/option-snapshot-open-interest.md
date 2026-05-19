---
tags: ["option", "snapshot", "open-interest", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Open Interest

## Summary
Open Interest

## Operation ID
`option_snapshot_open_interest`

## Description
- Retrieve the last open interest message of an option contract.
- Open interest is reported around 06:30 ET every morning by OPRA and reflects the open interest at the of the previous trading day. 
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
**Description:** Returns open interest for an option contract

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
        *   `open_interest` (integer): The total amount of outstanding contracts.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":275.000,"expiration":"2026-01-16","right":"CALL"},
      "data": [
        {"open_interest":8066,"timestamp":"2025-08-20T06:30:13"}                      
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
df = client.option_snapshot_open_interest(symbol='AAPL', expiration=date(2027, 1, 15))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_snapshot_open_interest(symbol='AAPL', expiration=date(2027, 1, 15))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]