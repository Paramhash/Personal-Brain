---
tags: ["options", "portfolio-management", "risk-management", "quantitative-finance", "derivatives"]
created: 2026-05-16
reviewed: false
source_origin: "level1-analysis"
---
# Portfolio Greeks Management

Portfolio Greeks Management is the practice of monitoring and actively controlling the aggregate sensitivity of an options portfolio to changes in underlying price (Delta), price curvature (Gamma), implied volatility (Vega), and time decay (Theta). It is the operational core of the Greeks Analyst and Risk Management Team agents in the [MAOPM system](../research/Current%20Research%20Initiatives.md).

## Portfolio-Level Greeks

Unlike single-position Greeks, portfolio Greeks represent the *net* exposure across all positions simultaneously:

| Greek | Aggregate Meaning | Sign Preference (neutral book) |
|---|---|---|
| Net Delta (Δ) | Dollar change in portfolio value per $1 move in underlying | ≈ 0 (delta-neutral) |
| Net Gamma (Γ) | Rate of delta change per $1 move | Managed; high gamma = large delta swings |
| Net Vega (ν) | P&L change per 1% IV change | Managed; reflects vol bias |
| Net Theta (Θ) | Daily P&L from time passage (negative = time decay cost) | Often positive for premium sellers |

**Key relationship**: Gamma and Theta are roughly inversely related. Long gamma portfolios tend to have negative theta (you pay time decay for the optionality). Short gamma portfolios collect positive theta but are exposed to large moves.

## Greek Targets and Limits

The Portfolio Manager sets target ranges; the Risk Team enforces hard limits:

| Greek | Example Target Range | Hard Limit (paper trading) |
|---|---|---|
| Net Delta | ±$500 per 1% underlying move | ±$2,000 per 1% |
| Net Gamma | Monitor; regime-dependent | Escalate if breached |
| Net Vega | ±$1,000 per 1% IV change | ±$3,000 per 1% IV change |
| Net Theta | Positive (premium-selling bias) | Minimum −$100/day (protect against bleed) |

Limits should tighten in [negative GEX regimes](../concepts/gamma-exposure-gex.md) and expand in positive GEX / low-vol regimes (per [Regime Detection](../concepts/regime-detection.md)).

## Delta-Neutral Hedging

A delta-neutral portfolio has a net delta of approximately zero — gains and losses from price movement cancel across positions. This allows the portfolio to profit from volatility and time decay rather than directional moves.

**Maintenance**:
- When net delta drifts outside the target range, the Greeks Analyst triggers a hedge alert
- The Portfolio Manager may add or remove shares of the underlying (delta hedging with stock) or adjust an existing options leg
- Frequency: continuous monitoring; hedge adjustments triggered at ±threshold (not continuously rebalanced, due to transaction cost)

**Gamma scalping**: A portfolio that is long net gamma can profit by continuously delta-hedging as the underlying moves. Each hedge lock-in a gain from the convexity of long options. Most viable when [realized volatility exceeds IV](../concepts/implied-volatility.md) (i.e., you are "long vega at a good price").

## Vega Management

Net Vega determines the portfolio's sensitivity to [implied volatility](../concepts/implied-volatility.md) changes. Managing vega is particularly important around binary events ([earnings, FOMC](../concepts/event-driven-options-risk.md)).

- **Long vega (positive net vega)**: Portfolio benefits from IV expansion; loses if IV contracts (vol crush)
- **Short vega (negative net vega)**: Portfolio benefits from IV contraction; loses if IV spikes

**Regime adjustment**: The Volatility Analyst's regime classification feeds into the Portfolio Manager's vega target. In a vol-expansion regime, the system reduces short vega exposure. In a vol-contraction (stable, high IVR) regime, the system increases short vega exposure for premium capture.

## Theta Management

Theta is the portfolio's daily time decay. For premium sellers, positive theta is the primary profit engine. For option buyers, negative theta is the cost of holding optionality.

**Monitoring**: The Greeks Analyst tracks cumulative daily theta bleed vs. realized P&L to ensure premium collected is justifying exposure taken.

## Position Sizing and Greek Contribution

Each new position proposed by the Portfolio Manager is evaluated for its *marginal Greek contribution* to the portfolio before approval:

1. Calculate new position's individual Greeks
2. Add to portfolio net Greeks
3. Check result against targets and hard limits
4. If limits would be breached, Risk Team must approve or resize the position

## Integration with MAOPM Agents

```
Greeks Analyst → monitors real-time net Greeks, triggers breach alerts
     ↓
Portfolio Manager → checks Greek impact of proposed trades before approval
     ↓
Risk Management Team → enforces hard limits; may veto or resize
     ↓
Execution Agent → confirms fill; Greeks Analyst updates portfolio state
```

## How Tightening Gamma/Vega Limits Affects Position Sizing and Capital Deployment

Greek limits are portfolio-wide caps on the **net sum across all open positions**, not per-position limits. After all positions net out (e.g., a short put partially cancels a long call hedge), the residual must stay within the limit.

### Vega Limit Tightening

Vega measures P&L change per 1% move in implied volatility. Short-vol strategies (iron condors, CSPs, short strangles) are net short vega — they lose when IV spikes. Tightening the vega limit reduces the allowable short vega position:

**Sizing math**: if one iron condor contributes −$80 vega and the allowable short vega drops from −$3,000 to −$1,500, maximum contract count drops from ~37 to ~18. Premium collected (theta) per cycle falls proportionally. The theta-to-vega ratio does not improve — the portfolio simply earns less.

### Gamma Limit Tightening

Gamma measures how fast delta changes as the underlying moves. A net short gamma book has a concave P&L profile — it profits from stillness, suffers from large moves. Tighter gamma limits do not simply reduce size; they **change which strategy types are viable**:

- Short gamma comes primarily from short options near ATM with short DTE
- Tighter limits push toward wider spreads (defined-risk structures cap gamma per contract), longer DTE (lower gamma), or fewer contracts
- This may require shifting *strategy type* — e.g., from short strangles to iron condors, or from 30-DTE to 45-DTE positions

### Capital Deployment Consequence

The binding Greek limit determines how much buying power reduction (BPR) can actually be deployed:

```
Capital deployed ≤ min(
    BPR cap (% of net liquidation value),
    vega limit / vega-per-contract,
    gamma limit / gamma-per-contract
)
```

In a vol-expansion regime, tighter vega limits often become the **binding constraint before the BPR cap is reached** — capital sits idle that would otherwise be deployable. A portfolio at 40% BPR utilization under normal limits may drop to 20% under tightened vega limits, with the remaining 20% unallocated because adding any more short-vol exposure would breach the cap.

The exact scaling function (linear, step-function, or regime-specific presets) is an open question documented in [Q2 of the MAOPM research agenda](../research/research-agenda-options-maopm.md).

## Related Concepts

- [Options Greeks](../concepts/options-greeks.md) — definitions of Delta, Gamma, Vega, Theta
- [Options Strategies](../concepts/options-strategies.md) — each strategy's Greek profile
- [Implied Volatility](../concepts/implied-volatility.md) — Vega sensitivity driver
- [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md) — market-level gamma context
- [Options Risk Metrics](../concepts/options-risk-metrics.md) — max loss and PoP alongside Greek limits
- [Expiration Management](../concepts/expiration-management.md) — Gamma acceleration near expiry requires tighter monitoring
- [Regime Detection](../concepts/regime-detection.md) — Greek limit sizing is regime-adaptive

---
