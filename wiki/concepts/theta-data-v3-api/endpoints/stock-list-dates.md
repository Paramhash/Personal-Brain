---
tags: ["stock", "list", "dates", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Stock List Dates

## Summary
Dates

## Operation ID
`stock_list_dates`

## Description
Lists all dates of data that are available for a stock with a given request type and symbol. This endpoint is updated overnight.

## Minimum Subscription
`free`

## Parameters
*   [[../parameters/request-type.md|request_type]] (Required)
*   [[../parameters/multi-symbol.md|symbol]] (Required)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** List all dates for a stock quote for a given symbol

**Content Types:** `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`

**Schema (Common for all content types):**
Type: `array`
Items:
    Type: `object`
    Properties:
        *   `date` (string, format: `date`): The date formated as YYYY-MM-DD.

**Example (application/json):**
```json
{
  "response": [
    {"date": "2016-08-16"},
    {"date": "2016-08-17"},
    {"date": "2016-08-18"},
    {"date": "2016-08-19"},
    {"date": "2016-08-23"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.stock_list_dates(request_type='quote', symbol=['AAPL'])
```

### Python (polars)
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='polars')
df = client.stock_list_dates(request_type='quote', symbol=['AAPL'])
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]