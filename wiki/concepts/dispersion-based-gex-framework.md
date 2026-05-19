---
tags: ["risk-management", "options-trading", "gamma-exposure", "market-regimes", "portfolio-management", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/dispersion-gex-framework-document.md"
---
# Dispersion-Based GEX Framework

The **Dispersion-Based GEX Framework** is a risk architecture designed for dynamic portfolio-level Greek limits. It moves beyond generic volatility tracking by employing a **structural dispersion monitor** based on the [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio (RDR)]].

This framework aims to expose the mechanical equilibrium between macro-index systematic hedging and single-stock speculative behavior. By doing so, it allows a portfolio to scale risk dynamically based on structural market decoupling, rather than relying on static risk parameters.

## Core Principles

*   **Structural Dispersion Monitoring:** The RDR acts as a direct measure of the divergence between index-level and single-stock derivatives positioning.
*   **Dynamic Risk Scaling:** Portfolio risk, specifically [[../concepts/dynamic-greek-limits-scaling.md|options Greeks]], are adjusted asymmetrically based on the prevailing market regime identified by the RDR.
*   **Regime-Based Adaptation:** The market is categorized into three distinct regimes—Component-Dominated, Balanced Coherent, and Index-Dominated—each dictating specific risk responses.

## Key Components

1.  **[[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio (RDR)]]:** The central metric, defined as the ratio of Index [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]] to the aggregate GEX of its underlying constituents. It includes specific mathematical normalizations to ensure robust algorithmic deployment.
2.  **[[../concepts/market-regimes-rdr.md|Market Regimes]]:** Three distinct market states (Component-Dominated, Balanced Coherent, Index-Dominated) identified by the RDR, each with unique implications for portfolio risk.
3.  **[[../concepts/dynamic-greek-limits-scaling.md|Dynamic Greek Limits Scaling]]:** An asymmetric matrix that adjusts portfolio Vega, Gamma, Delta, and Theta limits based on the identified RDR regime, accounting for directional velocity, path dependency, and correlation dynamics.
4.  **Implementation Protocol:** Guidelines for data normalization (e.g., liquidity-weighting components) and intraday recalibration to ensure practical and stable deployment.

This framework provides a sophisticated approach to managing options portfolios by aligning risk exposure with the underlying structural dynamics of the market.

---
### Related Concepts
*   [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]]
*   [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio (RDR)]]
*   [[../concepts/market-regimes-rdr.md|Market Regimes (RDR)]]
*   [[../concepts/dynamic-greek-limits-scaling.md|Dynamic Greek Limits Scaling]]