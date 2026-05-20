---
tags: ["options", "volatility", "market-metrics", "trading-strategy"]
created: 2023-10-27
reviewed: false
source_origin: "market-metrics.md"
---
# Implied Volatility Percentile (IV Percentile)

**Implied Volatility Percentile (IV Percentile)** is a metric used in options trading to gauge the current [[./implied-volatility.md|implied volatility (IV)]] of an underlying asset relative to its historical values over the past year. It is expressed as a decimal between 0 and 1 (or a percentage between 0% and 100%).

**Interpretation:**
*   An IV Percentile of `0.42` (42%) means that on 42% of the trading days in the past year, the implied volatility was lower than the current level. Conversely, on 58% of the days, it was higher.
*   A higher IV Percentile (e.g., above 0.70 or 70%) indicates that the current implied volatility is higher than it has been on most days over the past year, suggesting that options are relatively expensive. This can be a favorable condition for strategies that involve selling options premium.
*   A lower IV Percentile suggests options are relatively cheaper.

**Distinction from [[./implied-volatility-rank.md|Implied Volatility Rank (IVR)]]**:
While both IV Percentile and IVR aim to show the relative expensiveness of options, they do so differently. IV Percentile measures the *percentage of days* that IV was lower than the current level. IVR, on the other hand, measures where the current IV falls within the *range* of the 52-week high and low. It's possible for IVR to be low while IV Percentile is high if there was a single, very high IV spike during the year that significantly widened the 52-week range.

The [[../entities/tastyworks-market-metrics-api.md|Tastyworks Market Metrics API]] provides `implied-volatility-percentile` as a key data point for equity underlyings.

---