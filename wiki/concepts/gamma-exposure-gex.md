---
tags: [options, volatility, market-analysis, gamma, gex]
created: 2023-10-27
reviewed: false
source_origin: "Strategies to benefit from divergences between the GEX profiles of individual stocks in the S&P500 and the index..md"
---
# Gamma Exposure (GEX)

**Gamma Exposure (GEX)**, often referred to simply as GEX, is a measure of the sensitivity of options dealers' deltas to changes in the underlying asset's price. It quantifies the amount of gamma that market makers are exposed to, which in turn indicates their potential hedging activity.

## Role in Market Dynamics

*   **Positive GEX:** Generally indicates that dealers are net long gamma. This means they will buy into falling prices and sell into rising prices, acting as a stabilizing force on the market. High GEX often signals market stability and range-bound movement.
*   **Negative GEX:** Generally indicates that dealers are net short gamma. This means they will sell into falling prices and buy into rising prices, acting as an accelerating force on market movements. Low or negative GEX often signals market instability and increased volatility.

When the [[../entities/sp500-index.md|S&P 500 index]] GEX is at odds with the aggregate GEX of its 500 constituents, it signals that the "market engine" is misfiring, leading to [[../concepts/gex-divergence-strategies.md|GEX Divergences]].

## Metrics for Divergence Detection

To effectively identify and trade GEX divergences, several metrics can be calculated:

### GEX Z-Score

For each of the 500 stocks in the S&P 500, the **GEX Z-Score** measures how far its current GEX is from its 30-day mean. This helps to normalize GEX values across different stocks and identify outliers in their gamma profiles.

### S&P 500 Internal GEX Index

The **S&P 500 Internal GEX Index** is created by averaging the GEX Z-scores of all 500 constituents. This aggregate metric provides a view of the "internal health" or underlying gamma support of the index components, independent of the headline index GEX.

### Decoupling Regime

A **Decoupling Regime** is identified when the [[../entities/sp500-index.md|Index GEX]] is rising (suggesting stability) but the **S&P 500 Internal GEX Index** is falling (suggesting underlying fragility). This divergence signals a market where the index's apparent stability is not supported by its components, creating opportunities for [[../concepts/gex-divergence-strategies.md|GEX Divergence Strategies]].

## Importance of Key Constituents

The GEX of heavily weighted stocks, such as the [[../entities/magnificent-7-stocks.md|Magnificent 7]], can disproportionately influence the overall index GEX. If their GEX diverges significantly from the other 495 stocks, the index will often eventually follow the leaders.

## Related Concepts

*   [[../concepts/gex-divergence-strategies.md|GEX Divergence Strategies]]
*   [[../entities/sp500-index.md|S&P 500 Index]]
*   [[../entities/magnificent-7-stocks.md|Magnificent 7 Stocks]]
*   [[../research/gex-scanner-logic-flow.md|GEX Scanner Logic Flow]]

---