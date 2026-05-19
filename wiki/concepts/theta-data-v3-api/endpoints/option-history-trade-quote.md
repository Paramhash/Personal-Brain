---
tags: ["option", "history", "trade-quote", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Trade Quote

## Summary
Trade Quote

## Operation ID
`option_history_trade_quote`

## Description
- Returns every [trade](/operations/option_history_trade.html) reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) paired with the last NBBO quote reported by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) at the time of trade.
- A quote is matched with a trade if its timestamp ``<=`` the trade timestamp. 
- To match trades with quotes timestamps that are ``<`` the trade timestamp, specify the ``exclusive``parameter to ``true``. After thorough testing, we have determined that using ``exclusive=true`` might yield better results for various applications.
- Multi-day requests are limited to 1 month of data, and must specify an expiration.

## Minimum Subscription
`standard`

## History Access
`true`

## Parameters
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/start-time.md|start_time]] (Optional)
*   [[../parameters/end-time.md|end_time]] (Optional)
*   [[../parameters/exclusive.md|exclusive]] (Optional)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns every trade quote for an option contract

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
    {
      "contract": {"symbol":"AAPL","strike":220.000,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"ask_size":14,"trade_timestamp":"2024-11-04T09:30:00.471","ask_condition":50,"sequence":18902138,"condition":130,"size":2,"bid_size":14,"ask_exchange":47,"price":3.90,"ext_condition2":255,"bid_exchange":47,"ask":4.05,"quote_timestamp":"2024-11-04T09:30:00.396","ext_condition1":255,"ext_condition4":255,"exchange":22,"ext_condition3":255,"bid":3.90,"bid_condition":50},
        {"ask_size":35,"trade_timestamp":"2024-11-04T09:30:01.626","ask_condition":50,"sequence":19368856,"condition":130,"size":1,"bid_size":93,"ask_exchange":73,"price":4.25,"ext_condition2":255,"bid_exchange":76,"ask":4.30,"quote_timestamp":"2024-11-04T09:30:01.594","ext_condition1":255,"ext_condition4":255,"exchange":6,"ext_condition3":255,"bid":4.15,"bid_condition":50},
        {"ask_size":59,"trade_timestamp":"2024-11-04T09:30:01.698","ask_condition":50,"sequence":19403970,"condition":130,"size":1,"bid_size":59,"ask_exchange":69,"price":4.22,"ext_condition2":255,"bid_exchange":69,"ask":4.30,"quote_timestamp":"2024-11-04T09:30:01.643","ext_condition1":255,"ext_condition4":255,"exchange":6,"ext_condition3":255,"bid":4.15,"bid_condition":50},
        {"ask_size":81,"trade_timestamp":"2024-11-04T09:30:02.064","ask_condition":50,"sequence":19598457,"condition":18,"size":1,"bid_size":31,"ask_exchange":11,"price":4.15,"ext_condition2":255,"bid_exchange":69,"ask":4.30,"quote_timestamp":"2024-11-04T09:30:02.039","ext_condition1":255,"ext_condition4":255,"exchange":5,"ext_condition3":255,"bid":4.15,"bid_condition":50},
        {"ask_size":81,"trade_timestamp":"2024-11-04T09:30:02.064","ask_condition":50,"sequence":19598464,"condition":18,"size":1,"bid_size":31,"ask_exchange":11,"price":4.15,"ext_condition2":255,"bid_exchange":69,"ask":4.30,"quote_timestamp":"2024-11-04T09:30:02.039","ext_condition1":255,"ext_condition4":255,"exchange":5,"ext_condition3":255,"bid":4.15,"bid_condition":50}      
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
df = client.option_history_trade_quote(symbol='AAPL', expiration=date(2024, 11, 8))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_trade_quote(symbol='AAPL', expiration=date(2024, 11, 8))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]