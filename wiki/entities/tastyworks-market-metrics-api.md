---
tags: ["api", "trading", "options", "market-data", "tastyworks"]
created: 2023-10-27
reviewed: false
source_origin: "market-metrics.md"
---
# Tastyworks Market Metrics API

The Market Metrics API, provided by Tastyworks, offers comprehensive volatility, liquidity, dividend, and earnings data specifically tailored for equity underlyings. It is a crucial resource for options-focused trading workflows, enabling users to make informed decisions based on key metrics like implied volatility rank (IVR) and implied volatility percentile.

**Base URL:** `https://api.tastyworks.com`
**Authentication:** Requires a valid session token passed via the `Authorization` header.
**API Version:** 1.9.1

## Endpoints

### Get Market Metrics

Returns volatility and liquidity data for one or more symbols, including per-expiration implied volatility breakdowns.

*   **Request:** `GET /market-metrics?symbols={symbols}`
*   **Query Parameters:**
    *   `symbols` (string, Required): Comma-separated list of underlying symbols (e.g., `AAPL,SPY,TSLA`). URL-encode special characters (e.g., `BRK%2FB`).
*   **Response:** `200 OK` — An array of [[MarketMetricInfo]] objects.

### Get Historical Dividends

Returns historical dividend data for a specified symbol.

*   **Request:** `GET /market-metrics/historic-corporate-events/dividends/{symbol}`
*   **Path Parameters:**
    *   `symbol` (string, Required): The equity symbol (e.g., `AAPL`).
*   **Response:** `200 OK` — An array of [[DividendInfo]] objects.

### Get Historical Earnings Reports

Returns historical earnings data for a symbol within a specified date range.

*   **Request:** `GET /market-metrics/historic-corporate-events/earnings-reports/{symbol}`
*   **Path Parameters:**
    *   `symbol` (string, Required): The equity symbol (e.g., `AAPL`).
*   **Query Parameters:**
    *   `start-date` (string, date, Required): Start of the date range (format: `YYYY-MM-DD`).
    *   `end-date` (string, date, Optional): End of the date range (format: `YYYY-MM-DD`). If omitted, returns earnings from `start-date` through the present.
*   **Response:** `200 OK` — An array of [[EarningsInfo]] objects.

## Data Models

### MarketMetricInfo

Provides volatility and liquidity data for an underlying symbol, including per-expiration implied volatility breakdowns.

*   **Underlying Volatility:**
    *   `symbol`: The underlying symbol.
    *   `implied-volatility-index`: The current [[../concepts/implied-volatility.md|implied volatility]] index for the underlying (e.g., `0.2845` = 28.45% IV).
    *   `implied-volatility-index-5-day-change`: Change in IV index over the past 5 trading days.
    *   `implied-volatility-rank`: [[../concepts/implied-volatility-rank.md|IV Rank (IVR)]] (0-1).
    *   `implied-volatility-percentile`: [[../concepts/implied-volatility-percentile.md|IV Percentile]] (0-1).
*   **Liquidity:**
    *   `liquidity`: A [[../concepts/liquidity.md|liquidity]] score for the underlying's options (0-1).
    *   `liquidity-rank`: Liquidity rank relative to other underlyings (0-1).
    *   `liquidity-rating`: Integer liquidity rating (e.g., 1–5).
*   **Per-Expiration Implied Volatility:**
    *   `option-expiration-implied-volatilities`: Array of objects, each containing:
        *   `expiration-date`: The option expiration date.
        *   `settlement-type`: `AM` or `PM`.
        *   `option-chain-type`: `Standard` or `Non-standard`.
        *   `implied-volatility`: The implied volatility for this specific expiration.

### DividendInfo

A single historical [[../concepts/dividends.md|dividend]] record.

*   `occurred-date`: The date the dividend occurred (ex-dividend date).
*   `amount`: The per-share dividend amount.

### EarningsInfo

A single historical [[../concepts/earnings-reports.md|earnings report]] record.

*   `occurred-date`: The date of the earnings announcement.
*   `eps`: Earnings per share (actual reported EPS).

## Common Use Cases

*   **Premium selling signals:** Identify underlyings with high [[../concepts/implied-volatility-rank.md|IVR]] (e.g., >0.50) and good [[../concepts/liquidity.md|liquidity]] (rating 4+) to find favorable conditions for selling options premium.
*   **Expiration selection:** Compare `option-expiration-implied-volatilities` to find expirations with relatively high [[../concepts/implied-volatility.md|implied volatility]].
*   **Earnings plays:** Analyze historical [[../concepts/earnings-reports.md|earnings reports]] and IV behavior around announcements to inform trading strategies.
*   **Dividend risk for options:** Identify upcoming ex-dividend dates using the dividends endpoint to manage risk for short call positions.
*   **Batch symbol lookup:** Fetch volatility data for multiple symbols in a single request.

## Important Notes

*   **IVR vs. IV Percentile:** These are distinct measures. [[../concepts/implled-volatility-rank.md|IVR]] compares current IV to its 52-week range, while [[../concepts/implied-volatility-percentile.md|IV Percentile]] measures the percentage of days IV was lower in the past year.
*   **Volatility values are decimals:** An `implied-volatility-index` of `0.2845` represents 28.45% annualized implied volatility.
*   **URL encoding:** Symbols with special characters (e.g., `BRK/B`) must be URL-encoded as `BRK%2FB`.

---