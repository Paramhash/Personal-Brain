---
tags: ["market-data", "trading", "api", "sessions", "real-time"]
created: 2023-10-27
reviewed: false
source_origin: "market-sessions.md"
---
# Market State

Market state refers to the current operational status of a financial market at any given time. This status indicates whether the market is actively trading, closed, or in a pre- or post-market phase. Understanding the market state is vital for making informed trading decisions and for the correct functioning of automated trading systems.

The [[../concepts/market-sessions.md|Tastyworks Market Sessions API]] provides the current market state through its `state` field within the [[../concepts/currentsession-data-model.md|CurrentSession]] object.

## Common Market States
*   **Open:** The regular trading session is active.
*   **Closed:** The market is fully closed for trading.
*   **Pre-Market:** The period before the regular trading session opens, where some trading may occur (e.g., for equities).
*   **After-Hours:** The period after the regular trading session closes, where some trading may occur (e.g., for equities, also known as [[../concepts/extended-hours-trading.md|extended hours]]).

## API Endpoints for Market State
*   **Get Current Sessions (Multi-Collection):** `GET /market-time/sessions/current`
    *   Provides the `state` for multiple [[../concepts/instrument-collections.md|instrument collections]].
*   **Get Current Equities Session:** `GET /market-time/equities/sessions/current`
    *   Specifically for the `Equity` instrument collection.
*   **Get Current Futures Session by Exchange:** `GET /market-time/futures/sessions/current/{instrument_collection}`
    *   For specific futures exchanges like [[../entities/cme-group.md|CME]] or [[../entities/cboe-futures-exchange.md|CFE]].

## Use Cases
*   Displaying real-time market status in a trading application.
*   Implementing logic to prevent order submission when the market is closed.
*   Triggering specific trading strategies based on market phase (e.g., pre-market analysis).

## Related Notes
*   [[../concepts/market-sessions.md|Market Sessions]]
*   [[../concepts/currentsession-data-model.md|CurrentSession Data Model]]
*   [[../concepts/extended-hours-trading.md|Extended Hours Trading]]
*   [[../concepts/instrument-collections.md|Instrument Collections]]
*   [[../concepts/api-endpoints.md|API Endpoints]]