---
tags: ["option", "history", "greeks", "eod-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History End of Day Greeks

## Summary
End of Day Greeks

## Operation ID
`option_history_greeks_eod`

## Description
- Returns the data for all contracts that share the same provided symbol and expiration. 
- Uses Theta Data's EOD reports that get generated at 17:15 ET each day. The closing option price and closing underlying price are used for the greeks calculation.
- **Set `expiration` to ``*`` if you want to retrieve data for every option that shares the same ``symbol``. (note: Any ``expiration=*`` must be requested day by day)**

## Minimum Subscription
`standard`

## History Access
`true`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/start-date.md|start_date]] (Required)
*   [[../parameters/end-date.md|end_date]] (Required)
*   [[../parameters/annual-dividend.md|annual_dividend]] (Optional)
*   [[../parameters/rate-type.md|rate_type]] (Optional)
*   [[../parameters/rate-value.md|rate_value]] (Optional)
*   [[../parameters/greeks-version.md|version]] (Optional)
*   [[../parameters/underlyer-use-nbbo.md|underlyer_use_nbbo]] (Optional)
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
        *   `timestamp` (string, format: `date-time`): The timestamp in YYYY-MM-DDTHH:mm:ss.SSS format.
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
        *   `delta` (number): The delta.
        *   `theta` (string): The Theta.
        *   `vega` (number): The vega.
        *   `rho` (number): The rho.
        *   `epsilon` (string): The epsilon.
        *   `lambda` (number): The lambda.
        *   `gamma` (number): The gamma.
        *   `vanna` (string): The vanna.
        *   `charm` (number): The charm.
        *   `vomma` (number): The vomma.
        *   `veta` (number): The veta.
        *   `vera` (number): The vera.
        *   `speed` (number): The speed.
        *   `zomma` (number): The zomma.
        *   `color` (string): The color.
        *   `ultima` (string): The ultima.
        *   `d1` (number): The d1.
        *   `d2` (number): The d2.
        *   `dual_delta` (string): The dual delta.
        *   `dual_gamma` (number): The dual gamma.
        *   `implied_vol` (number): The implied volatiltiy calculated using the trade price.
        *   `iv_error` (number): IV Error: the value of the option calculated using the implied volatiltiy divided by the actual value reported in the quote. This value will increase as the strike price recedes from the underlying price.
        *   `underlying_timestamp` (string, format: `date-time`): The underlying date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price` (number): The midpoint of the underlying at the time of the option trade.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":220.000,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"ask_size":12,"dual_delta":-0.5945,"color":-0.0163,"zomma":0.0000,"delta":0.6083,"implied_vol":0.3334,"theta":-0.3892,"d1":0.2750,"speed":0.0000,"d2":0.2401,"epsilon":-1.4791,"high":4.85,"lambda":32.3623,"low":3.35,"ask_exchange":5,"bid_exchange":11,"vomma":1.7667,"bid_condition":50,"underlying_timestamp":"2024-11-04T17:15:28.71","close":4.15,"timestamp":"2024-11-04T15:59:59.828","underlying_price":221.870,"ask_condition":50,"count":1511,"vera":0.0000,"veta":0.0149,"iv_error":0.0001,"ultima":-15.6407,"volume":7425,"charm":3.6779,"bid_size":9,"ask":4.25,"rho":1.4334,"vanna":-0.2765,"dual_gamma":0.0000,"bid":4.10,"open":3.90,"vega":8.9221,"gamma":0.0495}
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
df = client.option_history_greeks_eod(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_greeks_eod(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    start_date=date(2024, 11, 4),
    end_date=date(2024, 11, 4),
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]