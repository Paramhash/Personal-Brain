---
tags: [options, features, implied-volatility, term-structure, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# ATM IV DTE Slope

**Definition:** This feature measures the difference in At-The-Money (ATM) Implied Volatility (IV) between the current near-expiry options cycle and the next available (longer DTE) expiration cycle. It captures the slope of the implied volatility term structure at the ATM strike.

**Calculation:**
1.  Identify the ATM IV for the current expiration.
2.  Identify the ATM IV for the next available expiration (with a longer DTE).
3.  **Feature Value:** `(ATM IV at this expiration) - (ATM IV at the NEXT expiration)`
4.  If only one expiration is available, the value is `0`.

**Significance:**
*   A positive value indicates that near-expiry ATM IV is elevated compared to the next expiration, suggesting heightened short-term volatility expectations or demand for short-dated options.
*   A negative value suggests the opposite, with longer-dated IV being higher.
*   This feature helps the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]] assess whether the market is pricing in immediate volatility spikes or a more normalized term structure, contributing to the identification of regimes like [[../concepts/market-regime-gamma-squeeze.md|gamma squeeze]] (often associated with elevated front-month IV) or [[../concepts/market-regime-pinning.md|pinning]] (which might see a flattening or inversion of the front end).
*   **Constraint:** This is the only feature allowed to use BSM-derived IV (`vendor_iv` or `solved_iv` from `vol_solver.py`).

---