---
tags: ["options", "derivatives", "trading-strategy", "risk-management", "portfolio-management"]
created: 2026-05-16
reviewed: false
source_origin: "level1-analysis"
---
# Expiration Management

Expiration Management covers the strategic selection of Days to Expiration (DTE) when entering options positions, and the ongoing management of those positions as they approach expiration — including rolling, closing early, and managing the risks unique to the expiration period.

## Days to Expiration (DTE) Selection

DTE determines the balance between theta decay rate and gamma risk. The choice is not arbitrary; it reflects a deliberate view on the trade-off:

| DTE Range | Theta Decay Rate | Gamma Risk | Typical Use Case |
|---|---|---|---|
| 0–7 DTE (0DTE) | Extreme (non-linear) | Very high | Day-trading; [Zero Days to Expiration](../concepts/zero-days-to-expiration.md) strategies |
| 7–21 DTE | High | High | Short-term momentum / directional plays |
| 21–45 DTE | Optimal for premium selling | Moderate | Iron condors, credit spreads, CSPs |
| 45–60 DTE | Moderate | Low | Balanced risk; standard entry for short-vol |
| 60–90 DTE | Lower | Low | Calendars, diagonals, long vol setups |
| 90–180+ DTE (LEAPS) | Very low | Very low | Long-term directional exposure; equity substitute |

**The 21–45 DTE Sweet Spot**: For premium-selling strategies, this window is widely used because theta decay accelerates as expiration approaches but gamma risk has not yet become extreme. Positions are typically opened at 45 DTE and closed at 21 DTE (50% profit or stop-loss rule).

## The 21 DTE Management Rule

A common rules-based discipline: close or roll short-vol positions when they reach 21 DTE, regardless of profit. This avoids the asymmetric gamma risk of the final three weeks, where small adverse moves can cause outsized losses.

In the MAOPM system, the Greeks Analyst monitors DTE continuously and generates a management event when any short option reaches 21 DTE, triggering a Portfolio Manager review cycle.

## Rolling Positions

**Rolling** means closing an existing position and opening a new one further in time (and optionally at different strikes) to:
- Collect additional premium and extend the profit window
- Avoid assignment or expiration losses
- Adjust strikes to accommodate a changed underlying price level

**Roll criteria**:
- **Roll up/down**: Move strikes to keep them OTM when the underlying has moved significantly
- **Roll out**: Extend expiration to collect more time premium and reduce gamma risk
- **Roll for credit**: Only roll when the new position collects a net credit (standard discipline for short-vol books)

**When NOT to roll**: If the position has breached the max-loss threshold, rolling compounds the loss by taking on more risk. The Risk Team has veto authority over rolls that would increase total max loss.

## Gamma Risk Near Expiration

As options approach expiration, Gamma (the rate of delta change) increases dramatically for near-the-money options. This creates **gamma risk**:

- Small moves in the underlying cause large, rapid delta swings
- Delta can move from 0.10 to 0.90 within a single trading day in the final week
- Short gamma positions (iron condors, short straddles) are most vulnerable
- The Greeks Analyst escalates gamma risk alerts when any short option with > 0.20 delta approaches < 14 DTE

Refer to [Options Greeks](../concepts/options-greeks.md) for the Gamma definition and [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md) for how net gamma is monitored.

## Pin Risk

**Pin risk** occurs when the underlying closes exactly at or near a short strike at expiration. This creates ambiguity:

- If the underlying closes exactly at the short strike, the option may or may not be exercised (depends on the holder's decision)
- The short seller doesn't know whether they will be assigned until after market close
- Creates overnight risk: the position may be assigned and the trader wakes up with an unexpected stock position

**MAOPM mitigation**: The Execution Agent closes any position where the underlying is within 0.5% of a short strike at 3:00 PM ET on expiration day (one hour before close). This is a hard rule enforced by the Risk Team.

## Assignment Risk

Early assignment (for American-style options) can occur any time for short options that are in-the-money. Most common for:
- Short calls when the underlying pays a dividend (call assignment to capture the dividend)
- Deep ITM short puts or calls near expiration

**MAOPM mitigation**: The Greeks Analyst monitors delta of all short options; any short option with delta exceeding 0.70 in absolute value triggers a management review.

## Expiration Calendar Management

The News/Catalyst Analyst tracks the expiration calendar in conjunction with event risk:
- Avoid holding short-vol positions through earnings (IV crush unpredictable direction)
- Prefer expirations that do not straddle known binary events (FOMC, CPI) unless explicitly positioning for the event
- See [Event-Driven Options Risk](../concepts/event-driven-options-risk.md) for the full event framework

## Related Concepts

- [Zero Days to Expiration](../concepts/zero-days-to-expiration.md) — the extreme case of DTE selection
- [Options Greeks](../concepts/options-greeks.md) — Gamma and Theta dynamics near expiration
- [Options Strategies](../concepts/options-strategies.md) — DTE selection varies by strategy type
- [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md) — net gamma monitoring near expiry
- [Options Risk Metrics](../concepts/options-risk-metrics.md) — max loss and PoP change as DTE decreases
- [Event-Driven Options Risk](../concepts/event-driven-options-risk.md) — event calendar drives expiration selection

---
