---
tags: ["market-data", "trading", "holidays", "scheduling", "market-closure"]
created: 2023-10-27
reviewed: false
source_origin: "market-sessions.md"
---
# Trading Holidays

Trading holidays are specific days when financial markets are closed, either for the entire day (full holiday) or for a portion of the day (half-day, early close). These closures are typically due to national holidays or other significant events. Understanding and accounting for trading holidays is crucial for anyone involved in financial markets, especially for automated trading systems and order management.

The [[../concepts/market-sessions.md|Tastyworks Market Sessions API]] provides dedicated endpoints to retrieve holiday schedules for different [[../concepts/instrument-collections.md|instrument collections]]:

*   **Equities Holidays:** `GET /market-time/equities/holidays`
    *   Returns the US equity market holiday calendar, including full holidays and half days.
*   **Futures Holidays by Exchange:** `GET /market-time/futures/holidays/{instrument_collection}`
    *   Returns the holiday calendar for a specific futures exchange (e.g., [[../entities/cme-group.md|CME]], [[../entities/cboe-futures-exchange.md|CFE]]).

The holiday information is returned using the [[../concepts/marketcalendar-data-model.md|MarketCalendar data model]], which maps dates to full market holidays and half days.

## Importance
*   **Preventing Order Submission Errors:** Avoid submitting orders when markets are closed, which can lead to rejections or unexpected behavior.
*   **Accurate Scheduling:** Plan automated trading strategies and alerts to respect market closures.
*   **Risk Management:** Be aware of potential liquidity changes or market volatility around holiday periods.

## Related Notes
*   [[../concepts/market-sessions.md|Market Sessions]]
*   [[../concepts/marketcalendar-data-model.md|MarketCalendar Data Model]]
*   [[../concepts/instrument-collections.md|Instrument Collections]]
*   [[../concepts/api-endpoints.md|API Endpoints]]