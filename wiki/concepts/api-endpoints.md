---
tags: ["API", "Endpoints", "Financial Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# API Endpoints

The [Theta Data v3](../entities/theta-data-v3.md) API is structured around various endpoints, each designed to provide specific types of financial market data. These endpoints are categorized by the asset class they serve (Stocks, Options, Indices, Calendar, Interest Rates) and further by the type of data they deliver (List, Snapshot, History, At-Time).

## Endpoint Categories:

*   **[Stock Data Endpoints](../concepts/stock-data.md)**:
    *   List: `stock/list/symbols`, `stock/list/dates/{request_type}`
    *   Snapshot: `stock/snapshot/ohlc`, `stock/snapshot/trade`, `stock/snapshot/quote`, `stock/snapshot/market_value`
    *   History: `stock/history/eod`, `stock/history/ohlc`, `stock/history/trade`, `stock/history/quote`, `stock/history/trade_quote`
    *   At-Time: `stock/at_time/trade`, `stock/at_time/quote`

*   **[Option Data Endpoints](../concepts/option-data.md)**:
    *   List: `option/list/symbols`, `option/list/dates/{request_type}`, `option/list/expirations`, `option/list/strikes`, `option/list/contracts/{request_type}`
    *   Snapshot: `option/snapshot/ohlc`, `option/snapshot/trade`, `option/snapshot/quote`, `option/snapshot/open_interest`, `option/snapshot/market_value`, `option/snapshot/greeks/implied_volatility`, `option/snapshot/greeks/all`, `option/snapshot/greeks/first_order`, `option/snapshot/greeks/second_order`, `option/snapshot/greeks/third_order`
    *   History: `option/history/eod`, `option/history/ohlc`, `option/history/trade`, `option/history/quote`, `option/history/trade_quote`, `option/history/open_interest`, `option/history/greeks/eod`, `option/history/greeks/all`, `option/history/greeks/first_order`, `option/history/greeks/second_order`, `option/history/greeks/third_order`, `option/history/trade_greeks/all`, `option/history/trade_greeks/first_order`, `option/history/trade_greeks/second_order`, `option/history/trade_greeks/third_order`, `option/history/greeks/implied_volatility`, `option/history/trade_greeks/implied_volatility`
    *   At-Time: `option/at_time/trade`, `option/at_time/quote`

*   **[Index Data Endpoints](../concepts/index-data.md)**:
    *   List: `index/list/symbols`, `index/list/dates`
    *   Snapshot: `index/snapshot/ohlc`, `index/snapshot/price`, `index/snapshot/market_value`
    *   History: `index/history/eod`, `index/history/ohlc`, `index/history/price`
    *   At-Time: `index/at_time/price`

*   **[Market Calendar Endpoints](../concepts/market-calendar.md)**:
    *   `calendar/today`, `calendar/on_date`, `calendar/year_holidays`

*   **[Interest Rates Endpoints](../concepts/interest-rates.md)**:
    *   History: `interest_rate/history/eod`

Each endpoint is designed to be intuitive, with clear summaries, descriptions, and code samples to aid integration. Parameters are consistently defined and reused across relevant endpoints.

## Common Concepts:
*   [API Parameters](../concepts/api-parameters.md)
*   [Data Formats](../concepts/data-formats.md)
*   [Time Intervals](../concepts/time-intervals.md)
*   [Subscription Tiers](../concepts/subscription-tiers.md)

---