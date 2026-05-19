---
tags: ["option", "list", "symbols", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Symbols

## Summary
Symbols

## Operation ID
`option_list_symbols`

## Description
A symbol can be defined as a unique identifier for a stock / underlying asset. Common terms also include: root, ticker, and underlying. This endpoint returns all traded symbols for options. This endpoint is updated overnight.

## Minimum Subscription
`free`

## Parameters
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** List all symbols for options

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `symbol` (string): The symbol of the contract, or stock / underlying asset / option / index.

**Example (application/json):**
```json
{
  "response": [
    {"symbol":"A"},
    {"symbol":"AA"},
    {"symbol":"AAAP"},
    {"symbol":"AAAU"},
    {"symbol":"AABA"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_symbols()
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.option_list_symbols()
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]