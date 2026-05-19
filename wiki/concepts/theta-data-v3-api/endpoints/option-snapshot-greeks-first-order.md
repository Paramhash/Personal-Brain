---
tags: ["option", "snapshot", "greeks", "first-order-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot First Order Greeks

## Summary
First Order Greeks

## Operation ID
`option_snapshot_greeks_first_order`

## Description
- Retrieve a real-time last greeks calculation for all option contracts that lie on a provided expiration.
- You might need to change the default expiration date to a different date if it is past the current date. Some quotes are omitted in the example to reduce the space of the sample output.
- Make `expiration` * if you want to get the snapshot for every expiration chain for the underlying.
> This endpoint will return no data if the market was closed for the day. Theta Data resets the snapshot cache at midnight ET every night.

## Minimum Subscription
`standard`

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
**Description:** Returns first order greeks for an option contract

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
        *   `implied_vol` (number): The implied volatiltiy calculated using the trade price.
        *   `iv_error` (string): IV Error: the value of the option calculated using the implied volatiltiy divided by the actual value reported in the quote. This value will increase as the strike price recedes from the underlying price.
        *   `underlying_timestamp` (string, format: `date-time`): The underlying date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price` (number): The midpoint of the underlying at the time of the option trade.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":275.000,"right":"CALL","expiration":"2026-01-16"},
      "data": [
        {"underlying_price":225.74,"delta":0.1060,"implied_vol":0.2142,"theta":-0.0217,"iv_error":-0.0003,"epsilon":-9.7049,"lambda":16.1782,"ask":1.50,"rho":9.1050,"bid":1.47,"underlying_timestamp":"2025-08-20T16:37:06.988","vega":26.3226,"timestamp":"2025-08-20T15:59:59.805"}
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
df = client.option_snapshot_greeks_first_order(symbol='AAPL', expiration=date(2027, 1, 15))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_snapshot_greeks_first_order(symbol='AAPL', expiration=date(2027, 1, 15))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]