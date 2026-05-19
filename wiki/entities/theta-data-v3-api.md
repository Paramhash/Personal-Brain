---
tags: ["api", "financial-data", "stocks", "options", "indices"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Theta Data v3 API

The Theta Data v3 API provides real-time and historic stock, options, and index data. It offers a comprehensive suite of endpoints for listing symbols, retrieving historical data, and accessing real-time snapshots, including various Greeks calculations for options.

**Version:** 3.0.0
**Description:** Real-time and historic stock, options, and index data!
**Base URL (Development):** `http://127.0.0.1:25503/v3`

## Endpoint Categories

### Stock Endpoints
*   [[../concepts/theta-data-v3-api/endpoints/stock-list-symbols.md|Stock List Symbols]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-list-dates.md|Stock List Dates]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-snapshot-ohlc.md|Stock Snapshot Open High Low Close]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-snapshot-trade.md|Stock Snapshot Trade]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-snapshot-quote.md|Stock Snapshot Quote]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-snapshot-market-value.md|Stock Snapshot Market Value]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-history-eod.md|Stock History End of Day]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-history-ohlc.md|Stock History Open High Low Close]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-history-trade.md|Stock History Trade]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-history-quote.md|Stock History Quote]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-history-trade-quote.md|Stock History Trade Quote]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-at-time-trade.md|Stock At-Time Trade]]
*   [[../concepts/theta-data-v3-api/endpoints/stock-at-time-quote.md|Stock At-Time Quote]]

### Option Endpoints
*   [[../concepts/theta-data-v3-api/endpoints/option-list-symbols.md|Option List Symbols]]
*   [[../concepts/theta-data-v3-api/endpoints/option-list-dates.md|Option List Dates]]
*   [[../concepts/theta-data-v3-api/endpoints/option-list-expirations.md|Option List Expirations]]
*   [[../concepts/theta-data-v3-api/endpoints/option-list-strikes.md|Option List Strikes]]
*   [[../concepts/theta-data-v3-api/endpoints/option-list-contracts.md|Option List Contracts]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-ohlc.md|Option Snapshot Open High Low Close]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-trade.md|Option Snapshot Trade]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-quote.md|Option Snapshot Quote]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-open-interest.md|Option Snapshot Open Interest]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-market-value.md|Option Snapshot Market Value]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-greeks-implied-volatility.md|Option Snapshot Implied Volatility]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-greeks-all.md|Option Snapshot All Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-greeks-first-order.md|Option Snapshot First Order Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-greeks-second-order.md|Option Snapshot Second Order Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-snapshot-greeks-third-order.md|Option Snapshot Third Order Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-eod.md|Option History End of Day]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-ohlc.md|Option History Open High Low Close]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-trade.md|Option History Trade]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-quote.md|Option History Quote]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-trade-quote.md|Option History Trade Quote]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-open-interest.md|Option History Open Interest]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-greeks-eod.md|Option History End of Day Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-greeks-all.md|Option History All Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-greeks-first-order.md|Option History First Order Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-trade-greeks-first-order.md|Option History First Order Trade Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-greeks-second-order.md|Option History Second Order Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-trade-greeks-second-order.md|Option History Second Order Trade Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-greeks-third-order.md|Option History Third Order Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-history-trade-greeks-third-order.md|Option History Third Order Trade Greeks]]
*   [[../concepts/theta-data-v3-api/endpoints/option-at-time-trade.md|Option At-Time Trade]]
*   [[../concepts/theta-data-v3-api/endpoints/option-at-time-quote.md|Option At-Time Quote]]

### Index Endpoints
*   [[../concepts/theta-data-v3-api/endpoints/index-list-symbols.md|Index List Symbols]]
*   [[../concepts/theta-data-v3-api/endpoints/index-list-dates.md|Index List Dates]]
*   [[../concepts/theta-data-v3-api/endpoints/index-snapshot-ohlc.md|Index Snapshot Open High Low Close]]
*   [[../concepts/theta-data-v3-api/endpoints/index-snapshot-price.md|Index Snapshot Price]]
*   [[../concepts/theta-data-v3-api/endpoints/index-snapshot-market-value.md|Index Snapshot Market Value]]
*   [[../concepts/theta-data-v3-api/endpoints/index-history-eod.md|Index History End of Day]]
*   [[../concepts/theta-data-v3-api/endpoints/index-history-ohlc.md|Index History Open High Low Close]]
*   [[../concepts/theta-data-v3-api/endpoints/index-history-price.md|Index History Price]]
*   [[../concepts/theta-data-v3-api/endpoints/index-at-time-price.md|Index At-Time Price]]

### Calendar Endpoints
*   [[../concepts/theta-data-v3-api/endpoints/calendar-today.md|Calendar Today]]
*   [[../concepts/theta-data-v3-api/endpoints/calendar-on-date.md|Calendar On Date]]
*   [[../concepts/theta-data-v3-api/endpoints/calendar-year-holidays.md|Calendar Year Holidays]]

### Interest Rate Endpoints
*   [[../concepts/theta-data-v3-api/endpoints/interest-rate-history-eod.md|Interest Rate History End of Day]]

## API Parameters
For a detailed description of all reusable parameters, refer to the [[../concepts/theta-data-v3-api/api-parameters.md|Theta Data v3 API Parameters]] overview.