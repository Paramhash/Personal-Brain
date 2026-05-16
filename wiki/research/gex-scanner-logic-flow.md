---
tags: [research, automation, trading-tools, gex, market-analysis]
created: 2023-10-27
reviewed: false
source_origin: "Strategies to benefit from divergences between the GEX profiles of individual stocks in the S&P500 and the index..md"
---
# GEX Scanner Logic Flow

This document outlines a logic flow for a **GEX Scanner** designed to automate the detection of specific stock-vs-index decoupling events, which are central to [[../concepts/gex-divergence-strategies.md|GEX Divergence Strategies]]. The scanner leverages real-time processing capabilities to identify actionable divergences.

## Objective

To build a "Divergence Heatmap" that flags instances where the [[../entities/sp500-index.md|S&P 500 Index]] GEX is diverging from the aggregate GEX of its individual constituents, indicating a potential "decoupling regime."

## Logic Flow Steps

1.  **Calculate the "GEX Z-Score" for Each Stock:**
    *   For each of the 500 stocks in the [[../entities/sp500-index.md|S&P 500]], calculate its current [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]].
    *   Determine the 30-day mean of the GEX for that specific stock.
    *   Calculate the Z-score: `(Current GEX - 30-day Mean GEX) / 30-day Standard Deviation of GEX`.
    *   This normalizes the GEX values and highlights how unusual the current GEX is for each stock relative to its recent history.

2.  **Aggregate the "Internal Health" (S&P 500 Internal GEX Index):**
    *   Average the GEX Z-scores calculated in Step 1 across all 500 stocks.
    *   This average creates the **[[../concepts/gamma-exposure-gex.md#sp-500-internal-gex-index|S&P 500 Internal GEX Index]]**, which represents the collective gamma health of the underlying components.

3.  **Define the Trigger for a "Decoupling Regime":**
    *   A **[[../concepts/gamma-exposure-gex.md#decoupling-regime|Decoupling Regime]]** is triggered when two conditions are met:
        *   The **[[../entities/sp500-index.md|S&P 500 Index]] GEX** (the headline index GEX) is rising, indicating increasing stability at the index level.
        *   The **[[../concepts/gamma-exposure-gex.md#sp-500-internal-gex-index|S&P 500 Internal GEX Index]]** (the aggregated Z-score of constituents) is falling, indicating decreasing stability or increasing fragility among individual stocks.

## Expert Tip for Prioritization

When a decoupling regime is detected, pay particular attention to the **Top 5 weighted stocks** within the [[../entities/sp500-index.md|S&P 500]] (e.g., [[../entities/magnificent-7-stocks.md|AAPL, MSFT, NVDA, AMZN, GOOGL]]). Because of their massive weight, if their individual GEX diverges significantly from the other 495 stocks, the index will eventually follow the leaders. This provides a strong signal for potential [[../concepts/fragility-short-strategy.md|Fragility Short]] or [[../concepts/dispersion-trade-strategy.md|Dispersion Trade]] opportunities.

## Potential Enhancements

*   Integrate real-time options data feeds.
*   Visualize the "Divergence Heatmap" for quick identification.
*   Implement alerts for trigger conditions.
*   Incorporate historical backtesting capabilities.

## Related Concepts

*   [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]]
*   [[../concepts/gex-divergence-strategies.md|GEX Divergence Strategies]]
*   [[../entities/sp500-index.md|S&P 500 Index]]
*   [[../entities/magnificent-7-stocks.md|Magnificent 7 Stocks]]

---