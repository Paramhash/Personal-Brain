---
tags: [financial-metrics, market-regimes, risk-indicators]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# Regime Divergence Ratio (RDR)

The **Regime Divergence Ratio (RDR)** is a critical input metric used by the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]] to quantify the current market regime's divergence from a perceived "coherent" or stable state. While its exact calculation method is not detailed in the provided payload, its role as an indicator of market stability or stress is clearly defined.

## Role in Risk Management
The RDR serves as the primary continuous input for the [[../concepts/bi-symmetric-sigmoid-decay-function.md|Bi-Symmetric Sigmoid Decay Function]], which in turn calculates a baseline risk multiplier.

*   **Coherent Regime**: When the RDR is within a defined range (e.g., between `theta_lower` and `theta_upper`), the market is considered "coherent," and risk limits are scaled smoothly, often allowing for higher exposures.
*   **Divergent Regimes**: As the RDR moves outside this coherent band, particularly above `theta_upper`, it signals increasing market divergence or stress. This leads to a rapid reduction in the risk multiplier, resulting in tighter [[../concepts/portfolio-greek-limits.md|portfolio Greek limits]].

## Impact on Risk Limits
A higher RDR value, especially one exceeding the `theta_upper` threshold, indicates a more volatile or uncertain market environment. In such scenarios, the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]] will significantly reduce permitted risk exposures, particularly for [[../concepts/options-greeks.md|Greeks]] associated with short volatility or gamma positions.

## Parameters
The RDR interacts with the following parameters within the risk engine:
*   `theta_lower`: The lower boundary of the coherent RDR regime.
*   `theta_upper`: The upper boundary of the coherent RDR regime.

These parameters define the range within which the market is considered relatively stable and where risk limits are less aggressively curtailed by the RDR multiplier alone.