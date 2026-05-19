---
tags: ["stock", "snapshot", "market-value", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock Snapshot Market Value

## Summary
Market Value

## Operation ID
`stock_snapshot_market_value`

## Description
* Returns a real-time market value derived from the last BBO quote from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
* Returns a 15-minute delayed market value derived from an NBBO quote from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs) if the account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.
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
**Description:** Returns last market value for stocks for all symbols

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `timestamp` (string, format: `date-time`): The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
        *   `market_bid` (number): The last market bid
        *   `market_ask` (number): The last market ask
        *   `market_price` (number): The last market value price

**Example (application/json):**
```json
{
  "response": [
    {"symbol":"CVCO","market_bid":590.60,"market_ask":595.55,"market_price":593.07,"timestamp":"2025-12-16T11:47:50.854"},
    {"symbol":"KLXY","market_bid":26.77,"market_ask":27.69,"market_price":27.23,"timestamp":"2025-12-16T11:02:05.409"},
    {"symbol":"FXR","market_bid":80.23,"market_ask":80.27,"market_price":80.25,"timestamp":"2025-12-16T11:47:52.923"},
    {"symbol":"AAPL","market_bid":273.22,"market_ask":273.23,"market_price":273.22,"timestamp":"2025-12-16T11:47:53.496"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_snapshot_market_value(symbol=['AAPL'])
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_snapshot_market_value(symbol=['AAPL'])
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]