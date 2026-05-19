---
tags: ["stock", "history", "quote", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock History Quote

## Summary
Quote

## Operation ID
`stock_history_quote`

## Description
- Returns every NBBO quote reported by [UTP and CTA](/Articles/Data-And-Requests/The-SIPs). 
- If the ``interval`` parameter is specified, the quote for each interval represents the last quote prior to the interval's timestamp. 
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
**Description:** Returns every quote for a given symbol between specified dates (inclusive) with a one minute interval

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
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
    {"ask_size":1,"bid_size":30,"ask_exchange":1,"ask_condition":0,"bid_exchange":7,"ask":187.20,"bid":187.10,"bid_condition":0,"timestamp":"2024-01-02T09:30:00"},
    {"ask_size":4,"bid_size":2,"ask_exchange":1,"ask_condition":0,"bid_exchange":1,"ask":187.86,"bid":187.83,"bid_condition":0,"timestamp":"2024-01-02T09:31:00"},
    {"ask_size":1,"bid_size":2,"ask_exchange":73,"ask_condition":0,"bid_exchange":60,"ask":187.77,"bid":187.74,"bid_condition":0,"timestamp":"2024-01-02T09:32:00"},
    {"ask_size":2,"bid_size":2,"ask_exchange":73,"ask_condition":0,"bid_exchange":60,"ask":188.32,"bid":188.29,"bid_condition":0,"timestamp":"2024-01-02T09:33:00"},
    {"ask_size":2,"bid_size":5,"ask_exchange":7,"ask_condition":0,"bid_exchange":1,"ask":188.16,"bid":188.14,"bid_condition":0,"timestamp":"2024-01-02T09:34:00"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_history_quote(symbol='AAPL', interval='1m')
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_history_quote(symbol='AAPL', interval='1m')
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]