---
tags: ["option", "history", "eod", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History End of Day

## Summary
End of Day

## Operation ID
`option_history_eod`

## Description
- Since [OPRA](/Articles/Data-And-Requests/The-SIPs.html) does not provide a national EOD report for options, Theta Data generates a national EOD report at 17:15 ET each day.
- ``created`` represents the datetime the report was generated and ``last_trade`` represents the datetime of the last trade. 
- The quote in the response represents the last NBBO reported by OPRA at the time of report generation. 
- You can read more about EOD & OHLC data [here](/Articles/Data-And-Requests/OHLC-EOD.html).

## Minimum Subscription
`free`

## History Access
`true`

## Parameters
*   [[../parameters/start-date.md|start_date]] (Required)
*   [[../parameters/end-date.md|end_date]] (Required)
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns EOD report for an option contract

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
    {
      "contract": {"symbol":"AAPL","strike":170.000,"right":"CALL","expiration":"2024-11-15"},
      "data": [
        {"ask_size":15,"last_trade":"2024-11-04T15:48:12.005","created":"2024-11-04T17:16:56.205","ask_condition":50,"count":3,"volume":10,"high":52.75,"low":52.40,"bid_size":70,"ask_exchange":47,"bid_exchange":60,"ask":52.45,"bid":52.05,"bid_condition":50,"close":52.40,"open":52.54}                      
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
df = client.option_history_eod(
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
    symbol='AAPL',
    expiration=date(2024, 11, 15),
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_eod(
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
    symbol='AAPL',
    expiration=date(2024, 11, 15),
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]