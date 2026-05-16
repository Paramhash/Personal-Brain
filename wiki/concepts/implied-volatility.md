---
tags: ["options", "volatility", "derivatives", "quantitative-finance"]
created: 2026-05-16
reviewed: false
source_origin: "level1-analysis"
---
# Implied Volatility

Implied Volatility (IV) is the market's forward-looking expectation of the magnitude of price movement in an underlying asset, derived by inverting an options pricing model (typically Black-Scholes) against observed market option prices. Unlike historical volatility, which is backward-looking, IV is a real-time signal embedded in option premiums.

## Core Concept

IV is expressed as an annualized percentage standard deviation. An IV of 20% on a stock implies the market expects roughly a ±20% move over the next year (or ±20% / √12 ≈ ±5.77% monthly) at one standard deviation.

IV increases when demand for options increases (fear, hedging, event anticipation) and decreases when demand falls (complacency, post-event resolution).

## IV Rank (IVR)

**IV Rank** measures where the current IV sits relative to its 52-week range:

```
IVR = (Current IV − 52-week Low IV) / (52-week High IV − 52-week Low IV) × 100
```

- **IVR > 50**: IV is elevated relative to its range → options are relatively expensive → favors short-vol strategies (premium selling)
- **IVR < 30**: IV is suppressed → options are relatively cheap → favors long-vol strategies (premium buying)

## IV Percentile (IVP)

**IV Percentile** measures the percentage of days over the past year where IV was *below* the current IV level. More robust than IVR when IV distribution is skewed.

- **IVP > 70**: IV is high versus history → favorable for selling premium
- **IVP < 30**: IV is low versus history → favorable for buying optionality

## Historical Volatility vs. Implied Volatility

| Metric | Backward-looking | Forward-looking |
|---|---|---|
| Historical Volatility (HV) | Realized price movement (rolling window) | — |
| Implied Volatility (IV) | — | Market expectation of future movement |

**IV Premium**: IV typically trades above realized HV (the "volatility risk premium"). This premium is why systematic premium-selling strategies (iron condors, covered calls) have a long-run positive expected value — sellers capture the gap between what the market implies and what actually occurs.

## Vol Crush and Vol Expansion

**Vol Crush**: IV drops sharply after a binary event resolves (earnings announcement, FOMC decision). Options that were expensive going into the event become cheap afterward, even if the underlying moved significantly. This is the central risk in holding long options through earnings.

**Vol Expansion**: IV rises in anticipation of upcoming uncertainty or during market stress. Increases option premium and benefits holders of long options or straddles.

## IV in the MAOPM System

The [Volatility Analyst](../research/Current%20Research%20Initiatives.md) agent monitors IV rank and percentile per symbol to classify the current volatility regime and feed into the strategy debate between the Long-Vol and Short-Vol Researchers. See also [Options Strategies](../concepts/options-strategies.md) for how IV level maps to strategy selection, and [Event-Driven Options Risk](../concepts/event-driven-options-risk.md) for IV crush dynamics.

## Related Concepts

- [Volatility Surfaces](../concepts/volatility-surfaces.md) — how IV varies across strikes and expirations
- [Volatility Surface Dynamics](../concepts/volatility-surface-dynamics.md) — skew and term structure interpretation
- [Options Greeks](../concepts/options-greeks.md) — Vega measures an option's sensitivity to IV changes
- [Regime Detection](../concepts/regime-detection.md) — vol regime classification
- [Options Risk Metrics](../concepts/options-risk-metrics.md) — probability of profit changes with IV

---
