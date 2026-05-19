---
tags: ["stock", "snapshot", "trade", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock Snapshot Trade

## Summary
Trade

## Operation ID
`stock_snapshot_trade`

## Description
Returns a real-time last trade from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).

- Theta Data resets its snapshot cache at midnight ET every day. This endpoint may not work on a weekend where there were no eligible messages sent over exchange feeds. We recommend using historic requests during the weekend.

## Minimum Subscription
`standard`

## Parameters
*   [[../parameters/multi-symbol.md|symbol]] (Required)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/min-time.md|min_time]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns last trade for stocks for a given symbol

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `timestamp` (string, format: `date-time`): The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
        *   `sequence` (integer): The exchange [sequence](/Articles/Data-And-Requests/Making-Requests.html#trade-sequences).
        *   `size` (integer): The amount of contracts / shares traded.
        *   `condition` (integer): The trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
        *   `price` (number): The trade price.

**Example (application/json):**
```json
{
  "response": [
    {"symbol":"AAPL","sequence":63539137,"condition":1,"size":23,"price":225.7500,"timestamp":"2025-08-20T16:36:05.549"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_snapshot_trade(symbol=['AAPL'])
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_snapshot_trade(symbol=['AAPL'])
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]