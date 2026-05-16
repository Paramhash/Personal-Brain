---
tags: ["options", "trading-strategy", "derivatives", "portfolio-management"]
created: 2026-05-16
reviewed: false
source_origin: "level1-analysis"
---
# Options Strategies

Options strategies are structured positions combining one or more options legs (and optionally the underlying) to express a specific market view with a defined risk/reward profile. Strategy selection is the primary output of the [Strategy Research Team](../research/Current%20Research%20Initiatives.md) debate in the MAOPM system.

## Strategy Taxonomy

### Single-Leg Strategies

| Strategy | Structure | Bias | IV Preference |
|---|---|---|---|
| Long Call | Buy call | Bullish | Low IV (IVR < 30) |
| Long Put | Buy put | Bearish | Low IV (IVR < 30) |
| Short Call (naked) | Sell call | Bearish / neutral | High IV (IVR > 50) |
| Short Put (CSP) | Sell OTM put | Neutral / bullish | High IV (IVR > 50) |
| Covered Call | Own shares + sell call | Neutral / mildly bullish | High IV (IVR > 50) |

### Defined-Risk Spread Strategies

| Strategy | Structure | Bias | IV Preference |
|---|---|---|---|
| Bull Call Spread | Buy lower call + sell higher call | Bullish | Low-moderate IV |
| Bear Put Spread | Buy higher put + sell lower put | Bearish | Low-moderate IV |
| Bull Put Spread (credit) | Sell higher put + buy lower put | Bullish / neutral | High IV |
| Bear Call Spread (credit) | Sell lower call + buy higher call | Bearish / neutral | High IV |

### Non-Directional / Volatility Strategies

| Strategy | Structure | Bias | IV Preference | P&L Driver |
|---|---|---|---|---|
| Long Straddle | Buy ATM call + buy ATM put | Neutral (long vol) | Low IV; expects move > combined premium | Vol expansion or large move |
| Long Strangle | Buy OTM call + buy OTM put | Neutral (long vol) | Low IV; cheaper than straddle | Larger move required |
| Short Straddle | Sell ATM call + sell ATM put | Neutral (short vol) | High IV | Vol contraction, time decay |
| Short Strangle | Sell OTM call + sell OTM put | Neutral (short vol) | High IV; wider breakevens | Vol contraction, time decay |
| Iron Condor | Bull put spread + bear call spread | Neutral (short vol) | High IV; defined risk | Premium capture in range |
| Iron Butterfly | Sell ATM call/put + buy OTM call/put | Neutral (short vol) | High IV; max credit at current price | Pinning near ATM at expiry |

### Time and Calendar Strategies

| Strategy | Structure | Bias | Key Dynamic |
|---|---|---|---|
| Calendar Spread | Sell near-term + buy far-term (same strike) | Neutral; long vol | Profits from near-term vol crush + positive theta |
| Diagonal Spread | Sell near-term + buy far-term (different strikes) | Directional + vol | Combines spread with term structure view |
| LEAPS Call | Buy deep ITM long-dated call | Bullish long-term | Low-cost equity substitute; Theta-resistant |

## IV Regime → Strategy Mapping

This is the core decision rule the Long-Vol and Short-Vol Researchers debate around:

| IV Rank (IVR) | [Regime](../concepts/regime-detection.md) | Preferred Strategies |
|---|---|---|
| Low (< 30) | Low vol, stable | Long straddles, calendars, debit spreads, LEAPS |
| Moderate (30–50) | Transitional | Defined-risk spreads, diagonals |
| High (> 50) | High vol, fear | Iron condors, credit spreads, CSPs, covered calls |
| Extreme (> 80) | Panic / event | Protective puts for hedging; avoid naked shorts |

## GEX Regime Overlay

[Gamma Exposure](../concepts/gamma-exposure-gex.md) provides a microstructure layer on top of IV regime:

- **Positive GEX + High IVR** → Ideal for iron condors (range-bound, vol likely to mean-revert)
- **Negative GEX + Low IVR** → Avoid short-vol; potential for large moves; consider long vol or directional
- **Decoupling regime** (index GEX rising, constituent GEX falling) → Dispersion trades or fragility shorts

## Risk Profile Summary

| Property | Long-Vol Strategies | Short-Vol Strategies |
|---|---|---|
| Max Loss | Defined (premium paid) | Defined (spreads) or unlimited (naked) |
| Max Gain | Unlimited (straddles) or capped (spreads) | Capped (premium collected) |
| Theta | Negative (time decay hurts) | Positive (time decay helps) |
| Vega | Positive (IV increase helps) | Negative (IV increase hurts) |
| Probability of Profit | Lower (requires move/vol) | Higher (range-bound wins) |

## Use in MAOPM

Strategy selection is not static — it is determined each cycle by the [Long-Vol Researcher and Short-Vol Researcher](../research/Current%20Research%20Initiatives.md) debate, informed by [implied volatility](../concepts/implied-volatility.md), [surface dynamics](../concepts/volatility-surface-dynamics.md), [GEX/regime](../concepts/gamma-exposure-gex.md), and [event risk](../concepts/event-driven-options-risk.md). The Portfolio Manager then checks the selected strategy against portfolio-level [Greek targets](../concepts/portfolio-greeks-management.md) before approval.

## Related Concepts

- [Options Greeks](../concepts/options-greeks.md) — Greeks describe each strategy's sensitivities
- [Implied Volatility](../concepts/implied-volatility.md) — primary input to strategy selection
- [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md) — net portfolio impact of each strategy
- [Options Risk Metrics](../concepts/options-risk-metrics.md) — max loss, PoP, expected value per strategy
- [Expiration Management](../concepts/expiration-management.md) — DTE selection rationale per strategy type
- [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md) — market microstructure overlay

---
