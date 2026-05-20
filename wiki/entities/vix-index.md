---
tags: [entity, index, volatility, market-sentiment, options]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# VIX Index

The CBOE Volatility Index (VIX) is a real-time market index that represents the market's expectation of 30-day forward-looking volatility. It is constructed using the implied volatilities of a wide range of S&P 500 index options. Often referred to as the "fear gauge," a higher VIX value generally indicates greater market uncertainty and expected volatility.

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], the VIX index plays a critical role in stratifying the training data and models:
*   **Model Tiers:** The HMMs are trained in two tiers based on the VIX level at the start of each options cycle:
    *   **Tier A:** VIX < 20 (representing lower volatility regimes)
    *   **Tier B:** VIX ≥ 20 (representing higher volatility regimes)
*   **Data Source:** VIX data can be sourced from [[../entities/thetadata.md|ThetaData]] (`index_option_snapshot` for VIX) or [[../entities/polygon-io.md|Polygon.io]].

This stratification allows the model to learn distinct market dynamics that may prevail under different overall volatility environments.

---