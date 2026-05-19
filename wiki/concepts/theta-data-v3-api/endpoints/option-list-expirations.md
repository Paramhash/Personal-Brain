---
tags: ["option", "list", "expirations", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Expirations

## Summary
Expirations

## Operation ID
`option_list_expirations`

## Description
Lists all dates of expirations that are available for an option with a given symbol.
This endpoint is updated overnight.

## Minimum Subscription
`free`

## Parameters
*   [[../parameters/multi-symbol.md|symbol]] (Required)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** List all expirations for an option with a given symbol

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.
        *   `expiration` (string, format: `date`): Expiration date of the contract in YYYY-MM-DD format.

**Example (application/json):**
```json
{
  "response": [
    {"symbol":"AAPL","expiration":"2012-06-01"},
    {"symbol":"AAPL","expiration":"2012-06-08"},
    {"symbol":"AAPL","expiration":"2012-06-16"},
    {"symbol":"AAPL","expiration":"2012-06-22"},
    {"symbol":"AAPL","expiration":"2012-06-29"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_expirations(symbol=['AAPL'])
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.option_list_expirations(symbol=['AAPL'])
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]