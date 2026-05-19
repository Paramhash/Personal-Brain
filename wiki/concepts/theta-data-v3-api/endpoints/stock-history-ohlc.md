---
tags: ["stock", "history", "ohlc", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock History Open High Low Close

## Summary
Open High Low Close

## Operation ID
`stock_history_ohlc`

## Description
- Aggregated OHLC bars that use [SIP rules](/Articles/Data-And-Requests/OHLC-EOD.html) for each bar. Time timestamp of the bar represents the opening time of the bar. For a trade to be part of the bar: ``bar time`` <= ``trade time`` < ``bar timestamp + ivl``, where ivl is the specified interval size in milliseconds. 
- Set the ``venue`` parameter to ``nqb`` to access current-day real-time historic data from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Multi-day requests are limited to 1 month of data.

## Minimum Subscription
`value`

## History Access
`true`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/interval.md|interval]] (Required)
*   [[../parameters/start-time.md|start_time]] (Optional)
*   [[../parameters/end-time.md|end_time]] (Optional)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns OHLC for a given symbol between specified dates (inclusive) with a one minute interval

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
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
    {"volume":3256708,"high":188.050,"low":186.350,"vwap":187.25,"count":37886,"close":187.830,"open":187.1500,"timestamp":"2024-01-02T09:30:00"},
    {"volume":809707,"high":188.120,"low":187.630,"vwap":187.38,"count":7481,"close":187.765,"open":187.830,"timestamp":"2024-01-02T09:31:00"},
    {"volume":687086,"high":188.440,"low":187.730,"vwap":187.48,"count":7103,"close":188.2984,"open":187.770,"timestamp":"2024-01-02T09:32:00"},
    {"volume":485275,"high":188.310,"low":187.810,"vwap":187.53,"count":6245,"close":188.160,"open":188.3050,"timestamp":"2024-01-02T09:33:00"},
    {"volume":415948,"high":188.150,"low":187.670,"vwap":187.55,"count":5942,"close":187.730,"open":188.150,"timestamp":"2024-01-02T09:34:00"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_history_ohlc(symbol='AAPL', interval='1m')
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_history_ohlc(symbol='AAPL', interval='1m')
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]