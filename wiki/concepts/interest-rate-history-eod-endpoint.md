---
tags: ["Interest Rate", "History", "End of Day"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Interest Rate History EOD Endpoint

The `/interest_rate/history/eod` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides historical End-of-Day (EOD) interest rate data for a specified symbol over a given date range.

## Endpoint Details:
*   **Path**: `/interest_rate/history/eod`
*   **Method**: `GET`
*   **Summary**: End of Day
*   **Operation ID**: `interest_rate_history_eod`
*   **Minimum Subscription**: `value`
*   **Description**:
    *   Returns the interest rate reported. Depending on the rate, reports can occur in the morning or the afternoon.

## Parameters:
*   `symbol` (Required): The interest rate symbol (e.g., SOFR). See [API Parameters](../../concepts/api-parameters.md#single-symbol) and [Symbols](../../concepts/symbols.md).
*   `start_date` (Required): The start date (inclusive). See [API Parameters](../../concepts/api-parameters.md#start-date).
*   `end_date` (Required): The end date (inclusive). See [API Parameters](../../concepts/api-parameters.md#end-date).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns the interest rate for a given symbol between specified dates (inclusive).
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `created`: The date formatted as YYYY-MM-DD.
        *   `rate`: The interest rate expressed as a percent (i.e., 1.25% is 1.25).

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.interest_rate_history_eod(
    symbol='SOFR',
    start_date=date(2025, 11, 4),
    end_date=date(2025, 11, 8),
)
```

## Related Concepts:
*   [Interest Rates](../concepts/interest-rates.md)
*   [API Endpoints](../concepts/api-endpoints.md)

---