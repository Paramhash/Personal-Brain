---
tags: [risk-management, financial-engineering, portfolio-management, dynamic-limits]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# Regime Risk Scaling Engine

The **Regime Risk Scaling Engine** is a structural architecture designed to implement dynamic, portfolio-level [[../concepts/portfolio-greek-limits.md|Greek limits]]. Its primary purpose is to adjust risk exposures in real-time based on prevailing market conditions, moving beyond static risk thresholds.

## Purpose
The engine aims to:
*   Provide continuous, non-linear scaling of [[../concepts/options-greeks.md|Options Greeks]] exposures.
*   Integrate absolute market filters to trigger hard overrides in extreme conditions.
*   Apply asymmetric scaling rules, allowing different Greeks to be managed distinctly across various market regimes.
*   Enhance risk management by making portfolio limits adaptive and responsive to market stress and stability.

## Key Components and Mechanism
1.  **[[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio (RDR)]]**: A core input that quantifies the current market regime's divergence from a "coherent" state.
2.  **[[../concepts/bi-symmetric-sigmoid-decay-function.md|Bi-Symmetric Sigmoid Decay Function]]**: This mathematical function takes the RDR as input and computes a continuous non-linear multiplier (between 0.0 and 1.0). This multiplier forms the baseline for scaling Greek limits.
3.  **Absolute Filters**:
    *   **[[../concepts/gex.md|Gamma Exposure (GEX)]]**: If aggregate dealer GEX falls below a critical negative threshold (`gex_critical`), it triggers a specific override mode focused on reducing path-dependent risk.
    *   **[[../concepts/vvix.md|Vol-of-Vol Index (VVIX)]]**: If VVIX exceeds a critical threshold (`vvix_threshold`), indicating structural panic, it triggers a severe divergence strategy mode.
4.  **Asymmetric Greek Scaling Rules**: Depending on the detected market regime and active overrides, the engine applies different scaling factors to individual [[../concepts/options-greeks.md|Greeks]] (Delta, Gamma, Vega, Theta).
    *   **STANDARD_COHERENT**: When RDR is within a stable range and no absolute overrides are active, limits are scaled smoothly by the RDR multiplier. Delta limits might tighten slightly in hyper-stable regimes.
    *   **NEGATIVE_GEX_RISK_REDUCTION**: Triggered by critical negative GEX. Gamma and Vega limits are significantly contracted, while Delta limits may be widened to absorb localized spot gaps.
    *   **DIVERGENCE_STRATEGY_MODE**: Triggered by high VVIX or RDR exceeding its upper boundary. This represents a severe environment where short volatility/gamma risk is drastically reduced (e.g., 95% reduction for Vega/Gamma), and Delta buffers are expanded to prevent over-hedging churn.

## Implementation
The engine is implemented by the [[../entities/regimeriskscaler-class.md|RegimeRiskScaler class]], which encapsulates the logic for calculating multipliers and applying scaling rules.

## Related Concepts
*   [[../concepts/portfolio-greek-limits.md|Portfolio Greek Limits]]
*   [[../concepts/options-greeks.md|Options Greeks]]
*   [[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio (RDR)]]
*   [[../concepts/gex.md|Gamma Exposure (GEX)]]
*   [[../concepts/vvix.md|Vol-of-Vol Index (VVIX)]]