---
domain: cl-market-making
tags:
- dlmm
- backtesting
- research
- cost-model
- lvr
- hedging
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-vs-simulator-2026-10-01.md
ingest_hashes:
- ae551da850be6ce4
---
# DLMM Simulator
**In one line:** A research tool used to accurately estimate the costs and break-even points for [[cl-market-making|DLMM concentrated liquidity]] policies by integrating over historical or simulated price paths.
## Intuition
The [[dlmm-simulator]] provides a more realistic assessment of [[cl-position|concentrated liquidity position]] profitability compared to simplified analytical models. It does this by simulating the behavior of a liquidity position and its associated hedging activities over time, capturing dynamic effects that static models might miss.
## Key facts
*   **Comprehensive Cost Modeling:** The simulator accounts for various cost components, including [[loss-versus-rebalancing|LVR]], [[hedge-drag|hedge costs]], [[m09-perpetuals-and-funding|funding rates]], and fixed costs like rent, [[slippage]], and gas.
*   **Path Integration:** Unlike static models that might evaluate metrics at a single point in time (e.g., at position open), the simulator integrates these costs and revenues over the entire price path. This allows it to capture how factors like [[rho-bar|value density]] change as the price moves within and out of the [[dlmm-bins|liquidity range]].
*   **Benchmark for Live Systems:** It serves as a benchmark for evaluating the accuracy of live decision-making components, such as the [[ev-gate]].
*   **Policy Evaluation:** Used to test and compare different [[cl-provider-strategy|liquidity provision policies]] (e.g., different [[sigma-derived-deployed-window|range widths]], hedge bands) under various market conditions.
## How it is used here
In the context of the "EV gate vs simulator" finding, the [[dlmm-simulator]] was used to:
*   **Quantify Discrepancies:** Highlight the significant underestimation of costs by the live [[ev-gate]], particularly for [[loss-versus-rebalancing|LVR]] and [[hedge-drag|hedge costs]].
*   **Provide Realistic Benchmarks:** Offer a more accurate estimate of the true break-even points for top [[cl-policy-report-2026-10-01|DLMM policies]] (e.g., 270–330 bps/day).
*   **Inform Model Calibration:** Identify biases in other models (e.g., the [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model overestimating simulator costs by ~2x), suggesting areas for calibration.
*   **Guide System Improvements:** Demonstrate the necessity of updating the [[ev-gate]]'s cost model to prevent the deployment of unprofitable positions.
## Related
[[ev-gate]], [[loss-versus-rebalancing]], [[hedge-drag]], [[economic-hurdle-rate-cl]], [[cl-position]], [[dlmm-bins]], [[rho-bar]], [[sigma-derived-deployed-window]], [[dlmm-2026-ev-gate-vs-simulator]], [[cl-policy-report-2026-10-01]], [[adr-043-research-simulator-reads-archive-offline]], [[blueprint-backtest-research]], [[m04-lvr-and-impermanent-loss]], [[m08-hedging-lp-exposure]]