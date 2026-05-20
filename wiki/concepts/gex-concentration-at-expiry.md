---
tags: [options, features, gamma-exposure, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# GEX Concentration at Expiry

**Definition:** This feature measures the proportion of Gamma Exposure (GEX) attributed to the current near-expiry options cycle relative to the total GEX across all available expiration cycles for a given underlying.

**Calculation:**
1.  **Per-contract GEX:** `gamma × Open Interest (OI) × 100 × spot²`
2.  **Sum GEX at THIS expiration:** Sum of per-contract GEX for all options expiring on the current date.
3.  **Sum GEX across ALL expirations:** Sum of per-contract GEX for all options across all available expiration dates.
4.  **Feature Value:** `(Sum GEX at THIS expiration) / (Sum GEX across ALL expirations)`

**Range:** `[0, 1]`

**Significance:**
A high value (closer to 1) indicates that the current near-expiry options cycle dominates the overall dealer hedging landscape. This implies that market makers' hedging activities for this specific expiration will have a more pronounced impact on the underlying's price dynamics. It is a key input for the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]] to identify regimes like [[../concepts/market-regime-gamma-squeeze.md|gamma squeeze]] or [[../concepts/market-regime-pinning.md|pinning]].

---