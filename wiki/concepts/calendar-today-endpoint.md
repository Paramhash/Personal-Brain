---
tags: ["Calendar", "Single Day", "Market Schedule"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Calendar Today Endpoint

The `/calendar/today` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API provides the current day's equity market schedule. This allows users to quickly determine if the market is open, closed, or has an early close on the present day.

## Endpoint Details:
*   **Path**: `/calendar/today`
*   **Method**: `GET`
*   **Summary**: Today
*   **Operation ID**: `calendar_open_today`
*   **Minimum Subscription**: `free`
*   **Description**:
    *   Retrieves the current day's equity market schedule.
    *   On days when the market closes early at 1:00 PM ET, eligible options will trade until 1:15 PM.
    *   Some NYSE exchanges will continue late trading until 5:00 PM ET on early close days.

## Parameters:
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns the current day's schedule.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `type`: The schedule type (`open`, `full_close`, `early_close`, `weekend`).
        *   `open`: Market open time in HH:mm:ss format.
        *   `close`: Market close time in HH:mm:ss format.

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.calendar_open_today()
```

## Related Concepts:
*   [Market Calendar](../concepts/market-calendar.md)
*   [Calendar On Date Endpoint](../concepts/calendar-on-date-endpoint.md)
*   [Calendar Year Holidays Endpoint](../concepts/calendar-year-holidays-endpoint.md)

---