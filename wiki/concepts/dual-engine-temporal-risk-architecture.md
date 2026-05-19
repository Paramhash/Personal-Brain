---
tags: [risk-management, options-trading, market-microstructure, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "temporal_risk_architecture.md"
---
# Dual-Engine Temporal Risk Architecture

## Overview
The Dual-Engine Temporal Risk Architecture is a framework designed to manage risk in options trading by decoupling the analysis of short-term (intraday) and long-term (macro) market regimes. It addresses the challenge where the explosive nominal gamma of [[./zero-days-to-expiration-0dte.md|Zero Days To Expiration (0DTE)]] options can overwhelm and distort structural signals from longer-dated contracts if a single, omnibus risk metric is used.

The core thesis is that immediate intraday liquidity is dominated by 0DTE options, while macro positioning is dictated by longer-dated options. Therefore, a single "Regime Divergence Ratio (RDR)" is insufficient. The architecture proposes two distinct engines: a **Tactical Engine** for intraday management and a **Strategic Engine** for baseline capital allocation.

## The Dual-Engine Architecture

### 1. Tactical Engine: 0DTE Delta/Gamma Matrix
This engine focuses on immediate, intraday market dynamics, monitoring order flow, dealer pinning, and localized gamma squeezes. It exclusively considers options expiring $\le 1$ Day to Expiration ($T \le 1$).

**Formula for Tactical Regime Divergence Ratio ($\text{RDR}_{\text{Tactical}}$):**
$$\text{RDR}_{\text{Tactical}} = \frac{|\text{Index GEX}_{\le 1\text{DTE}}|}{\sum |\text{Component GEX}_{\le 1\text{DTE}}|}$$
*   **Primary Objective:** Dictates Intraday Delta Buffers and real-time Execution Feasibility.
*   **Operational Behavior:** A spike or drop in $\text{RDR}_{\text{Tactical}}$ outside its core band signals dominance by localized programmatic intraday flows. The system responds by widening intraday Delta limits to mitigate risks from mechanical delta-hedging or high-frequency dealer pinning.
*   **Key Metric:** [[./gamma-exposure-gex.md|Gamma Exposure (GEX)]] for 0DTE options.

### 2. Strategic Engine: Term-Weighted Macro Matrix
This engine monitors structural asset-class positioning, systematic institutional overlays, and macro volatility regimes. It explicitly strips out 0DTE contracts, focusing on horizons from 1 week out to monthly/quarterly expiries ($T > 7\text{D}$).

**Formula for Strategic Regime Divergence Ratio ($\text{RDR}_{\text{Strategic}}$):**
$$\text{RDR}_{\text{Strategic}} = \frac{\sum_{i} w_i \cdot |\text{Index GEX}_i|}{\sum_{j} w_j \cdot \left( \sum |\text{Component GEX}_{j,i}| \right)}$$
Where $w$ is a duration-weighting factor, often based on [[./dollar-vega.md|Dollar-Vega ($\mathcal{V}_{\$}$)]] or time-to-expiration ($1/\sqrt{T}$).
*   **Primary Objective:** Dictates baseline Capital Capacity, Vega Limits, and Theta Targets.
*   **Operational Behavior:** This engine changes slowly, preventing aggressive short-premium sizing if the underlying basket is structurally fragile, even if 0DTE flows appear calm.
*   **Key Metrics:** [[./gamma-exposure-gex.md|Gamma Exposure (GEX)]] for longer-dated options, weighted by [[./dollar-vega.md|Dollar-Vega]].

## Asymmetric Greek Allocation via Temporal Decoupling
This architecture allows for dynamic and decoupled adjustment of risk limits for different option Greeks:

*   **Vega Limits:** Governed strictly by $\text{RDR}_{\text{Strategic}}$. Since 0DTE options have virtually no Vega, portfolio-level Vega exposure should ignore 0DTE volume. If $\text{RDR}_{\text{Strategic}}$ indicates an Index-Dominated macro regime (e.g., heavy institutional put buying across monthly expiries), Vega limits contract systematically.
*   **Delta Buffers:** Governed strictly by $\text{RDR}_{\text{Tactical}}$. Delta risk is an immediate, path-dependent phenomenon. If $\text{RDR}_{\text{Tactical}}$ signals a Component-Dominated regime (e.g., a single-stock gamma squeeze), the system instantly widens portfolio Delta limits to prevent chasing noise.
*   **Gamma Limits:** Under joint control via a multiplier product. Gamma bridges both short-term acceleration and structural risk. The final Gamma multiplier ($M_{\Gamma}$) is a product of both engines:
    $$M_{\Gamma} = M(\text{RDR}_{\text{Tactical}}) \times M(\text{RDR}_{\text{Strategic}})$$
    If either engine indicates a tail-risk or non-coherent regime state, aggregate Gamma capacity is immediately restricted.

## Operational Advantages
1.  **Prevents Noise Contamination:** Isolates structural risk signals from the massive but fleeting volume of 0DTE options, ensuring core capital allocation is based on fundamental market structure.
2.  **Optimizes Execution Windowing:** Enables systematic trading of index premium based on stable macro setups, while using the tactical engine to dynamically adjust intraday stops and stop-out frequencies.
3.  **Implements Structural Dispersion Cleanly:** Facilitates true Variance Risk Premium (VRP) capture by focusing on sticky, longer-dated implied correlations, free from intraday tracking error introduced by 0DTE flows.