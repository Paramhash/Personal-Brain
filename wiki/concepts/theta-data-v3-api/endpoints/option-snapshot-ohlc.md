---
tags: ["option", "snapshot", "ohlc", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Open High Low Close

## Summary
Open High Low Close

## Operation ID
`option_snapshot_ohlc`

## Description
- Retrieve a real-time last ohlc of an option contract for the trading day.
- You might need to change the default expiration date to a different date if it is past the current date.

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
**Description:** Returns OHLC for a given option contract

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
        *   `open` (number): The opening trade price.
        *   `high` (number): The highest traded price.
        *   `low` (number): The lowest traded price.
        *   `close` (number): The closing traded price.
        *   `volume` (integer): The amount of contracts / shares traded.
        *   `count` (integer): The amount of trades.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","expiration":"2026-01-16","strike":275.000,"right":"CALL"},
      "data": [
        {"volume":202,"high":1.78,"low":1.51,"count":29,"close":1.51,"open":1.78,"timestamp":"2025-08-20T15:25:31.03"}
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
df = client.option_snapshot_ohlc(symbol='AAPL', expiration=date(2027, 1, 15))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_snapshot_ohlc(symbol='AAPL', expiration=date(2027, 1, 15))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]