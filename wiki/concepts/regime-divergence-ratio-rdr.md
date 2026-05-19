---
tags: ["rdr", "dispersion", "gamma-exposure", "market-analysis", "quantitative-finance", "risk-metrics"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/dispersion-gex-framework-document.md"
---
# Regime Divergence Ratio (RDR)

The **Regime Divergence Ratio (RDR)** is a core metric within the [[../concepts/dispersion-based-gex-framework.md|Dispersion-Based GEX Framework]]. It serves as a structural dispersion monitor, quantifying the divergence between index-level derivatives positioning and single-stock derivatives positioning.

## Definition

The RDR is formally defined as the ratio of Index [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]] to the aggregate Gamma Exposure of its underlying constituents:

$$RDR = \frac{\text{Index GEX}}{\sum \text{Component GEX}}$$

This ratio directly exposes the mechanical equilibrium between macro-index systematic hedging and single-stock speculative behavior, allowing for dynamic risk scaling based on structural market decoupling.

## Mathematical Normalization & Adjustments

To ensure robust deployment in automated algorithmic risk systems, the RDR calculation requires two structural adjustments:

### 1. Absolute Value Magnitude Adjustment

Raw GEX calculations preserve signs (positive for long dealer gamma, negative for short dealer gamma). A negative RDR (e.g., from negative Index GEX and positive Component GEX) can disrupt standard scaling equations. To evaluate structural dominance safely, the calculation engine must use the **Absolute Value Magnitude**:

$$RDR_{\text{normalized}} = \frac{|\text{Index GEX}|}{\sum |\text{Component GEX}|}$$

This ensures the ratio always reflects the magnitude of dominance, regardless of the directional sign of GEX.

### 2. Absolute Directional Filter Override

While the absolute ratio measures *dominance*, risk limits must also account for *directionality*. A negative Index GEX signifies dealer short-gamma profiles, which act as a volatility accelerator. Therefore, the continuous RDR scaling engine is subordinated to an **Absolute GEX Directional Filter Checklist**:

```
                  +---------------------------------------+
                  |    Calculate Absolute Component RDR   |
                  +-------------------+-------------------+
                                      |
                                      v
                  +---------------------------------------+
                  |        Is Index GEX Negative?         |
                  +-------------------+-------------------+
                                     / \
                             YES    /   \   NO
                                   /     \
                                  v       v
         +--------------------------+   +--------------------------+
         | Trigger Risk Reduction   |   | Proceed with Continuous  |
         | Mode: Hard Vega/Gamma Cap|   | Bi-Symmetric Scaling     |
         +--------------------------+   +--------------------------+
```

If Index GEX is negative, a risk reduction mode is triggered, imposing hard Vega/Gamma caps, overriding the continuous bi-symmetric scaling that would otherwise apply.

## Market Regimes

The RDR dictates three distinct [[../concepts/market-regimes-rdr.md|market regimes]], each with specific implications for portfolio risk and strategy:

*   **Component-Dominated Regime ($RDR < 0.5$):** Characterized by speculative stock-driven frenzies where the index underprices localized basket risk.
*   **Balanced Coherent Regime ($0.5 \le RDR \le 2.0$):** Represents a state where derivatives flows are structurally aligned, optimal for systematic short premium deployment.
*   **Index-Dominated Regime ($RDR > 2.0$):** Driven by massive systematic macro overlays, where market action is dictated by programmatic dealer delta hedging.

---
### Related Concepts
*   [[../concepts/dispersion-based-gex-framework.md|Dispersion-Based GEX Framework]]
*   [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]]
*   [[../concepts/market-regimes-rdr.md|Market Regimes (RDR)]]
*   [[../concepts/dynamic-greek-limits-scaling.md|Dynamic Greek Limits Scaling]]