---
tags: [options, features, gamma, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# ATM Gamma Velocity

**Definition:** This feature approximates the rate of change of At-The-Money (ATM) gamma with respect to a change in the underlying spot price (dΓ/dS). It serves as a proxy for how frequently dealers might need to rehedge their positions as the spot price moves.

**Calculation:**
1.  Identify the ATM strike.
2.  Approximate dΓ/dS using a central difference:
    `dΓ/dS ≈ (gamma(K_atm + 1 strike) - gamma(K_atm - 1 strike)) / (2 × strike_increment)`

**Units:** Gamma per dollar.

**Significance:**
*   A higher `atm_gamma_velocity` suggests that dealers' gamma exposure changes rapidly with small movements in the underlying. This implies more frequent and potentially larger rehedging activities.
*   This feature is a key input for the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], particularly in distinguishing between [[../concepts/market-regime-mean-reverting.md|mean-reverting]] and [[../concepts/market-regime-gamma-squeeze.md|gamma squeeze]] regimes, where rehedge frequency plays a significant role in price dynamics.

---