---
tags: ["option", "history", "ohlc", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Open High Low Close

## Summary
Open High Low Close

## Operation ID
`option_history_ohlc`

## Description
- Aggregated OHLC bars that use [SIP rules](/Articles/Data-And-Requests/OHLC-EOD.html) for each bar. 
- Time timestamp of the bar represents the opening time of the bar. For a trade to be part of the bar: ``bar timestamp`` <= ``trade time`` < ``bar timestamp + interval``.
- Multi-day requests are limited to 1 month of data.

## Minimum Subscription
`value`

## History Access
`true`

## Parameters
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration-no-star.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/interval.md|interval]] (Required)
*   [[../parameters/start-time.md|start_time]] (Optional)
*   [[../parameters/end-time.md|end_time]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns OHLC for an option contract

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
        *   `open` (number): The opening trade price.
        *   `high` (number): The highest traded price.
        *   `low` (number): The lowest traded price.
        *   `close` (number): The closing traded price.
        *   `volume` (integer): The amount of contracts / shares traded.
        *   `count` (integer): The amount of trades.
        *   `vwap` (number): The volume weighted average price of the trading session.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":170.000,"right":"CALL","expiration":"2023-11-03"},
      "data": [
        {"volume":147,"high":7.05,"low":3.60,"vwap":4.39,"count":24,"close":4.00,"open":4.48,"timestamp":"2023-11-03T09:30:00"},
        {"volume":39,"high":4.65,"low":3.65,"vwap":4.31,"count":19,"close":4.65,"open":3.85,"timestamp":"2023-11-03T09:31:00"},
        {"volume":45,"high":5.20,"low":4.65,"vwap":4.45,"count":14,"close":5.00,"open":4.75,"timestamp":"2023-11-03T09:32:00"},
        {"volume":142,"high":5.05,"low":4.48,"vwap":4.53,"count":23,"close":4.49,"open":4.95,"timestamp":"2023-11-03T09:33:00"},        
        {"volume":29,"high":5.05,"low":4.50,"vwap":4.56,"count":11,"close":4.73,"open":4.50,"timestamp":"2023-11-03T09:34:00"}
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
df = client.option_history_ohlc(
    symbol='AAPL',
    expiration=date(2023, 11, 3),
    interval='1m',
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_ohlc(
    symbol='AAPL',
    expiration=date(2023, 11, 3),
    interval='1m',
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]