---
tags: ["api", "rest", "web-services", "integration", "programming"]
created: 2023-10-27
reviewed: false
source_origin: "market-sessions.md"
---
# API Endpoints

API endpoints are specific URLs that represent distinct functions or resources within a web service. They define the entry points for client applications to interact with the API, typically using HTTP methods (GET, POST, PUT, DELETE) to perform operations.

The [[../concepts/market-sessions.md|Tastyworks Market Sessions API]] provides a structured set of endpoints for retrieving market session information. These endpoints are organized to allow for general queries, as well as specific queries tailored to equities and futures markets.

## General Endpoints
*   `GET /market-time/sessions`: Retrieve session timings for a date range.
*   `GET /market-time/sessions/current`: Retrieve current session timings for multiple [[../concepts/instrument-collections.md|instrument collections]].

## Equities Endpoints
These endpoints focus specifically on the `Equity` instrument collection, covering markets like [[../entities/nyse.md|NYSE]] and [[../entities/nasdaq.md|NASDAQ]].
*   `GET /market-time/equities/sessions/current`: Get the current equities market session.
*   `GET /market-time/equities/sessions/next`: Get the next equities trading session.
*   `GET /market-time/equities/sessions/previous`: Get the most recent past equities trading session.
*   `GET /market-time/equities/holidays`: Get the equity market [[../concepts/trading-holidays.md|holiday calendar]].

## Futures Endpoints
These endpoints are designed for futures markets, supporting specific exchanges like [[../entities/cme-group.md|CME]] and [[../entities/cboe-futures-exchange.md|CFE]].
*   `GET /market-time/futures/sessions/current`: Get current sessions for all futures exchanges.
*   `GET /market-time/futures/sessions/current/{instrument_collection}`: Get current session for a specific futures exchange.
*   `GET /market-time/futures/sessions/next/{instrument_collection}`: Get next futures trading session for a specific exchange.
*   `GET /market-time/futures/sessions/previous/{instrument_collection}`: Get previous futures trading session for a specific exchange.
*   `GET /market-time/futures/holidays/{instrument_collection}`: Get the [[../concepts/trading-holidays.md|holiday calendar]] for a specific futures exchange.

## Common Parameters
Many endpoints utilize query parameters such as `to-date`, `from-date`, `instrument-collection`, and `date` to filter or specify the requested data. Path parameters like `{instrument_collection}` are used for exchange-specific queries.

## Responses
Responses typically return [[../concepts/data-models.md|data models]] like [[../concepts/simplesession-data-model.md|SimpleSession]], [[../concepts/currentsession-data-model.md|CurrentSession]], [[../concepts/nextsession-data-model.md|NextSession]], [[../concepts/previoussession-data-model.md|PreviousSession]], or [[../concepts/marketcalendar-data-model.md|MarketCalendar]], depending on the endpoint.

## Related Notes
*   [[../concepts/market-sessions.md|Market Sessions]]
*   [[../concepts/data-models.md|Data Models]]
*   [[../concepts/instrument-collections.md|Instrument Collections]]
*   [[../concepts/trading-holidays.md|Trading Holidays]]
*   [[../sources/tastyworks-market-sessions-api-docs.md|Tastyworks Market Sessions API Documentation]]