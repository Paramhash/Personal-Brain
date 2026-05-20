---
tags: ["market-data", "historic-data", "candles", "dxlink", "streaming"]
created: 2024-07-30
reviewed: false
source_origin: "streaming-market-data.md"
---
# Candle Events (DXLink Historic Data)

[[../entities/dxlink.md|DXLink]] supports subscribing to `Candle` events, which represent aggregated quote data over a specified duration (e.g., 5 minutes, 1 hour, 1 day). Each candle event includes fields such as `open`, `close`, `high`, and `low` for that period.

## Subscription Requirements

To subscribe to candle events for a symbol, you need to provide:

1.  **Symbol with Period and Type**: The symbol must be formatted to include a `period` (multiplier) and a `type` (unit of time).
    *   **Type**: Represents the unit of time (e.g., `m` for minutes, `h` for hours, `d` for days).
    *   **Period**: A multiplier for the type (e.g., `5` for 5 minutes, `1` for 1 hour).
    *   **Format**: `SYMBOL{=periodType}` (e.g., `AAPL{=5m}` for 5-minute candles of AAPL).
    *   Refer to DXFeed's guidelines for generating candle symbols correctly.
2.  **`fromTime` Timestamp**: An integer in Unix epoch time format, specifying the start time for fetching historical data. DXLink will provide all candles from this point up to the current moment; there is no way to set an end time.

## Candle Event Fields

For a candle event covering a specific duration:
*   **`open`**: Price at the start of the candle duration.
*   **`close`**: Price at the end of the candle duration.
*   **`high`**: Highest price hit during the candle duration.
*   **`low`**: Lowest price hit during the candle duration.

## "Live" Candle Data

The most recent candle event received is considered the "live" candle. This event will update constantly as the quote changes within the current period. For example, for `AAPL{=5m}` at 12:51, the "live" candle event would have a timestamp of 12:50, and its `close` value would update until 12:55, when a new 12:55 candle event becomes "live."

## Recommendations for Historical Data

Requesting too many candles can lead to millions of events, potentially overwhelming the client. It is recommended to use larger time intervals for data further back in time.

| Time Back | Recommended Type | Example    | Notes                                    |
| :-------- | :--------------- | :--------- | :--------------------------------------- |
| 1 day     | 1 Minute         | `AAPL{=1m}` | Returns around 1440 candle events        |
| 1 week    | 5 Minutes        | `AAPL{=5m}` | Returns around 2016 candle events        |
| 1 month   | 30 Minutes       | `AAPL{=30m}` | Returns around 1440 candle events        |
| 3 months  | 1 hour           | `AAPL{=1h}` | Returns around 2160 candle events        |
| 6 months  | 2 hours          | `AAPL{=2h}` | Returns around 2160 candle events        |
| 1 year+   | 1 day            | `AAPL{=1d}` | Returns around 365 candle events         |

## Code Examples (tastytrade TypeScript SDK)

Assuming `dxLinkFeed` is an instance of `DXLinkFeed` from the DXLink JavaScript SDK.

### 5-minute candles for the past 24 hours

```typescript
const date = new Date();
date.setDate(date.getDate() - 1); // Set date to 1 day ago
dxLinkFeed.addSubscriptions({ type: 'Candle', symbol: 'AAPL{=5m}', fromTime: date.getTime() });
```

### 30-minute candles for the past 30 days

```typescript
const date = new Date();
date.setDate(date.getDate() - 30); // Set date to 30 days ago
dxLinkFeed.addSubscriptions({ type: 'Candle', symbol: 'AAPL{=30m}', fromTime: date.getTime() });
```

### 60-minute candles for the past 3 months

```typescript
const date = new Date();
date.setDate(date.getDate() - 90); // Set date to 90 days ago
dxLinkFeed.addSubscriptions({ type: 'Candle', symbol: 'AAPL{=1h}', fromTime: date.getTime() });
```

## Related Concepts

*   [[../concepts/streaming-market-data.md|Streaming Market Data (tastytrade & DXLink)]]
*   [[../entities/dxlink.md|DXLink]]
*   [[../concepts/dxlink-market-data-events.md|DXLink Market Data Events]]