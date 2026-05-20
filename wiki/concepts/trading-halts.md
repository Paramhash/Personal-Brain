---
tags: ["market-data", "trading", "regulation"]
created: 2023-10-27
reviewed: false
source_origin: "market-data.md"
---
# Trading Halts

A trading halt is a temporary suspension of trading for a specific security or market. Halts are typically imposed by exchanges for various reasons, such as pending news announcements, significant price volatility (circuit breakers), or technical issues.

The [[Market Data API (Tastyworks)|Tastyworks Market Data API]] provides specific fields within the [[MarketData Object]] to indicate and provide details about trading halts.

## Key Fields in MarketData Object
*   `tradingHalted` (boolean): `true` if trading is currently halted for the instrument.
*   `tradingHaltedReason` (string): A description of the reason for the halt.
*   `haltStartTime` (integer): The timestamp (epoch milliseconds) when the halt began.
*   `haltEndTime` (integer): The timestamp (epoch milliseconds) when the halt is expected to end.
*   `lowLimitPrice` (number): The lower price limit (circuit breaker, applicable to futures).
*   `highLimitPrice` (number): The upper price limit (circuit breaker, applicable to futures).

## Importance for Trading
Checking `tradingHalted` status is crucial before submitting orders to avoid rejections and ensure compliance with market rules.

## Related
*   [[MarketData Object]]
*   [[Market Data API (Tastyworks)]]