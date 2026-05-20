---
tags: [volatility, features, quantitative-finance, intraday]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Realized Volatility Intraday

**Definition:** This feature quantifies the actual volatility observed in the underlying asset's price movements during the current trading session, up to the snapshot time. It provides a direct measure of how much the price has fluctuated intraday.

**Calculation:**
1.  Utilize 1-minute OHLC (Open, High, Low, Close) bars from the session open to the current snapshot time.
2.  Apply the [[../concepts/parkinson-volatility-estimator.md|Parkinson Volatility Estimator]] to these 1-minute bars.
3.  Annualize the result by multiplying by `sqrt(252 × 6.5 × 60)`.

**Significance:**
*   `realized_vol_intraday` is a direct indicator of market turbulence and price action.
*   It is a primary distinguishing feature for the three market regimes in the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]]:
    *   **Lowest values:** Associated with the [[../concepts/market-regime-pinning.md|pinning]] regime.
    *   **Middle values:** Associated with the [[../concepts/market-regime-mean-reverting.md|mean-reverting]] regime.
    *   **Highest values:** Associated with the [[../concepts/market-regime-gamma-squeeze.md|gamma squeeze]] regime.
*   The state labels of the HMM are explicitly anchored to the ordering of the mean of this feature across states.

---