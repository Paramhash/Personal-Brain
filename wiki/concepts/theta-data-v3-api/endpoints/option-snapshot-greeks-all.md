---
tags: ["option", "snapshot", "greeks", "all-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot All Greeks

## Summary
All Greeks

## Operation ID
`option_snapshot_greeks_all`

## Description
- Retrieve a real-time last greeks calculation for all option contracts that lie on a provided expiration.
- You might need to change the default expiration date to a different date if it is past the current date. Some quotes are omitted in the example to reduce the space of the sample output.
- Make `expiration` * if you want to get the snapshot for every expiration chain for the underlying.
> This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

## Minimum Subscription
`professional`

## Parameters
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/annual-dividend.md|annual_dividend]] (Optional)
*   [[../parameters/rate-type.md|rate_type]] (Optional)
*   [[../parameters/rate-value.md|rate_value]] (Optional)
*   [[../parameters/stock-price.md|stock_price]] (Optional)
*   [[../parameters/greeks-version.md|version]] (Optional)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/min-time.md|min_time]] (Optional)
*   [[../parameters/use-market-value.md|use_market_value]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** Returns all greeks for an option contract

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
        *   `bid` (number): The last NBBO bid price.
        *   `ask` (number): The last NBBO ask price.
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
      "contract": {"symbol":"AAPL","expiration":"2026-05-15","strike":170.000,"right":"CALL"},
      "data": [
        {"dual_delta":-0.8302,"color":-0.0816,"zomma":0.0000,"delta":0.9085,"implied_vol":0.3075,"theta":-0.0352,"d1":1.3319,"speed":0.0000,"d2":1.0689,"epsilon":-150.0314,"lambda":3.2071,"vomma":146.8562,"underlying_timestamp":"2025-08-20T16:36:52.257","timestamp":"2025-08-20T15:59:59.677","underlying_price":225.74,"vera":0.0000,"veta":22.9525,"iv_error":0.0000,"ultima":-100.0000,"charm":0.0925,"ask":64.25,"rho":103.2513,"vanna":-0.5710,"dual_gamma":0.0003,"bid":63.65,"vega":31.7235,"gamma":0.0027}
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
df = client.option_snapshot_greeks_all(symbol='AAPL', expiration=date(2026, 5, 15))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_snapshot_greeks_all(symbol='AAPL', expiration=date(2026, 5, 15))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]