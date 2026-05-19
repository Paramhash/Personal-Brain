---
tags: ["source", "framework-document", "quantitative-finance", "risk-management"]
created: 2023-10-27
reviewed: false
source_origin: "dispersion_gex_framework.md"
---
# Dispersion-Based GEX Framework Document

This document serves as the foundational source for the [[../concepts/dispersion-based-gex-framework.md|Dispersion-Based GEX Framework]]. It formalizes a risk architecture that utilizes the Regime Divergence Ratio (RDR) to dynamically manage portfolio-level Greek limits.

## Overview

The document outlines the structural thesis behind using the RDR as a dispersion monitor, detailing its calculation, necessary mathematical adjustments for algorithmic deployment, and its role in identifying distinct market regimes. It further specifies an independent asymmetric Greek scaling matrix, providing concrete rules for adjusting Vega, Gamma, Delta, and Theta based on these regimes. Practical implementation protocols, including data normalization and recalibration frameworks, are also discussed.

## Key Information Contained:

*   Definition and formula for the [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio (RDR)]].
*   Description of the three [[../concepts/market-regimes-rdr.md|market regimes]] (Component-Dominated, Balanced Coherent, Index-Dominated) and their implications.
*   Mathematical adjustments for RDR, including the Absolute Value Magnitude Adjustment and the Absolute Directional Filter Override.
*   A matrix detailing [[../concepts/dynamic-greek-limits-scaling.md|dynamic adjustments to options Greeks]] (Vega, Gamma, Delta, Theta) across different RDR regimes.
*   Implementation considerations for data normalization and intraday recalibration.

This document is crucial for understanding the theoretical underpinnings and practical application of the Dispersion-Based GEX Framework for dynamic risk management in options portfolios.

---
### Derived Concepts
*   [[../concepts/dispersion-based-gex-framework.md|Dispersion-Based GEX Framework]]
*   [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio (RDR)]]
*   [[../concepts/market-regimes-rdr.md|Market Regimes (RDR)]]
*   [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]]
*   [[../concepts/dynamic-greek-limits-scaling.md|Dynamic Greek Limits Scaling]]