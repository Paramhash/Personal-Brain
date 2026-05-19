---
tags: ["option", "history", "greeks", "first-order-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History First Order Greeks

## Summary
First Order Greeks

## Operation ID
`option_history_greeks_first_order`

## Description
- Returns the data for all contracts that share the same provided symbol and expiration. 
- Calculated using the option and underlying midpoint price. If an interval size is specified (*highly recommended*), the option quote used in the calculation follows the same rules as the [quote](/operations/option_history_quote.html) endpoint. 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data.

## Minimum Subscription
`standard`

## History Access
`true`

## Parameters
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration-no-star.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/start-time.md|start_time]] (Optional)
*   [[../parameters/end-time.md|end_time]] (Optional)
*   [[../parameters/interval.md|interval]] (Required)
*   [[../parameters/annual-dividend.md|annual_dividend]] (Optional)
*   [[../parameters/rate-type.md|rate_type]] (Optional)
*   [[../parameters/rate-value.md|rate_value]] (Optional)
*   [[../parameters/greeks-version.md|version]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

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
        *   `theta` (number): The Theta.
        *   `vega` (number): The vega.
        *   `rho` (number): The rho.
        *   `epsilon` (number): The epsilon.
        *   `lambda` (number): The lambda.
        *   `implied_vol` (number): The implied volatiltiy calculated using the trade price.
        *   `iv_error` (number): IV Error: the value of the option calculated using the implied volatiltiy divided by the actual value reported in the quote. This value will increase as the strike price recedes from the underlying price.
        *   `underlying_timestamp` (string, format: `date-time`): The underlying date formated as YYYY-MM-DDTHH:mm:ss.SSS format.
        *   `underlying_price` (number): The midpoint of the underlying at the time of the option trade.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":262.500,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"underlying_price":221.00,"delta":0.0000,"implied_vol":0.2500,"theta":0.0000,"iv_error":100.0000,"epsilon":0.0000,"lambda":261.9304,"ask":0.00,"rho":0.0000,"bid":0.00,"underlying_timestamp":"2024-11-04T09:30:00","vega":0.0000,"timestamp":"2024-11-04T09:30:00"},
        {"underlying_price":220.66,"delta":0.0026,"implied_vol":0.5874,"theta":-0.0141,"iv_error":0.0721,"epsilon":-0.0064,"lambda":55.2930,"ask":0.02,"rho":0.0063,"bid":0.00,"underlying_timestamp":"2024-11-04T09:35:00","vega":0.1913,"timestamp":"2024-11-04T09:35:00"},
        {"underlying_price":220.56,"delta":0.0026,"implied_vol":0.5874,"theta":-0.0138,"iv_error":0.0455,"epsilon":-0.0063,"lambda":55.3974,"ask":0.02,"rho":0.0062,"bid":0.00,"underlying_timestamp":"2024-11-04T09:40:00","vega":0.1873,"timestamp":"2024-11-04T09:40:00"},
        {"underlying_price":220.86,"delta":0.0025,"implied_vol":0.5812,"theta":-0.0133,"iv_error":0.0075,"epsilon":-0.0061,"lambda":56.1024,"ask":0.02,"rho":0.0060,"bid":0.00,"underlying_timestamp":"2024-11-04T09:45:00","vega":0.1832,"timestamp":"2024-11-04T09:45:00"},
        {"underlying_price":221.20,"delta":0.0025,"implied_vol":0.5749,"theta":-0.0130,"iv_error":-0.0199,"epsilon":-0.0060,"lambda":56.7822,"ask":0.02,"rho":0.0059,"bid":0.00,"underlying_timestamp":"2024-11-04T09:50:00","vega":0.1807,"timestamp":"2024-11-04T09:50:00"}
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
df = client.option_history_greeks_first_order(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='5m',
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_greeks_first_order(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='5m',
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]