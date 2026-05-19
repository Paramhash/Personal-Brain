---
tags: [mathematics, financial-modeling, sigmoid-function, risk-management]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# Bi-Symmetric Sigmoid Decay Function

The **Bi-Symmetric Sigmoid Decay Function** is a mathematical construct used within the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]] to compute a continuous, non-linear multiplier for risk limits. It is designed to provide a smooth transition of risk capacity, particularly handling tail behaviors where risk capacity asymptotically approaches zero.

## Purpose
This function's primary role is to translate a continuous input metric, such as the [[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio (RDR)]], into a scaling factor (multiplier) that typically ranges between 0.0 and 1.0. This multiplier then dictates how much of the baseline risk limits are permitted.

## Mechanism
The function combines two logistic (sigmoid) components:
1.  **Lower Bound Sigmoid**: `1.0 / (1.0 + exp(-k_lower * (rdr - theta_lower)))`
    *   This component activates as the input `rdr` approaches `theta_lower`, contributing to the initial rise of the multiplier.
2.  **Upper Bound Sigmoid**: `1.0 / (1.0 + exp(-k_upper * (rdr - theta_upper)))`
    *   This component activates as the input `rdr` approaches `theta_upper`, contributing to the decline of the multiplier.

The combined multiplier is derived by subtracting the upper bound sigmoid from the lower bound sigmoid:
`multiplier = sigmoid_l - sigmoid_u`

The result is then clipped to ensure it remains strictly between 0.0 and 1.0. This creates a curve that rises, plateaus, and then decays, effectively defining a "coherent" regime band where the multiplier is high, and rapidly reducing it as the input moves into extreme tails.

## Parameters
*   `theta_lower` (float): The lower boundary of the "coherent" regime, where the multiplier begins to rise significantly.
*   `theta_upper` (float): The upper boundary of the "coherent" regime, where the multiplier begins to decay significantly.
*   `k_lower` (float): Controls the steepness or "speed of risk reduction" as the input approaches the lower boundary. A higher `k_lower` means a faster rise.
*   `k_upper` (float): Controls the steepness or "speed of risk reduction" as the input approaches the upper boundary. A higher `k_upper` means a faster decay.

## Application
This function is central to the `calculate_rdr_multiplier` method within the [[../entities/regimeriskscaler-class.md|RegimeRiskScaler class]], providing the foundational continuous scaling for dynamic risk limits.