---
tags: [options, features, open-interest, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# OI Concentration Ratio

**Definition:** This feature measures the concentration of Open Interest (OI) at strikes immediately surrounding the At-The-Money (ATM) level for a given expiration. It indicates how much options activity is focused on strikes very close to the current spot price.

**Calculation:**
1.  **OI at ATM ± 1 strike:** Sum of Open Interest for all calls and puts at the ATM strike, and one strike above and one strike below ATM.
2.  **Total Chain OI at this expiration:** Sum of Open Interest for all calls and puts across all strikes for the current expiration.
3.  **Feature Value:** `(OI at strikes within ±1 strike of ATM) / (Total chain OI at this expiration)`

**Range:** `[0, 1]`

**Significance:**
*   A high value (closer to 1) indicates that a significant portion of the open interest for the near-expiry cycle is concentrated very close to the current spot price.
*   This high concentration suggests increased "pin risk," where market makers may have strong incentives to keep the underlying price near these strikes to manage their delta and gamma exposures as expiration approaches.
*   It is a crucial feature for identifying the [[../concepts/market-regime-pinning.md|pinning]] regime within the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]].

---