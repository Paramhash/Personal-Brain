---
tags: ["option", "snapshot", "greeks", "second-order-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option Snapshot Second Order Greeks

## Summary
Second Order Greeks

## Operation ID
`option_snapshot_greeks_second_order`

## Description
- Retrieve a real-time last second order greeks calculation for all option contracts that lie on a provided expiration.
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
**Description:** Returns second order greeks for an option contract

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
        *   `gamma` (number): The gamma.
        *   `vanna` (number): The vanna.
        *   `charm` (string): The charm.
        *   `vomma` (number): The vomma.
        *   `veta` (number): The veta.
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
        {"underlying_price":225.74,"veta":18.8522,"implied_vol":0.2142,"iv_error":-0.0003,"charm":-0.3716,"ask":1.50,"vanna":1.1833,"vomma":212.2670,"bid":1.47,"underlying_timestamp":"2025-08-20T16:37:06.988","gamma":0.0059,"timestamp":"2025-08-20T15:59:59.805"}
      ]
    },
    {
      "contract": {"symbol":"AAPL","strike":275.000,"right":"PUT","expiration":"2026-01-16"},
      "data": [
        {"underlying_price":225.74,"veta":18.2234,"implied_vol":0.3106,"iv_error":0.0000,"charm":-0.4210,"ask":49.70,"vanna":0.9320,"vomma":108.3415,"bid":48.75,"underlying_timestamp":"2025-08-20T16:37:06.988","gamma":0.0064,"timestamp":"2025-08-20T15:59:59.839"}        
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
df = client.option_snapshot_greeks_second_order(symbol='AAPL', expiration=date(2027, 1, 15))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_snapshot_greeks_second_order(symbol='AAPL', expiration=date(2027, 1, 15))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]