---
tags: [entity, data-provider, market-data, options-data, historical-data]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# ThetaData

ThetaData is a financial data provider specializing in historical options and equities data. It offers a Python client (`thetadata` pip package) to access its API (`api.thetadata.us`).

In the context of the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], ThetaData is the primary source for building the historical corpus:
*   **Data Pulled:** SPX and SPY weekly expirations from 2022-01-01 to 2026-04-30.
*   **Granularity:** Full options chain snapshots (bid, ask, mid, volume, OI, gamma, delta, IV) and underlying 1-minute OHLC bars.
*   **Sampling:** Specific intraday times (09:35, 10:30, 11:30, 12:30, 13:30, 14:30, 15:00, 15:45 ET) for each DTE from 7 down to 1.
*   **VIX Data:** Can also be used to source VIX data via `index_option_snapshot` for model tiering.

The `scripts/pull_historical.py` module is responsible for interacting with the ThetaData API to collect and store this raw historical data.

---