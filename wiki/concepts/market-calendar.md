---
tags: ["Market Schedule", "Holidays", "Trading Hours"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Market Calendar

The market calendar provides essential information about trading days, holidays, and special trading hours for equity markets. The [Theta Data v3](../../entities/theta-data-v3.md) API offers endpoints to retrieve this information, which is crucial for scheduling data requests and understanding market behavior.

## Key Characteristics:
*   **Holiday Data**: Available from 01/01/2012 through the end of the calendar year that immediately follows the current year.
*   **Early Close Days**: On days when the market closes early (e.g., 1:00 PM ET), eligible options may trade for an extended period (e.g., until 1:15 PM). Some NYSE exchanges might also have late trading until 5:00 PM ET.
*   **Schedule Types**: Responses indicate the type of market day: `open`, `full_close`, `early_close`, or `weekend`.

## Available Endpoints:

### Single Day Endpoints:
*   **[Calendar Today Endpoint](../concepts/calendar-today-endpoint.md)**: Retrieves the current day's equity market schedule.
*   **[Calendar On Date Endpoint](../concepts/calendar-on-date-endpoint.md)**: Retrieves the equity market schedule for a specific, user-defined date.

### Year Endpoints:
*   **[Calendar Year Holidays Endpoint](../concepts/calendar-year-holidays-endpoint.md)**: Retrieves a list of equity market holidays for a given year.

## Related Concepts:
*   [API Endpoints](../concepts/api-endpoints.md)
*   [API Parameters](../concepts/api-parameters.md)

---