---
tags: ["option", "list", "strikes", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Strikes

## Summary
Strikes

## Operation ID
`option_list_strikes`

## Description
Lists all strikes that are available for an option with a given symbol and expiration date.
This endpoint is updated overnight.

## Minimum Subscription
`free`

## Parameters
*   [[../parameters/multi-symbol.md|symbol]] (Required)
*   [[../parameters/expiration-no-star.md|expiration]] (Required)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** List all strikes for an option with a given symbol and expiration date

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
        *   `strike` (number): Strike price of the contract in dollars 180.00

**Example (application/json):**
```json
{
  "response": [
    {"symbol":"AAPL","strike":80.000},
    {"symbol":"AAPL","strike":128.000},
    {"symbol":"AAPL","strike":160.000},
    {"symbol":"AAPL","strike":144.000},
    {"symbol":"AAPL","strike":240.000}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_strikes(symbol=['AAPL'], expiration=date(2022, 9, 30))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_list_strikes(symbol=['AAPL'], expiration=date(2022, 9, 30))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]