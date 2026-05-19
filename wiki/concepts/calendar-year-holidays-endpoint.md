---
tags: ["Calendar", "Year", "Holidays", "Market Schedule"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Calendar Year Holidays Endpoint

The `/calendar/year_holidays` endpoint of the [Theta Data v3](../../entities/theta-data-v3.md) API allows users to retrieve a list of equity market holidays for a specified year. This is useful for planning and understanding market closures in advance.

## Endpoint Details:
*   **Path**: `/calendar/year_holidays`
*   **Method**: `GET`
*   **Summary**: Year Holidays
*   **Operation ID**: `calendar_year`
*   **Minimum Subscription**: `value`
*   **Description**:
    *   Retrieves equity market holidays for a given year.
    *   Holiday data is available from 01/01/2012 through the end of the calendar year that immediately follows the current year.
    *   On days when the market closes early at 1:00 PM ET, eligible options will trade until 1:15 PM.
    *   Some NYSE exchanges will continue late trading until 5:00 PM ET on early close days.

## Parameters:
*   `year` (Required): The year to fetch data for. See [API Parameters](../../concepts/api-parameters.md#year).
*   `format` (Optional): The format of the data when returned to the user. See [API Parameters](../../concepts/api-parameters.md#format) and [Data Formats](../../concepts/data-formats.md).

## Responses:
*   **200 OK**: Returns holidays for a given year.
    *   **Content**: `text/csv`, `application/json`, `application/x-ndjson`, `python/pandas`, `python/polars`
    *   **Schema**: An array of objects, each with:
        *   `date`: The date of a closure.
        *   `type`: The closure type (`full_close`, `early_close`).
        *   `open`: Market open time in HH:mm:ss format (or null if full_close).
        *   `close`: Market close time in HH:mm:ss format (or null if full_close).

## Example (Python - pandas):
```python
from thetadata import ThetaClient

client = ThetaClient(dataframe_type='pandas')
df = client.calendar_year(year='2024')
```

## Related Concepts:
*   [Market Calendar](../concepts/market-calendar.md)
*   [Calendar Today Endpoint](../concepts/calendar-today-endpoint.md)
*   [Calendar On Date Endpoint](../concepts/calendar-on-date-endpoint.md)

---