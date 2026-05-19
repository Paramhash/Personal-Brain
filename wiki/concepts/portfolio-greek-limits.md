---
tags: [risk-management, options-trading, portfolio-management, greeks]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# Portfolio Greek Limits

**Portfolio Greek Limits** refer to the maximum allowable exposures to various [[../concepts/options-greeks.md|Options Greeks]] (Delta, Gamma, Vega, Theta) within a trading portfolio. These limits are fundamental tools in options risk management, designed to control the sensitivity of a portfolio's value to changes in underlying market parameters.

## Purpose
The primary purpose of setting Greek limits is to:
*   **Control Risk**: Prevent excessive exposure to specific market factors.
*   **Manage Volatility**: Limit potential losses from adverse movements in underlying prices, volatility, or time decay.
*   **Ensure Liquidity**: Maintain a manageable risk profile that can be adjusted or hedged efficiently.

## Dynamic Adjustment
Traditionally, Greek limits might be static or adjusted manually. However, the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]] introduces a dynamic approach:
*   **Baseline Limits**: A set of initial, maximum dollar exposures for each Greek (e.g., max Delta, max Gamma).
*   **Dynamic Scaling**: These baseline limits are continuously adjusted by the engine based on real-time market conditions, including the [[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio (RDR)]], [[../concepts/gex.md|Gamma Exposure (GEX)]], and [[../concepts/vvix.md|Vol-of-Vol Index (VVIX)]].

## Asymmetric Scaling
A key feature of dynamic Greek limits is asymmetric scaling, where different Greeks are adjusted differently depending on the market regime:
*   **Standard Coherent Regime**: Limits are scaled by a general multiplier derived from RDR. Delta limits might tighten slightly in very stable markets.
*   **Negative GEX Risk Reduction**: In environments with critical negative GEX, Gamma and Vega limits are significantly contracted, while Delta limits may be widened to absorb localized spot gaps.
*   **Divergence Strategy Mode**: During periods of high market stress (e.g., high VVIX or extreme RDR), short volatility/gamma risk (Vega, Gamma) is drastically reduced, and Delta limits are expanded to provide buffers against rapid price movements.

This dynamic and asymmetric approach allows for more nuanced and adaptive risk management, ensuring that the portfolio's risk profile is appropriate for the prevailing market environment.

## Related Concepts
*   [[../concepts/options-greeks.md|Options Greeks]]
*   [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]]
*   [[../concepts/gex.md|Gamma Exposure (GEX)]]
*   [[../concepts/vvix.md|Vol-of-Vol Index (VVIX)]]