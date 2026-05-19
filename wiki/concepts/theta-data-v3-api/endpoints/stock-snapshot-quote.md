---
tags: ["stock", "snapshot", "quote", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock Snapshot Quote

## Summary
Quote

## Operation ID
`stock_snapshot_quote`

## Description
* Returns a real-time last BBO quote from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
* Returns a 15-minute delayed NBBO quote from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs) account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.
- Theta Data resets its snapshot cache at midnight ET every day. This endpoint may not work on a weekend where there were no eligible messages sent over exchange feeds. We recommend using historic requests during the weekend.

## Minimum Subscription
`value`

## Parameters
*   [[../parameters/multi-symbol.md|symbol]] (Required)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/min-time.md|min_time]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns last quote for stocks for all symbols

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `timestamp` (string, format: `date-time`): The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
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
    {"symbol":"CVCO","ask_size":3,"bid_size":1,"ask_exchange":29,"ask_condition":0,"bid_exchange":29,"ask":494.33,"bid":475.75,"bid_condition":0,"timestamp":"2025-08-20T16:03:05.142"},
    {"symbol":"KLXY","ask_size":200,"bid_size":200,"ask_exchange":29,"ask_condition":0,"bid_exchange":29,"ask":37.18,"bid":12.40,"bid_condition":0,"timestamp":"2025-08-20T16:10:05.032"},
    {"symbol":"IFRX","ask_size":45,"bid_size":100,"ask_exchange":29,"ask_condition":0,"bid_exchange":29,"ask":0.9500,"bid":0.7510,"bid_condition":0,"timestamp":"2025-08-20T16:21:05.781"},
    {"symbol":"SCS","ask_size":100,"bid_size":100,"ask_exchange":29,"ask_condition":0,"bid_exchange":29,"ask":17.60,"bid":14.64,"bid_condition":0,"timestamp":"2025-08-20T16:19:55.101"},
    {"symbol":"BBC","ask_size":2800,"bid_size":100,"ask_exchange":29,"ask_condition":0,"bid_exchange":29,"ask":24.06,"bid":13.29,"bid_condition":0,"timestamp":"2025-08-20T16:33:50.877"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_snapshot_quote(symbol=['AAPL'])
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_snapshot_quote(symbol=['AAPL'])
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]