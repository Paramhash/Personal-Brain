---
tags: ["option", "list", "dates", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option List Dates

## Summary
Dates

## Operation ID
`option_list_dates`

## Description
Lists all dates of data that are available for an option with a given symbol, request type, and expiration.
This endpoint is updated overnight.

## Minimum Subscription
`free`

## Parameters
*   [[../parameters/request-type.md|request_type]] (Required)
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration-no-star.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/format.md|format]] (Optional)

## Responses

### 200 OK
**Description:** List all dates for an option quote for a given symbol and expiration date

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
    {"date":"2022-09-12"},
    {"date":"2022-09-13"},
    {"date":"2022-09-14"},
    {"date":"2022-09-16"},
    {"date":"2022-09-19"}
  ]
}
```

## Code Samples

### Python (pandas)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.option_list_dates(
    request_type='quote',
    symbol='AAPL',
    expiration=date(2022, 9, 30),
)
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_list_dates(
    request_type='quote',
    symbol='AAPL',
    expiration=date(2022, 9, 30),
)
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]