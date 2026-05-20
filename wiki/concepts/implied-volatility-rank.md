---
tags: ["options", "volatility", "market-metrics", "trading-strategy"]
created: 2023-10-27
reviewed: false
source_origin: "market-metrics.md"
---
# Implied Volatility Rank (IVR)

**Implied Volatility Rank (IVR)** is a metric used in options trading to assess the current [[./implied-volatility.md|implied volatility (IV)]] of an underlying asset relative to its own 52-week high and low IV levels. It is expressed as a decimal between 0 and 1 (or a percentage between 0% and 100%).

**Calculation:**
IVR = (Current IV - 52-week Low IV) / (52-week High IV - 52-week Low IV)

**Interpretation:**
*   An IVR of `0.35` (35%) means the current implied volatility is 35% of the way between its 52-week low and 52-week high.
*   A higher IVR (e.g., above 0.50 or 50%) suggests that the current implied volatility is relatively high compared to its past year's range, implying that options are currently more expensive. This can be a favorable condition for strategies that involve selling options premium.
*   A lower IVR suggests options are relatively cheaper.

**Distinction from [[./implied-volatility-percentile.md|Implied Volatility Percentile]]**:
While both IVR and IV Percentile aim to show the relative expensiveness of options, they do so differently. IVR looks at the current IV's position within the *range* of the last 52 weeks. A single extreme spike in IV during the year can skew the 52-week range, potentially making the IVR seem low even if the current IV is historically high on most days.

The [[../entities/tastyworks-market-metrics-api.md|Tastyworks Market Metrics API]] provides `implied-volatility-rank` as a key data point for equity underlyings.

---