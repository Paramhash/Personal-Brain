---
tags: [entity, index, equity, options, underlying]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# SPX Index

The S&P 500 Index (SPX) is a stock market index that represents the performance of 500 of the largest publicly traded companies in the United States. It is a market-capitalization-weighted index and is widely regarded as one of the best gauges of large-cap U.S. equities and the overall health of the U.S. stock market.

Options on the SPX index are highly liquid and frequently traded, particularly short-dated expirations. The [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]] is designed to analyze the market microstructure dynamics of SPX options in the 7DTE-1DTE window.

**Key Characteristics in Context:**
*   **AM-Settlement:** SPX options are typically AM-settled on their expiration day. This requires a specific adjustment for `time_to_expiry_years` for DTE=1 observations taken at 15:45 ET, correcting it to `(minutes_to_930_next_day / 525600)`.
*   **Data Source:** Historical SPX options data is pulled from [[../entities/thetadata.md|ThetaData]]. Live data is consumed via [[../entities/dxfeed.md|dxFeed]].

---