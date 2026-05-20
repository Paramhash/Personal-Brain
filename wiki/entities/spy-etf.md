---
tags: [entity, etf, equity, options, underlying]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# SPY ETF

The SPDR S&P 500 ETF Trust (SPY) is an exchange-traded fund (ETF) that seeks to track the investment results of the S&P 500 Index. It is one of the largest and most actively traded ETFs globally, providing investors with exposure to the performance of the [[../entities/spx-index.md|S&P 500]].

Options on SPY are also highly liquid and are a key focus of the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]] for analyzing near-expiry market microstructure dynamics (7DTE-1DTE window).

**Key Characteristics in Context:**
*   **Dividend Yield:** For accurate options pricing and greeks calculations, a `dividend_yield=0.013` (approximate annual yield) must be passed to `enrich_contract_snapshot` when processing SPY options data. This is a crucial constraint to avoid using the default 0.0.
*   **Data Source:** Historical SPY options data is pulled from [[../entities/thetadata.md|ThetaData]]. Live data is consumed via [[../entities/dxfeed.md|dxFeed]].

---