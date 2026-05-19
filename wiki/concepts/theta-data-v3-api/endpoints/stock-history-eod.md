---
tags: ["stock", "history", "eod", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock History End of Day

## Summary
End of Day

## Operation ID
`stock_history_eod`

## Description
Since [the equity SIPs](/Articles/Data-And-Requests/The-SIPs.html) only generate a partial EOD report, Theta Data generates a national EOD report at 17:15 ET each day. `created` represents the datetime the report was generated and `last_trade` represents the datetime of the last trade. The quote in the response represents the last NBBO reported by [CTA or UTP](/Articles/Data-And-Requests/The-SIPs.html) at the time of report generation. You can read more about EOD & OHLC data [here](/Articles/Data-And-Requests/OHLC-EOD.html). Theta Data plans to avail SIP EOD reports in the near future.

## Minimum Subscription
`free`

## History Access
`true`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/start-date.md|start_date]] (Required)
*   [[../parameters/end-date.md|end_date]] (Required)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns EOD report for a given symbol between specified dates (inclusive)

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `created` (string, format: `date-time`): The date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `last_trade` (string, format: `date-time`): The last trade date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `open` (number): The opening trade price.
        *   `high` (number): The highest traded price.
        *   `low` (number): The lowest traded price.
        *   `close` (number): The closing traded price.
        *   `volume` (integer): The amount of contracts / shares traded.
        *   `count` (integer): The amount of trades.
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
    {"ask_size":2,"last_trade":"2024-01-02T17:17:51.877","created":"2024-01-02T17:17:53.606","ask_condition":0,"count":1003582,"volume":80680243,"high":188.440,"low":183.885,"bid_size":2,"ask_exchange":1,"bid_exchange":7,"ask":18.536,"bid":18.534,"bid_condition":0,"close":185.640,"open":187.030},
    {"ask_size":2,"last_trade":"2024-01-03T17:16:28.586","created":"2024-01-03T17:16:29.883","ask_condition":0,"count":654127,"volume":58308345,"high":185.880,"low":183.430,"bid_size":5,"ask_exchange":1,"bid_exchange":7,"ask":18.410,"bid":18.405,"bid_condition":0,"close":184.250,"open":184.200},
    {"ask_size":2,"last_trade":"2024-01-04T17:17:02.445","created":"2024-01-04T17:17:06.02","ask_condition":0,"count":709246,"volume":71197269,"high":183.0872,"low":180.8800,"bid_size":8,"ask_exchange":7,"bid_exchange":60,"ask":1.8179,"bid":1.8176,"bid_condition":0,"close":181.9100,"open":182.0000},
    {"ask_size":3,"last_trade":"2024-01-05T17:16:49.821","created":"2024-01-05T17:16:57.032","ask_condition":0,"count":679405,"volume":61949135,"high":182.760,"low":180.170,"bid_size":3,"ask_exchange":7,"bid_exchange":1,"ask":18.105,"bid":18.103,"bid_condition":0,"close":181.180,"open":181.900},
    {"ask_size":1,"last_trade":"2024-01-08T17:17:01.484","created":"2024-01-08T17:17:01.83","ask_condition":0,"count":665626,"volume":59029146,"high":185.600,"low":181.500,"bid_size":4,"ask_exchange":65,"bid_exchange":1,"ask":18.537,"bid":18.528,"bid_condition":0,"close":185.560,"open":182.000}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.stock_history_eod(
    symbol='AAPL',
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 31),
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.stock_history_eod(
    symbol='AAPL',
    start_date=date(2024, 1, 1),
    end_date=date(2024, 1, 31),
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]