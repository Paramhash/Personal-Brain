---
tags: ["stock", "snapshot", "ohlc", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock Snapshot Open High Low Close

## Summary
Open High Low Close

## Operation ID
`stock_snapshot_ohlc`

## Description
Provides a real-time Open, High, Low, Close for the current day.
* Returns a real-time session OHLC from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
* Returns a 15-minute delayed session OHLC from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs) if the account has the stocks value subscription.
* Theta Data resets its snapshot cache at midnight ET every day. This endpoint may not work on a weekend where there were no eligible messages sent over exchange feeds. We recommend using historic requests during the weekend.

## Minimum Subscription
`value`

## Parameters
*   [[../parameters/multi-symbol.md|symbol]] (Required)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/min-time.md|min_time]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns OHLC for stocks for all symbols

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `timestamp` (string, format: `date-time`): The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
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
    {"volume":119656,"symbol":"CVCO","high":492.0000,"low":480.5477,"count":7684,"close":485.1100,"open":492.0000,"timestamp":"2025-08-20T16:10:04.43"},
    {"volume":57048,"symbol":"IFRX","high":0.9199,"low":0.8529,"count":138,"close":0.8929,"open":0.8900,"timestamp":"2025-08-20T16:11:13.962"},
    {"volume":9,"symbol":"KLXY","high":0.0000,"low":0.0000,"count":6,"close":0.0000,"open":0.0000,"timestamp":"2025-08-20T16:04:10.564"},
    {"volume":3648,"symbol":"HCOW","high":23.6976,"low":23.5600,"count":44,"close":23.6616,"open":23.5600,"timestamp":"2025-08-20T16:04:07.554"},
    {"volume":992620,"symbol":"SCS","high":16.3200,"low":16.1550,"count":7690,"close":16.1800,"open":16.2000,"timestamp":"2025-08-20T16:22:32.726"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_snapshot_ohlc(symbol=['AAPL'])
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_snapshot_ohlc(symbol=['AAPL'])
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]