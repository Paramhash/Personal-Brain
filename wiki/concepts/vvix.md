---
tags: [financial-metrics, volatility, market-sentiment, risk-indicators]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# VVIX (Vol-of-Vol Index)

The **VVIX** (Volatility of Volatility Index) is a financial metric that measures the implied volatility of options on the VIX (CBOE Volatility Index). In essence, it reflects the market's expectation of future volatility in the VIX itself.

## Significance
*   **Volatility of Volatility**: While VIX measures the market's expectation of future S&P 500 volatility, VVIX measures how much the market expects that *volatility expectation* to change.
*   **Market Panic Indicator**: A high VVIX reading typically indicates extreme uncertainty or "panic" in the market regarding future volatility. Investors are not just expecting high volatility, but also expecting that high volatility to be highly volatile itself. This often precedes or accompanies periods of significant market stress and large price swings.
*   **Risk-Off Sentiment**: Elevated VVIX levels are often associated with a "risk-off" sentiment, where investors seek to reduce exposure to risky assets.

## Role in Regime Risk Scaling
Within the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]], VVIX serves as a critical absolute filter:
*   **`vvix_threshold`**: A predefined critical level (e.g., 120.0).
*   **Override Trigger**: If the `current_vvix` exceeds this `vvix_threshold`, it triggers a "DIVERGENCE_STRATEGY_MODE" operational mode. This mode represents a severe environment and leads to drastic adjustments in [[../concepts/portfolio-greek-limits.md|portfolio Greek limits]].

## Impact on Portfolio Limits
When a VVIX override is active, the engine typically:
*   **Crushes Short Volatility/Gamma Risk**: Significantly reduces allowable [[../concepts/options-greeks.md|Vega]] and [[../concepts/options-greeks.md|Gamma]] exposures (e.g., a 95% reduction), effectively blocking new premium selling.
*   **Expands Delta Buffers**: Widens [[../concepts/options-greeks.md|Delta]] limits to prevent over-hedging churn and allow for greater directional flexibility in highly volatile conditions.

This aggressive scaling aims to rapidly de-risk the portfolio in anticipation of or during periods of structural market panic.

## Related Concepts
*   [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]]
*   [[../concepts/portfolio-greek-limits.md|Portfolio Greek Limits]]
*   [[../concepts/options-greeks.md|Options Greeks]]
*   [[../concepts/gex.md|Gamma Exposure (GEX)]]