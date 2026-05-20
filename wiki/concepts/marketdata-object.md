---
tags: ["data-model", "api", "market-data"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# MarketData Object

The `MarketData` object is the primary data structure returned by the [[Market Data API (Tastyworks)|Tastyworks Market Data API]]. It provides a comprehensive, point-in-time snapshot of market data for a single instrument.

## Structure and Fields

### Identification
*   `symbol` (string): The instrument symbol.
*   `instrumentType` (string): The [[Market Data Instrument Types|instrument type]] (e.g., `Equity`, `Equity Option`).
*   `updatedAt` (datetime): Timestamp of the last update.
*   `instrument` ([[Instrument Object|Instrument]]): Nested details about the instrument.

### Quote Data
*   `bid` (number): Current best bid price.
*   `bidSize` (number): Size at the best bid.
*   `ask` (number): Current best ask price.
*   `askSize` (number): Size at the best ask.
*   `mid` (number): Midpoint price `(bid + ask) / 2`.
*   `mark` (number): Mark price (exchange-calculated or mid).
See [[Quote Data]] for more details.

### Last Trade
*   `last` (number): Last trade price (regular hours).
*   `lastExt` (number): Last trade price (extended hours).
*   `lastMkt` (number): Last market trade price.
*   `lastTradeTime` (integer): Timestamp of last trade (epoch milliseconds).
*   `volume` (number): Total trading volume for the session.

### Day Session Prices
*   `open` (number): Session opening price.
*   `dayHighPrice` (number): Session high price.
*   `dayLowPrice` (number): Session low price.
*   `close` (number): Session closing price.
*   `prevClose` (number): Previous session's close price.
*   `summaryDate` (date): Date of this session's summary data.
*   `prevCloseDate` (date): Date of the previous close.

### Annual Range
*   `yearHighPrice` (number): 52-week high price.
*   `yearLowPrice` (number): 52-week low price.

### Fundamental Data
*   `beta` (number): Beta coefficient.
*   `dividendAmount` (number): Current dividend amount.
*   `dividendFrequency` (number): Number of dividend payments per year.

### Trading Halts & Limits
*   `tradingHalted` (boolean): `true` if trading is currently halted for the instrument.
*   `tradingHaltedReason` (string): Reason for the halt.
*   `haltStartTime` (integer): Halt start time (epoch milliseconds).
*   `haltEndTime` (integer): Halt end time (epoch milliseconds).
*   `lowLimitPrice` (number): Lower circuit breaker limit.
*   `highLimitPrice` (number): Upper circuit breaker limit.
See [[Trading Halts]] for more details.

## Deprecated Fields
Several fields have been deprecated and replaced (e.g., `dayOpen` -> `open`).

## Related
*   [[Market Data API (Tastyworks)]]
*   [[Instrument Object]]
*   [[Quote Data]]
*   [[Trading Halts]]
*   [[Market Data Instrument Types]]