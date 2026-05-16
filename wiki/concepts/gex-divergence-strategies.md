---
tags: [trading, options, volatility, market-analysis]
created: 2023-10-27
reviewed: false
source_origin: "Strategies to benefit from divergences between the GEX profiles of individual stocks in the S&P500 and the index..md"
---
# GEX Divergence Strategies

GEX (Gamma Exposure) divergences occur when the aggregate [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]] of the [[../entities/sp500-index.md|S&P 500 index]] is at odds with the combined GEX of its individual constituents. This signals a potential "misfiring" in the market's underlying volatility structure, offering opportunities beyond simple price direction bets. These strategies leverage real-time processing capabilities to identify and capitalize on these discrepancies.

## Core Principle

The underlying premise is that market stability or instability, as indicated by GEX, can manifest differently at the index level versus the individual stock level. By identifying these divergences, traders can position themselves to profit from the resulting shifts in volatility and price action.

## Specific Strategies

Four key strategies are outlined to exploit these divergences:

1.  **[[./fragility-short-strategy.md|The "Fragility" Short]]**: Exploits high index GEX (stability) against low/negative individual stock GEX (instability).
2.  **[[./dispersion-trade-strategy.md|The Dispersion Trade]]**: Profits from suppressed index volatility alongside exploding component-level volatility.
3.  **[[./gamma-flip-mean-reversion-strategy.md|The "Gamma Flip" Mean Reversion]]**: Targets individual stocks that have flipped to negative gamma while the index remains stable, anticipating a snap-back.
4.  **[[./term-structure-catch-up-strategy.md|The Term Structure "Catch-Up"]]**: Leverages divergences between short-term (0DTE) and medium-term (45DTE) GEX profiles.

These strategies are designed to capitalize on different facets of volatility structure, from outright fragility to correlation breakdowns and term structure mispricings.

## Related Concepts

*   [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]]
*   [[../entities/sp500-index.md|S&P 500 Index]]
*   [[../entities/magnificent-7-stocks.md|Magnificent 7 Stocks]]
*   [[../research/gex-scanner-logic-flow.md|GEX Scanner Logic Flow]]

---