yaml
---
tags: ["data-provider", "financial-data", "options-data", "market-data"]
created: 2023-10-27
reviewed: false
source_origin: "maopm_horizon_spread_blueprint.md"
---
```
# ThetaData

**ThetaData** is a financial data provider specializing in options market data. It offers services tailored for quantitative analysis and trading systems, particularly those requiring pre-processed or high-level derivatives data.

Key features and characteristics of ThetaData include:
*   **Data Feed Type:** REST API for historical and on-demand snapshot data; WebSocket streaming for real-time trades and quotes.
*   **Granularity:** Tick-level contract events for STANDARD and PRO historical tiers; real-time quote and trade streaming for STANDARD and PRO.
*   **Chain Architecture:** The `expiration` parameter accepts a specific date (`YYYY-MM-DD`) or `*` for all expirations, allowing a full options chain for any underlying to be retrieved in a single call.
*   **Implied Volatility / Greek Engines:** ThetaData pre-computes implied volatility and Greeks (1st, 2nd, and 3rd order) server-side and returns them per contract, eliminating the need for a client-side BSM/numerical IV solver. Historical IV and 1st-order Greeks require STANDARD tier; 2nd and 3rd-order Greeks (historical and real-time snapshot) require PRO tier.
*   **Compute Overhead for Client:** Moderate for horizon spread use cases. ThetaData returns per-contract IV and prices keyed to **actual expiration dates** — not constant-maturity surfaces. To compute BKM model-independent variance V_Q(T) at a target tenor (e.g., 30d or 180d), the client must: (1) query the full chain for the two expirations bracketing the target tenor, (2) apply BKM integration over the strike domain, and (3) time-interpolate the resulting variance estimates to the exact target tenor. No integrated variance profiles are pre-computed by ThetaData.
*   **Subscription Tiers (Options):** FREE (EOD only) / VALUE (1-minute resolution, real-time quote snapshots) / STANDARD (tick-level historical, real-time quotes and trades, historical IV and 1st-order Greeks) / PRO (tick-level from 2012-06-01, real-time 2nd-order Greeks snapshots via `option_snapshot_greeks_second_order`, unlimited trade streaming).

For systems like the [MAOPM architecture for signal fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md), ThetaData is the recommended provider for horizon spread computation. The **minimum viable tier is VALUE** (real-time quote snapshots sufficient for BKM integration from raw option prices). **PRO tier** adds pre-computed per-contract `implied_vol`, eliminating client-side BSM solving across hundreds of strikes per expiration and materially reducing pipeline latency.

---