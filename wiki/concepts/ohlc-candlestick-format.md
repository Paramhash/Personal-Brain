---
tags: ["finance", "data-format", "charting", "technical-analysis"]
created: 2023-10-27
reviewed: false
source_origin: "net-liquidating-value-history.md"
---
# OHLC Candlestick Format

**OHLC** stands for **Open, High, Low, Close**. It is a common data format used in financial markets to represent price movements of an asset over a specific time interval (e.g., a minute, an hour, a day, a week).

Each OHLC "candle" or data point contains four key values:
*   **Open:** The price at which the asset first traded during the interval.
*   **High:** The highest price reached by the asset during the interval.
*   **Low:** The lowest price reached by the asset during the interval.
*   **Close:** The price at which the asset last traded during the interval.

This format is widely used for creating candlestick charts, which visually represent these four price points, providing insights into market sentiment and volatility within the given period.

APIs like the [tastytrade Net Liquidating Value History API](../entities/tastytrade-net-liquidating-value-history-api.md) utilize the OHLC format to provide historical data for metrics such as [Net Liquidating Value](../concepts/net-liquidating-value.md).