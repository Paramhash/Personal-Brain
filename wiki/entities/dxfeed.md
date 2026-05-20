---
tags: [entity, data-provider, market-data, real-time-data, options-data]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# dxFeed

dxFeed is a global provider of real-time market data solutions, offering high-performance data feeds for various asset classes, including equities, options, and futures. They specialize in delivering low-latency, high-quality data streams.

In the context of the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], dxFeed serves as the source for live, real-time options chain snapshots. The `data_engine.py` module is responsible for consuming these websocket chain snapshots and packaging them into `ChainSnapshot` dataclasses, which then feed into the HMM's live inference loop (`scripts/run_live.py`).

---