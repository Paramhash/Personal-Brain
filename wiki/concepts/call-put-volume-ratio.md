---
tags: [options, features, volume, order-flow, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Call/Put Volume Ratio

**Definition:** This feature quantifies the relative trading activity between call and put options at or near the At-The-Money (ATM) strikes for a given expiration. It serves as an indicator of directional market sentiment or order flow.

**Calculation:**
1.  Sum the volume of calls traded within ±2 strikes of ATM.
2.  Sum the volume of puts traded within ±2 strikes of ATM.
3.  **Feature Value:** `(Sum of call volume) / (Sum of call volume + Sum of put volume)`

**Range:** `[0, 1]`

**Significance:**
*   A value above `0.6` suggests call-heavy flow, indicating bullish sentiment or demand for upside exposure.
*   A value below `0.4` suggests put-heavy flow, indicating bearish sentiment or demand for downside protection.
*   Values closer to `0.5` suggest balanced flow.
*   This feature is valuable for the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]] in identifying regimes where strong directional pressure might be building, such as a [[../concepts/market-regime-gamma-squeeze.md|gamma squeeze]] (which can be initiated or exacerbated by heavy directional buying/selling).

---