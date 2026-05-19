---
tags: [financial-metrics, options-trading, market-structure, risk-indicators]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# Gamma Exposure (GEX)

**Gamma Exposure (GEX)**, in the context of market risk, typically refers to the aggregate net dealer gamma exposure across the options market for a particular underlying asset or index. It is a crucial metric for understanding market structure and potential feedback loops between options hedging and underlying price movements.

## Significance
*   **Dealer Hedging**: Dealers who sell options (often to retail or institutional buyers) become short gamma. To remain delta-neutral, they must buy the underlying asset as prices rise and sell as prices fall.
*   **Positive GEX**: When dealers are net long gamma, they buy into falling markets and sell into rising markets, acting as a stabilizing force.
*   **Negative GEX**: When dealers are net short gamma, they must sell into falling markets and buy into rising markets. This creates a "gamma squeeze" or "gamma trap," where dealer hedging amplifies price movements, leading to increased volatility and potentially rapid, large price swings.

## Role in Regime Risk Scaling
Within the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]], GEX serves as a critical absolute filter:
*   **`gex_critical`**: A predefined negative threshold (e.g., -100,000,000 USD per 1% move).
*   **Override Trigger**: If the `current_gex` falls below this `gex_critical` level, it triggers a "NEGATIVE_GEX_RISK_REDUCTION" operational mode. This mode implements specific, often severe, adjustments to [[../concepts/portfolio-greek-limits.md|portfolio Greek limits]] to mitigate risks associated with a dealer short-gamma environment.

## Impact on Portfolio Limits
When a negative GEX override is active, the engine typically:
*   **Contracts Gamma Limits**: Significantly reduces allowable [[../concepts/options-greeks.md|Gamma]] exposure.
*   **Contracts Vega Limits**: Reduces [[../concepts/options-greeks.md|Vega]] exposure.
*   **Widens Delta Limits**: Increases allowable [[../concepts/options-greeks.md|Delta]] exposure to absorb localized spot gaps and prevent over-hedging churn in a volatile environment.

This proactive adjustment helps protect the portfolio from the amplified price movements characteristic of negative GEX regimes.

## Related Concepts
*   [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]]
*   [[../concepts/portfolio-greek-limits.md|Portfolio Greek Limits]]
*   [[../concepts/options-greeks.md|Options Greeks]]