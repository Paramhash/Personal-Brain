---
tags: ["options", "risk-management", "derivatives", "market-analysis", "trading-strategy"]
created: 2026-05-16
reviewed: false
source_origin: "level1-analysis"
---
# Event-Driven Options Risk

Event-driven options risk arises from scheduled or unscheduled binary events that cause discontinuous, non-normal price and volatility changes in options portfolios. Managing this risk is the primary responsibility of the News/Catalyst Analyst in the [MAOPM system](../research/Current%20Research%20Initiatives.md), with the Risk Management Team enforcing hard position limits around event windows.

## Categories of Binary Events

### Earnings Announcements
The most common scheduled event risk in equities options. Characteristics:
- **IV Expansion** (pre-event): Implied volatility increases as the event approaches, inflating option premiums regardless of direction
- **IV Crush** (post-event): IV drops sharply immediately after the announcement, often by 30–60%, even if the underlying moved significantly
- **Gap risk**: The underlying may open 5–20%+ away from the prior close; standard PoP models (which assume continuous price movement) understate this risk

**Implication**: Short-vol positions (iron condors, short straddles) held through earnings face the possibility of the underlying gapping beyond the breakevens despite high IV having been collected. Long-vol positions (straddles, strangles) face vol crush if the move is smaller than the market priced in.

**MAOPM default rule**: No new short-vol positions are opened with expirations that straddle an earnings date unless the Portfolio Manager explicitly overrides with Risk Team approval. Existing positions are reviewed and optionally closed 2 days before earnings.

### FOMC Announcements
Federal Reserve rate decisions and meeting minutes create macro volatility spikes:
- Affect the entire equity market simultaneously (systematic risk — cannot be diversified away)
- VIX typically spikes then mean-reverts within 1–2 sessions
- Rate surprises create sharp directional moves and vol expansion

**MAOPM rule**: Reduce net short-vega exposure to ≤50% of normal limits in the 48 hours before scheduled FOMC announcements.

### Macroeconomic Data Releases
CPI, PCE, NFP, GDP revisions — all can cause sharp intraday moves:
- Less predictable in magnitude than earnings (no company-specific IV)
- Primarily affects broad-market positions (index options, ETF options)

### Unscheduled / Exogenous Events
Black swan events (geopolitical, systemic): credit crises, flash crashes, central bank interventions. These cause:
- Rapid [volatility surface](../concepts/volatility-surface-dynamics.md) inversion
- Extreme negative GEX regimes (see [Gamma Exposure GEX](../concepts/gamma-exposure-gex.md))
- Gap risk across all positions simultaneously

Cannot be predicted; managed by maintaining aggregate max-loss limits at the portfolio level.

## IV Crush Mechanics

The IV crush post-event is the primary trap for long-vol strategies:

```
Pre-event: IV = 80% (high demand for hedging)
Post-event: IV = 35% (event resolved, hedging demand drops)
```

Even if the underlying moves 5%, the premium decay from vol crush can exceed the gain from delta exposure. The Volatility Analyst monitors the expected move (EM) embedded in IV versus historical realized moves to assess whether long-vol positions are "cheap" or "expensive" going into events:

```
Expected Move (EM) = IV × Price × √(DTE / 365)
```

If EM > typical historical move size for similar events, long vol is rich; if EM < historical move, long vol may be cheap.

## Gap Risk

Options pricing models assume continuous price movement (no gaps). Binary events violate this assumption:
- A put spread with max loss at $480 strike provides no protection if the stock opens at $450
- Short strangles can suffer full max loss on a single overnight gap

**MAOPM mitigation**:
1. No naked short options held through earnings (defined-risk spreads only)
2. Spread widths sized to accommodate typical event-magnitude gaps
3. Portfolio Manager tracks aggregate gap exposure (worst-case gap P&L) as a separate risk metric

## Event Calendar Management

The News/Catalyst Analyst maintains a forward-looking event calendar and produces an **Event Risk Report** each morning:

| Event | Date | Affected Positions | Action Required |
|---|---|---|---|
| AAPL Earnings | 2026-05-28 | Short May28 condor | Close or roll before May 26 |
| FOMC Meeting | 2026-06-11 | All net short vega | Reduce to 50% before June 9 |
| CPI Release | 2026-06-12 | SPY positions | Review; no new positions day of |

This report is a structured document input to the Portfolio Manager and Risk Team at the start of each analysis cycle.

## Interaction with GEX Regime

During extreme events, [GEX](../concepts/gamma-exposure-gex.md) becomes sharply negative — dealers are forced to sell into falling markets, amplifying moves. This interaction means event-driven risk and regime risk are correlated: the worst outcomes occur when a binary event triggers a negative GEX regime simultaneously.

The GEX/Regime Analyst monitors for this combination and escalates to maximum defensive posture (hard Greek limit reductions, no new short-vol entries).

## Related Concepts

- [Implied Volatility](../concepts/implied-volatility.md) — IV expansion and crush are the mechanism of event risk
- [Volatility Surface Dynamics](../concepts/volatility-surface-dynamics.md) — term structure inversion signals event proximity
- [Options Strategies](../concepts/options-strategies.md) — strategy selection must account for upcoming events
- [Options Risk Metrics](../concepts/options-risk-metrics.md) — PoP models understate binary event risk
- [Expiration Management](../concepts/expiration-management.md) — expiration selection avoids binary event straddles
- [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md) — negative GEX amplifies event moves
- [Regime Detection](../concepts/regime-detection.md) — event risk interacts with regime classification

---
