---
tags: ["options", "volatility", "market-metrics"]
created: 2023-10-27
reviewed: false
source_origin: "market-metrics.md"
---
# Implied Volatility

**Implied Volatility (IV)** is a forward-looking estimate of a security's expected price fluctuation over a specific period. It is derived from the market price of an option and reflects the market's consensus view on the future volatility of the underlying asset. Higher implied volatility generally means higher option premiums, as there's a greater perceived chance of the underlying asset moving significantly.

The [[../entities/tastyworks-market-metrics-api.md|Tastyworks Market Metrics API]] provides several measures related to implied volatility:

*   **Implied Volatility Index:** A current, aggregated measure of implied volatility for an underlying asset.
*   **Per-Expiration Implied Volatilities:** Specific implied volatility values for different option expiration dates, allowing traders to assess volatility across the term structure.

Implied volatility is a core input for options pricing models and is often used in conjunction with other metrics like [[./implied-volatility-rank.md|Implied Volatility Rank (IVR)]] and [[./implied-volatility-percentile.md|Implied Volatility Percentile]] to gauge whether options are relatively expensive or cheap.

---