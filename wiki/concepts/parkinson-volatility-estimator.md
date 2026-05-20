---
tags: [volatility, quantitative-finance, statistics, estimators]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Parkinson Volatility Estimator

The Parkinson Volatility Estimator is a method for estimating historical volatility using the high and low prices of a trading period, rather than just the closing prices. It is considered more efficient than using close-to-close returns because it incorporates more information about price movements within the period.

The formula for the Parkinson estimator (σ_park) for a single period is:

`σ_park = sqrt( (1 / (4 × ln(2))) × (ln(H/L))² )`

Where:
*   `H` = High price for the period
*   `L` = Low price for the period
*   `ln` = Natural logarithm

For a series of `N` periods, the formula is:

`σ_park = sqrt( (1 / (4 × N × ln(2))) × Σ (ln(H_i/L_i))² )`

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], the Parkinson estimator is used to compute the [[../concepts/realized-vol-intraday.md|Realized Volatility Intraday]] feature. It is applied to 1-minute OHLC bars from session open to the snapshot time and then annualized by multiplying by `sqrt(252 × 6.5 × 60)`.

---