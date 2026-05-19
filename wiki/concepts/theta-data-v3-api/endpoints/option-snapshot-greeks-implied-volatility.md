---
tags: ["option", "snapshot", "greeks", "implied-volatility", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Implied Volatility

## Summary
Implied Volatility

## Operation ID
`option_snapshot_greeks_implied_volatility`

## Description
Returns implied volatilies calculated using the national best bid, mid, and ask price
of the option respectively. The underlying price represents whatever the last underlying price was at the
``underlying_timestamp`` field. You can read more about how Theta Data calculates greeks 
[here](/Articles/Data-And-Requests/Option-Greeks.html).

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
**Description:** Returns implied volatility for an option contract

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
        *   `implied_vol` (number): The implied volatiltiy calculated using the trade price.
        *   `iv_error` (string): IV Error: the value of the option calculated using the implied volatiltiy divided by the actual value reported in the quote. This value will increase as the strike price recedes from the underlying price.
        *   `underlying_timestamp` (string, format: `date-time`): The underlying date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price` (number): The midpoint of the underlying at the time of the option trade.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","expiration":"2026-01-16","strike":275.000,"right":"CALL"},
      "data": [
        {"underlying_price":225.74,"ask":1.50,"implied_vol":0.2142,"bid":1.47,"underlying_timestamp":"2025-08-20T16:36:52.257","iv_error":-0.0003,"timestamp":"2025-08-20T15:59:59.805"}
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
df = client.option_snapshot_greeks_implied_volatility(symbol='AAPL', expiration=date(2027, 1, 15))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_snapshot_greeks_implied_volatility(symbol='AAPL', expiration=date(2027, 1, 15))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]