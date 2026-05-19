---
tags: ["Calendar", "Single Day", "Market Schedule"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Calendar On Date Endpoint

The `/calendar/on_date` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve the equity market schedule for a specific date. This is useful for understanding if the market is open, fully closed, or has an early close on a given day.

## Endpoint Details:
*   **Path**: `/calendar/on_date`
*   **Method**: `GET`
*   **Summary**: On Date
*   **Operation ID**: `calendar_on_date`
*   **Minimum Subscription**: `value`
*   **Description**:
    *   Retrieves the equity market schedule for a given date.
    *   Holiday data is available from 01/01/2012 through the end of the calendar year that immediately follows the current year.
    *   On days when the market closes early at 1:00 PM ET, eligible options will trade until 1:15 PM.
    *   Some NYSE exchanges will continue late trading until 5:00 PM ET on early close days.

## Parameters:
*   `date` (Required): The date to fetch data for (YYYYMMDD format). See [API Parameters](../../concepts/api-parameters.md#date).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns the requested day's schedule.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `type`: The schedule type (`open`, `full_close`, `early_close`, `weekend`).
        *   `open`: Market open time in HH:mm:ss format (or null if closed).
        *   `close`: Market close time in HH:mm:ss format (or null if closed).

## Example (Python - pandas):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.calendar_on_date(date=date(2025, 12, 25))
```

## Related Concepts:
*   [Market Calendar](../concepts/market-calendar.md)
*   [Calendar Today Endpoint](../concepts/calendar-today-endpoint.md)
*   [Calendar Year Holidays Endpoint](../concepts/calendar-year-holidays-endpoint.md)

---