---
tags: ["options-greeks", "vega", "gamma", "delta", "theta", "risk-limits", "portfolio-management", "dynamic-hedging"]
created: 2023-10-27
reviewed: false
source_origin: "../sources/dispersion-gex-framework-document.md"
---
# Dynamic Greek Limits Scaling

The **Dynamic Greek Limits Scaling** is a critical application of the [[../concepts/dispersion-based-gex-framework.md|Dispersion-Based GEX Framework]]. Rather than uniform risk contraction, this framework adjusts portfolio Greek boundaries asymmetrically based on the prevailing [[../concepts/market-regimes-rdr.md|market regime]] identified by the [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio (RDR)]]. This accounts for directional velocity, path dependency, and correlation dynamics unique to each regime.

## Independent Asymmetric Greek Scaling Matrix

The following matrix outlines how key options Greeks (Vega, Gamma, Delta, Theta) are adjusted across the three RDR-defined market regimes:

| Greek Profile | Component Dominated ($RDR < 0.5$) | Coherent Band ($0.5 \le RDR \le 2.0$) | Index Dominated ($RDR > 2.0$) |
| :--- | :--- | :--- | :--- |
| **Vega ($\mathcal{V}$)** | **Aggressive Contraction ($0.25x$)**<br>*Reason:* Prevent blowout from correlation spikes and unpriced single-stock tail risk. | **Standard Baseline ($1.0x$)**<br>*Reason:* Maximum asset deployment for structured variance harvesting. | **Tapered Contraction ($0.50x$)**<br>*Reason:* Mitigate risk of index level systemic implied volatility expansion. |
| **Gamma ($\Gamma$)** | **Standard / Moderate Buffer ($0.85x$)**<br>*Reason:* Single stocks localized, index remains relatively constrained. | **Standard Baseline ($1.0x$)**<br>*Reason:* Stable pinning conditions across the structural corridor. | **Aggressive Contraction ($0.10x$)**<br>*Reason:* Eliminate path dependency risk under massive programmatic flows. |
| **Delta ($\Delta$)** | **Tightened Limits ($0.75x$)**<br>*Reason:* Protect against micro gaps from underlying single-stock breakdown. | **Standard Baseline ($1.0x$)**<br>*Reason:* Symmetric mean-reverting tracking across core bands. | **Aggressive Expansion ($1.75x$)**<br>*Reason:* Avoid mechanical over-hedging and slippage against sweeping macro trends. |
| **Theta ($\Theta$)** | **Tapered Reduction ($0.60x$)**<br>*Reason:* Decay is insufficient to justify holding unpriced correlation risk. | **Standard Baseline ($1.0x$)**<br>*Reason:* Premium capture perfectly balanced with structural decay metrics. | **Symmetric Scaling ($M_{RDR}x$)**<br>*Reason:* Scaled strictly in proportion to realized capital constraints. |

## Implementation Protocol Considerations

*   **Data Normalization:** Component [[../concepts/gamma-exposure-gex.md|GEX]] values must be capitalized or liquidity-weighted to prevent distortion from hyper-liquid individual stocks. The denominator of the RDR should represent the net effective option liquidity pool of the basket.
*   **Intraday Recalibration:** While single-stock component values update continuously, structural rebalancing of Greek limits should typically occur on a **2-Hour Rolling Average** to smooth out localized execution block-trade noise. However, instantaneous intraday breakout capabilities are maintained by the directional GEX filters (as described in [[../concepts/regime-divergence-ratio-rdr.md|RDR's mathematical adjustments]]).

This dynamic approach allows portfolio managers to optimize premium harvesting during stable periods and aggressively reduce exposure during periods of structural market stress or imbalance, aligning risk with the true underlying market mechanics.

---
### Related Concepts
*   [[../concepts/dispersion-based-gex-framework.md|Dispersion-Based GEX Framework]]
*   [[../concepts/regime-divergence-ratio-rdr.md|Regime Divergence Ratio (RDR)]]
*   [[../concepts/market-regimes-rdr.md|Market Regimes (RDR)]]
*   [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]]