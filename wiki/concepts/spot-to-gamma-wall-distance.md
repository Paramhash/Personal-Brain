---
tags: [options, features, gamma, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Spot to Gamma Wall Distance

**Definition:** This feature quantifies the relative distance between the current spot price of the underlying asset and the "gamma wall strike" for the current expiration. A gamma wall strike is a strike price where the absolute net gamma exposure (sum of gamma × OI for calls and puts) is maximal for that expiration.

**Calculation:**
1.  **Gamma Wall Strike:** Identify the strike price (`K_gamma_wall`) with the maximum absolute net GEX (`|net_GEX|`) at the current expiration.
2.  **Feature Value:** `(spot - K_gamma_wall) / K_gamma_wall`

**Significance:**
*   **Sign matters:**
    *   A negative value indicates the spot price is below the gamma wall.
    *   A positive value indicates the spot price is above the gamma wall.
*   **Magnitude:** A smaller absolute value suggests the spot price is closer to a significant gamma concentration point.

This feature is crucial for the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]] as it helps in identifying potential [[../concepts/market-regime-pinning.md|pinning]] scenarios (when spot is near a gamma wall) or the proximity to a level that could trigger a [[../concepts/market-regime-gamma-squeeze.md|gamma squeeze]].

---