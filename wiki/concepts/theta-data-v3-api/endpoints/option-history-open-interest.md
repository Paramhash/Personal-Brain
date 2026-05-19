---
tags: ["option", "history", "open-interest", "api-endpoint"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Option History Open Interest

## Summary
Open Interest

## Operation ID
`option_history_open_interest`

## Description
- Open Interest is normally reported once per day by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) at approximately 06:30 ET.
- A new open interest message might not be sent by [OPRA](/Articles/Data-And-Requests/The-SIPs.html) if there is no open interest for the option contract.
- The reported open interest represents the open interest at the end of the previous trading day.

## Minimum Subscription
`value`

## History Access
`true`

## Parameters
*   [[../parameters/opt-date.md|date]] (Optional)
*   [[../parameters/single-symbol.md|symbol]] (Required)
*   [[../parameters/expiration.md|expiration]] (Required)
*   [[../parameters/strike.md|strike]] (Optional)
*   [[../parameters/right.md|right]] (Optional)
*   [[../parameters/max-dte.md|max_dte]] (Optional)
*   [[../parameters/strike-range.md|strike_range]] (Optional)
*   [[../parameters/format.md|format]] (Optional)
*   [[../parameters/opt-start-date.md|start_date]] (Optional)
*   [[../parameters/opt-end-date.md|end_date]] (Optional)

## Responses

### 200 OK
**Description:** Returns open interest for an option contract

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
        *   `open_interest` (integer): The total amount of outstanding contracts.

**Example (application/json):**
```json
{
  "response": [
    {
      "contract": {"symbol":"AAPL","strike":220.000,"right":"CALL","expiration":"2024-11-08"},
      "data": [
        {"open_interest":2732,"timestamp":"2024-11-04T06:30:04"}
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
df = client.option_history_open_interest(symbol='AAPL', expiration=date(2024, 11, 8))
```

### Python (polars)
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.option_history_open_interest(symbol='AAPL', expiration=date(2024, 11, 8))
```

---
[[../../entities/theta-data-v3-api.md|Back to Theta Data v3 API Overview]]