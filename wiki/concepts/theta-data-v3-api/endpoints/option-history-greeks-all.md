---
tags: ["option", "history", "greeks", "all-greeks", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History All Greeks

## Summary
All Greeks

## Operation ID
`option_history_greeks_all`

## Description
- Returns the data for all contracts that share the same provided symbol and expiration. 
- Calculated using the option and underlying midpoint price. If an interval size is specified (*highly recommended*), the option quote used in the calculation follows the same rules as the [quote](/operations/option_history_quote.html) endpoint. 
- The underlying price represents whatever the last underlying price was at the ``timestamp`` field. You can read more about how Theta Data calculates greeks [here](/Articles/Data-And-Requests/Option-Greeks.html).
- Multi-day requests are limited to 1 month of data.

## Minimum Subscription
`professional`

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
        *   `theta` (number): The Theta.
        *   `vega` (number): The vega.
        *   `rho` (number): The rho.
        *   `epsilon` (number): The epsilon.
        *   `lambda` (number): The lambda.
        *   `gamma` (number): The gamma.
        *   `vanna` (number): The vanna.
        *   `charm` (number): The charm.
        *   `vomma` (number): The vomma.
        *   `veta` (number): The veta.
        *   `vera` (number): The vera.
        *   `speed` (number): The speed.
        *   `zomma` (number): The zomma.
        *   `color` (number): The color.
        *   `ultima` (number): The ultima.
        *   `d1` (string): The d1.
        *   `d2` (string): The d2.
        *   `dual_delta` (number): The dual delta.
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
      "contract": {"symbol":"AAPL","strike":262.500,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"dual_delta":0.0000,"color":0.0000,"zomma":0.0000,"delta":0.0000,"implied_vol":0.2500,"theta":0.0000,"d1":-6.5422,"speed":0.0000,"d2":-6.5683,"epsilon":0.0000,"lambda":261.9304,"vomma":0.0000,"underlying_timestamp":"2024-11-04T09:30:00","timestamp":"2024-11-04T09:30:00","underlying_price":221.00,"vera":0.0000,"veta":0.0000,"iv_error":100.0000,"ultima":0.0001,"charm":0.0000,"ask":0.00,"rho":0.0000,"vanna":0.0000,"dual_gamma":0.0000,"bid":0.00,"vega":0.0000,"gamma":0.0000},
        {"dual_delta":-0.0021,"color":-0.0005,"zomma":0.0000,"delta":0.0026,"implied_vol":0.5874,"theta":-0.0138,"d1":-2.7911,"speed":0.0000,"d2":-2.8526,"epsilon":-0.0063,"lambda":55.3974,"vomma":2.5389,"underlying_timestamp":"2024-11-04T09:40:00","timestamp":"2024-11-04T09:40:00","underlying_price":220.56,"vera":0.0000,"veta":0.0136,"iv_error":0.0455,"ultima":21.4427,"charm":-1.0623,"ask":0.02,"rho":0.0062,"vanna":0.0393,"dual_gamma":0.0000,"bid":0.00,"vega":0.1873,"gamma":0.0005},
        {"dual_delta":-0.0020,"color":-0.0005,"zomma":0.0000,"delta":0.0025,"implied_vol":0.5749,"theta":-0.0130,"d1":-2.8050,"speed":0.0000,"d2":-2.8652,"epsilon":-0.0060,"lambda":56.7822,"vomma":2.5262,"underlying_timestamp":"2024-11-04T09:50:00","timestamp":"2024-11-04T09:50:00","underlying_price":221.20,"vera":0.0000,"veta":0.0133,"iv_error":-0.0199,"ultima":22.1272,"charm":-1.0265,"ask":0.02,"rho":0.0059,"vanna":0.0388,"dual_gamma":0.0000,"bid":0.00,"vega":0.1807,"gamma":0.0005},
        {"dual_delta":-0.0021,"color":-0.0005,"zomma":0.0000,"delta":0.0025,"implied_vol":0.5625,"theta":-0.0129,"d1":-2.8027,"speed":0.0000,"d2":-2.8616,"epsilon":-0.0061,"lambda":57.9900,"vomma":2.6034,"underlying_timestamp":"2024-11-04T10:00:00","timestamp":"2024-11-04T10:00:00","underlying_price":222.06,"vera":0.0000,"veta":0.0136,"iv_error":-0.0299,"ultima":23.2345,"charm":-1.0319,"ask":0.02,"rho":0.0060,"vanna":0.0399,"dual_gamma":0.0000,"bid":0.00,"vega":0.1825,"gamma":0.0006},
        {"dual_delta":0.0000,"color":0.0000,"zomma":0.0000,"delta":0.0000,"implied_vol":0.2500,"theta":0.0000,"d1":-6.3404,"speed":0.0000,"d2":-6.3666,"epsilon":0.0000,"lambda":254.5285,"vomma":0.0000,"underlying_timestamp":"2024-11-04T10:10:00","timestamp":"2024-11-04T10:10:00","underlying_price":222.17,"vera":0.0000,"veta":0.0000,"iv_error":100.0000,"ultima":0.0004,"charm":0.0000,"ask":0.01,"rho":0.0000,"vanna":0.0000,"dual_gamma":0.0000,"bid":0.00,"vega":0.0000,"gamma":0.0000}
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
df = client.option_history_greeks_all(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='10m',
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_greeks_all(
    symbol='AAPL',
    expiration=date(2024, 11, 8),
    interval='10m',
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]