---
tags: ["option", "list", "contracts", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Contracts

## Summary
Contracts

## Operation ID
`option_list_contracts`

## Description
Lists all contracts that were traded or quoted on a particular date.

If the ``symbol`` parameter is specified, the returned contracts will be filtered to match the symbol.
Multiple symbols can be specified by separating them with commas such as ``symbol=AAPL,SPY,AMD``
This endpoint is updated real-time.

## Minimum Subscription
`value`

## History Access
`true`

## Parameters
*   [[../parameters/request-type.md|request_type]] (Required)
*   [[../parameters/opt-multi-symbol.md|symbol]] (Optional)
*   [[../parameters/date.md|date]] (Required)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** List all contracts for an option trade with a given date

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

**Example (application/json):**
```json
{
  "response": [
    {"symbol":"ABNB","strike":260.000,"expiration":"2023-06-16","right":"CALL"},
    {"symbol":"AAPL","strike":260.000,"expiration":"2023-06-16","right":"CALL"},
    {"symbol":"AAL","strike":14.500,"expiration":"2022-09-30","right":"CALL"},
    {"symbol":"ABNB","strike":80.000,"expiration":"2022-11-04","right":"PUT"},
    {"symbol":"AAPL","strike":80.000,"expiration":"2022-11-04","right":"PUT"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_contracts(request_type='trade', date=date(2022, 9, 30))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_list_contracts(request_type='trade', date=date(2022, 9, 30))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]