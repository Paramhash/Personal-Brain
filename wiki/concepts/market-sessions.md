---
tags: ["trading", "market-data", "api", "tastyworks", "sessions", "market-hours", "fintech"]
created: 2023-10-27
reviewed: false
source_origin: "market-sessions.md"
---
# Market Sessions

Market sessions refer to the specific periods during which financial markets are open for trading. Understanding these sessions is crucial for traders and automated systems to ensure orders are submitted at appropriate times and to account for [[../concepts/trading-holidays.md|trading holidays]] or [[../concepts/extended-hours-trading.md|extended hours]].

The Tastyworks Market Sessions API provides programmatic access to this information, offering endpoints to determine market open/close times, current [[../concepts/market-state.md|market state]], and trading holidays across various [[../concepts/instrument-collections.md|instrument collections]].

## Key Features
*   **Session Timings:** Retrieve `start-at`, `open-at`, `close-at`, and `close-at-ext` (extended hours close) for various sessions.
*   **Market State:** Get the current state of a market (e.g., `Open`, `Closed`, `Pre-Market`, `After-Hours`).
*   **Trading Holidays:** Access calendars for full market holidays and half-days.
*   **Multi-Collection Support:** Query sessions for Equities, CME, CFE, and Zero Hash CLOB markets.
*   **Timezone:** All timestamps are provided in [[../concepts/utc-timestamps.md|UTC]].

## API Details
*   **Provider:** [[../entities/tastyworks.md|Tastyworks]]
*   **Base URL:** `https://api.tastyworks.com/market-time`
*   **Authentication:** Requires a valid session token in the `Authorization` header.

## Endpoints
The API offers a range of [[../concepts/api-endpoints.md|endpoints]] categorized by general, equities-specific, and futures-specific queries. These include:
*   `GET /sessions`: Retrieve sessions for a date range.
*   `GET /sessions/current`: Get current sessions for multiple instrument collections.
*   `GET /equities/sessions/current`: Get current equities session.
*   `GET /equities/holidays`: Get equity market holidays.
*   `GET /futures/sessions/current/{instrument_collection}`: Get current futures session for a specific exchange.

## Data Models
The API returns data using several [[../concepts/data-models.md|data models]], including:
*   [[../concepts/simplesession-data-model.md|SimpleSession]]
*   [[../concepts/currentsession-data-model.md|CurrentSession]]
*   [[../concepts/nextsession-data-model.md|NextSession]]
*   [[../concepts/previoussession-data-model.md|PreviousSession]]
*   [[../concepts/marketcalendar-data-model.md|MarketCalendar]]

## Common Use Cases
*   Gating order submission based on market open/close.
*   Displaying real-time market status in user interfaces.
*   Scheduling automated trading activities around market hours and holidays.
*   Understanding specific session times for different futures exchanges.

## Important Notes
*   Futures markets often trade nearly 24 hours with short daily breaks.
*   The date range for session queries is limited to 9 months.
*   `close-at-ext` is relevant for orders with `time-in-force` of `Ext`.

## Related Notes
*   [[../sources/tastyworks-market-sessions-api-docs.md|Tastyworks Market Sessions API Documentation]]
*   [[../concepts/instrument-collections.md|Instrument Collections]]
*   [[../concepts/trading-holidays.md|Trading Holidays]]
*   [[../concepts/market-state.md|Market State]]
*   [[../concepts/api-endpoints.md|API Endpoints]]
*   [[../concepts/data-models.md|Data Models]]
*   [[../concepts/utc-timestamps.md|UTC Timestamps]]
*   [[../concepts/extended-hours-trading.md|Extended Hours Trading]]
*   [[../entities/tastyworks.md|Tastyworks]]
*   [[../entities/nyse.md|NYSE]]
*   [[../entities/nasdaq.md|NASDAQ]]
*   [[../entities/cme-group.md|CME Group]]
*   [[../entities/cboe-futures-exchange.md|Cboe Futures Exchange]]
*   [[../entities/zero-hash-clob.md|Zero Hash CLOB]]