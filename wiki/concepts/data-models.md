---
tags: ["api", "data-structure", "json", "schema", "programming"]
created: 2023-10-27
reviewed: false
source_origin: "market-sessions.md"
---
# Data Models

Data models define the structure and format of the information exchanged between a client and an API. They ensure consistency and predictability in API responses, making it easier for developers to parse and utilize the data.

The [[../concepts/market-sessions.md|Tastyworks Market Sessions API]] uses several specific data models to represent market session information, holidays, and market states. All timestamps within these models are in [[../concepts/utc-timestamps.md|UTC]].

## Common Session Time Fields
Most session-related data models share a common set of fields describing session timings:
*   `start-at` (datetime): The absolute start time of the session (e.g., pre-market open for equities, overnight session open for futures).
*   `open-at` (datetime): The regular market open time (e.g., 9:30 AM ET for equities).
*   `close-at` (datetime): The regular market close time (e.g., 4:00 PM ET for equities).
*   `close-at-ext` (datetime): The [[../concepts/extended-hours-trading.md|extended-hours]] close time (e.g., 8:00 PM ET for equities after-hours).
*   `instrument-collection` (string): The [[../concepts/instrument-collections.md|instrument collection]] this session belongs to.

## Specific Data Models
*   [[../concepts/simplesession-data-model.md|SimpleSession]]: Used for retrieving basic session timings over a date range.
*   [[../concepts/currentsession-data-model.md|CurrentSession]]: Provides detailed information about the current session, including its [[../concepts/market-state.md|market state]] and nested next/previous session details.
*   [[../concepts/nextsession-data-model.md|NextSession]]: Details about an upcoming trading session.
*   [[../concepts/previoussession-data-model.md|PreviousSession]]: Details about a past trading session.
*   [[../concepts/marketcalendar-data-model.md|MarketCalendar]]: Contains information about [[../concepts/trading-holidays.md|market holidays]] and half-days.

## Related Notes
*   [[../concepts/market-sessions.md|Market Sessions]]
*   [[../concepts/api-endpoints.md|API Endpoints]]
*   [[../concepts/utc-timestamps.md|UTC Timestamps]]
*   [[../concepts/extended-hours-trading.md|Extended Hours Trading]]
*   [[../concepts/instrument-collections.md|Instrument Collections]]
*   [[../concepts/market-state.md|Market State]]
*   [[../concepts/trading-holidays.md|Trading Holidays]]
*   [[../sources/tastyworks-market-sessions-api-docs.md|Tastyworks Market Sessions API Documentation]]