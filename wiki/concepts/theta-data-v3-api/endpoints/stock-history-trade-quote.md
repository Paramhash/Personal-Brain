---
tags: ["stock", "history", "trade-quote", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock History Trade Quote

## Summary
Trade Quote

## Operation ID
`stock_history_trade_quote`

## Description
Returns every trade reported by [UTP & CTA](/Articles/Data-And-Requests/The-SIPs) paired with the last BBO quote reported by [UTP or CTA](/Articles/Data-And-Requests/The-SIPs) at the time of trade. A quote is matched with a trade if its timestamp ``<=`` the trade timestamp. If you prefer to match quotes with timestamps that are ``<`` the trade timestamp, specify the ``exclusive`` parameter to ``true``. Set the ``venue`` parameter to ``nqb`` to access current-day real-time historic data from the [Nasdaq Basic feed](/Articles/Data-And-Requests/The-SIPs) if the account has a [stocks standard or pro subscription](https://www.thetadata.net/subscribe.html#stocks).
- Multi-day requests are limited to 1 month of data.

## Minimum Subscription
`standard`

## History Access
`true`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/start-time.md|start_time]] (Optional)
*   [[../parameters/end-time.md|end_time]] (Optional)
*   [[../parameters/exclusive.md|exclusive]] (Optional)
*   [[../parameters/venue.md|venue]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns every trade quote for a given symbol between specified dates (inclusive)

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `trade_timestamp` (string, format: `date-time`): The trade date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `quote_timestamp` (string, format: `date-time`): The quote date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `sequence` (integer): The exchange [sequence](/Articles/Data-And-Requests/Making-Requests.html#trade-sequences).
        *   `ext_condition1` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `ext_condition2` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `ext_condition3` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `ext_condition4` (integer): Additional trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html)(s). These can be ignored for options.
        *   `condition` (integer): The trade [condition](/Articles/Errors-Exchanges-Conditions/Trade-Conditions.html).
        *   `size` (integer): The amount of contracts / shares traded.
        *   `exchange` (integer): The [exchange](/Articles/Errors-Exchanges-Conditions/Exchanges.html) the trade was executed.
        *   `price` (number): The trade price.
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
    {"ask_size":1,"trade_timestamp":"2023-01-03T09:30:00.002","ask_condition":0,"sequence":562,"condition":115,"size":1,"bid_size":4,"ask_exchange":7,"price":130.3300,"ext_condition2":255,"bid_exchange":7,"ask":130.4000,"quote_timestamp":"2023-01-03T09:30:00.001","ext_condition1":32,"ext_condition4":115,"exchange":60,"ext_condition3":255,"bid":130.2600,"bid_condition":0},
    {"ask_size":1,"trade_timestamp":"2023-01-03T09:30:00.003","ask_condition":0,"sequence":563,"condition":115,"size":24,"bid_size":4,"ask_exchange":7,"price":130.3300,"ext_condition2":255,"bid_exchange":7,"ask":130.4000,"quote_timestamp":"2023-01-03T09:30:00.002","ext_condition1":32,"ext_condition4":115,"exchange":60,"ext_condition3":255,"bid":130.2600,"bid_condition":0},
    {"ask_size":1,"trade_timestamp":"2023-01-03T09:30:00.003","ask_condition":0,"sequence":564,"condition":115,"size":40,"bid_size":4,"ask_exchange":7,"price":130.3300,"ext_condition2":255,"bid_exchange":7,"ask":130.4000,"quote_timestamp":"2023-01-03T09:30:00.002","ext_condition1":32,"ext_condition4":115,"exchange":60,"ext_condition3":255,"bid":130.2600,"bid_condition":0},
    {"ask_size":1,"trade_timestamp":"2023-01-03T09:30:00.036","ask_condition":0,"sequence":6081,"condition":1,"size":19,"bid_size":4,"ask_exchange":1,"price":130.2500,"ext_condition2":95,"bid_exchange":7,"ask":130.3900,"quote_timestamp":"2023-01-03T09:30:00.017","ext_condition1":32,"ext_condition4":115,"exchange":1,"ext_condition3":1,"bid":130.2600,"bid_condition":0},
    {"ask_size":1,"trade_timestamp":"2023-01-03T09:30:00.057","ask_condition":0,"sequence":6082,"condition":1,"size":30,"bid_size":4,"ask_exchange":1,"price":130.2500,"ext_condition2":255,"bid_exchange":7,"ask":130.3900,"quote_timestamp":"2023-01-03T09:30:00.017","ext_condition1":32,"ext_condition4":115,"exchange":1,"ext_condition3":1,"bid":130.2600,"bid_condition":0}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_history_trade_quote(symbol='AAPL')
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_history_trade_quote(symbol='AAPL')
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]