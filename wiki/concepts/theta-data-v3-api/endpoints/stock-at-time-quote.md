---
tags: ["stock", "at-time", "quote", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock At-Time Quote

## Summary
Quote

## Operation ID
`stock_at_time_quote`

## Description
#### Real-time request:
  - Subscription tier standard or higher will default to NQB.
  - Real-time last BBO quote at-time_of_day-time from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs.html#nasdaq-basic) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
  - 15-minute delayed NBBO quote at-time_of_day-time from the [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) account has the [stocks value subscription](https://www.thetadata.net/subscribe.html#stocks) subscription.

#### Historical request:
  Returns the last NBBO quote reported by [UTP & CTA feeds](/Articles/Data-And-Requests/The-SIPs.html#equities-cta-utp) at a specified millisecond of the day.

## Minimum Subscription
`value`

## History Access
`true`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/start-date.md|start_date]] (Required)
*   [[../parameters/end-date.md|end_date]] (Required)
*   [[../parameters/time-of-day.md|time_of_day]] (Required)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns the last quote for a given symbol between specified dates (inclusive) with a one minute interval

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
    {"ask_size":8,"bid_size":15,"ask_exchange":7,"ask_condition":0,"bid_exchange":1,"ask":475.28,"bid":475.28,"bid_condition":0,"timestamp":"2024-01-16T09:30:00.1"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.stock_at_time_quote(
    symbol='SPY',
    start_date=date(2024, 1, 16),
    end_date=date(2024, 1, 16),
    time_of_day='09:30:00.100',
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.stock_at_time_quote(
    symbol='SPY',
    start_date=date(2024, 1, 16),
    end_date=date(2024, 1, 16),
    time_of_day='09:30:00.100',
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]