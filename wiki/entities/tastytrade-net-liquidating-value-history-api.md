---
tags: ["api", "tastytrade", "financial-data", "net-liquidating-value", "ohlc", "history"]
created: 2023-10-27
reviewed: false
source_origin: "net-liquidating-value-history.md"
---
# tastytrade Net Liquidating Value History API

The tastytrade Net Liquidating Value History API provides historical [net liquidating value (NLV)](../concepts/net-liquidating-value.md) snapshots for a given account in [OHLC (Open/High/Low/Close) candlestick format](../concepts/ohlc-candlestick-format.md). This API is crucial for charting account value over time, calculating portfolio performance metrics, and performing detailed financial analysis.

It is part of the broader [tastytrade API ecosystem](../entities/tastytrade.md).

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid [session token](../concepts/api-authentication.md#session-token) passed via the `Authorization` header.
**API Version:** v0

## Endpoints

### Get Net Liq History

Retrieves historical net liquidating value data for a specific tastytrade account. Data is returned in OHLC candlestick format, with each candle representing a defined time interval.

**Request**

```
GET /accounts/{accountNumber}/net-liq/history
```

**Path Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `accountNumber` | string | Yes | The tastytrade account number for which to retrieve history. |

**Query Parameters**

Users can specify either a relative `time-back` or an absolute `start-time`/`end-time` window.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `time-back` | string | No | Relative time lookback. Supported values include: `1d` (1 day), `1w` (1 week), `1m` (1 month), `3m` (3 months), `6m` (6 months), `1y` (1 year), `all` (all available history). |
| `start-time` | string | No | Absolute start time in [ISO 8601 zoned datetime format](../concepts/iso-8601.md) (e.g., `2026-01-01T00:00:00+00:00[UTC]`). |
| `end-time` | string | No | Absolute end time in the same [ISO 8601 zoned datetime format](../concepts/iso-8601.md). |
| `interval` | string | No | The time interval for each OHLC candle (e.g., `1d`, `1h`). |

**Response** — `200 OK`

Returns an array of `NetLiqOhlc` objects.

**Example Response**

```json
{
  "data": {
    "items": [
      {
        "open": 10250.50,
        "high": 10420.75,
        "low": 10180.30,
        "close": 10350.00,
        "totalOpen": 10250.50,
        "totalHigh": 10420.75,
        "totalLow": 10180.30,
        "totalClose": 10350.00,
        "pendingCashOpen": 0.0,
        "pendingCashHigh": 0.0,
        "pendingCashLow": 0.0,
        "pendingCashClose": 0.0,
        "time": "2026-04-09T00:00:00+00:00"
      }
    ]
  }
}
```

## Data Models

The API returns an array of `NetLiqOhlc` objects, each representing one OHLC candle of net liquidating value data for a specific time interval.

### NetLiqOhlc Object Structure

| Field | Type | Description |
|-------|------|-------------|
| `open` | number (double) | [Net liquidating value](../concepts/net-liquidating-value.md) at the open of the interval. |
| `high` | number (double) | Highest [net liquidating value](../concepts/net-liquidating-value.md) during the interval. |
| `low` | number (double) | Lowest [net liquidating value](../concepts/net-liquidating-value.md) during the interval. |
| `close` | number (double) | [Net liquidating value](../concepts/net-liquidating-value.md) at the close of the interval. |
| `time` | string | The timestamp for this candle, indicating the start or end of the interval. |
| `totalOpen` | number (double) | Total account value at open, including pending cash. |
| `totalHigh` | number (double) | Highest total account value during the interval, including pending cash. |
| `totalLow` | number (double) | Lowest total account value during the interval, including pending cash. |
| `totalClose` | number (double) | Total account value at close, including pending cash. |
| `pendingCashOpen` | number (double) | Pending cash value at the open of the interval. |
| `pendingCashHigh` | number (double) | Highest pending cash value during the interval. |
| `pendingCashLow` | number (double) | Lowest pending cash value during the interval. |
| `pendingCashClose` | number (double) | Pending cash value at the close of the interval. |

## Common Use Cases

*   **Portfolio Performance Charting:** Fetch a year of daily net-liq data (`time-back=1y`) and chart account value over time using the `close` value from each candle.
*   **Daily P&L Calculation:** Calculate daily profit/loss by comparing consecutive `close` values.
*   **Drawdown Analysis:** Utilize the `high` and `low` fields to determine maximum drawdown within intervals or across the entire dataset.
*   **Custom Date Range Analysis:** Use `start-time` and `end-time` parameters to analyze performance during specific market events or custom periods.

## Important Notes

*   **camelCase field names:** This endpoint uses `camelCase` field names (e.g., `totalClose`, `pendingCashOpen`), which differs from the `kebab-case` convention often used by other tastytrade API endpoints.
*   **Zoned datetime format:** The `start-time` and `end-time` parameters require [ISO 8601 zoned datetime format](../concepts/iso-8601.md) with timezone information (e.g., `2026-01-01T00:00:00+00:00[UTC]`), not plain dates.
*   **OHLC format:** Data is provided in [candlestick format](../concepts/ohlc-candlestick-format.md). For a simple line chart of account value, the `close` field from each candle is typically used.
*   **Total vs. Net Liq:** The `total*` fields include pending cash (unsettled funds), whereas the base `open`, `high`, `low`, and `close` fields represent the [net liquidating value](../concepts/net-liquidating-value.md) only.