---
domain: cl-market-making
tags:
- dlmm
- inventory-control
- risk-management
- strategy
- market-making
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- f0b251074c478259
---
# Warehouse Manager CL Inventory Strategy
**In one line:** A comprehensive policy for a Concentrated Liquidity (CL) market-making bot, focusing on hierarchical inventory management, disciplined capital allocation, and robust entry/exit conditions to ensure operational survival and achieve positive equity growth.
## Intuition
The strategy treats the market-making bot as managing distinct inventories: [[sol-inventory]] (for operations and volatile exposure), [[usdc-inventory]] (stable operating capital), and a temporary [[cl-position]] (for fee generation). The core idea is to prioritize operational continuity by reserving capital, only deploying surplus funds, and actively managing risk through hedging and proactive exit triggers. Success is defined hierarchically, with operational safety as paramount, followed by absolute equity growth and outperformance against a passive [[hodl-benchmark]].
## Mechanism / math
The strategy defines specific rules across the bot's lifecycle:
*   **Inventory Management:**
    *   `SOL_free = SOL_wallet - SOL_rent_reserve - SOL_execution_reserve`
    *   Hard constraints: `SOL_t >= SOL_min` and `USDC_t >= USDC_min`
*   **Deployment Boundaries:** Uses a [[buffered-policy-envelope]] as the hard deployment boundary, with a narrower [[sigma-derived-deployed-window]] for actual CL placement.
*   **[[cl-entry-strategy]]:** Requires untouched reserves, valid [[market-boundaries-cl]], active bin within the buffered envelope, valid range constraints, and [[expected-fees-cl]] exceeding the [[economic-hurdle-rate-cl]]:
    $$
    \text{Expected fees} > \text{LVR} + \text{hedge funding} + \text{rent} + \text{gas} + \text{slippage} + \text{risk premium}
    $$
*   **[[capital-allocation-rule-cl]]:** `C_deploy = min(C_economic_limit, C_reserve-safe_limit, C_collateral-safe_limit)`
*   **[[cl-position-monitoring]]:** Continuous tracking of active bin, price, distance to boundaries, volatility, [[gex-regime]], fees, projected [[lvr]], hedge error, reserves, and expected net equity.
*   **[[cl-hedge-target]]:** `q_t^* = -x_t`, where $x_t$ is the SOL held by the CL position.
*   **[[cl-rebalancing-condition]]:** Rebalance when `|q_t^* - q_t| > \epsilon_{base}` and collateral is sufficient.
*   **[[cl-exit-strategy]]:** Triggered by:
    *   [[boundary-threat-exit]]: `d(P_t, B) < execution buffer` (buffer widens with volatility, [[transaction-latency]], price velocity, [[network-congestion]], [[liquidity-concentration]]).
    *   [[negative-economics-exit]]: Projected fees < projected [[lvr]] + funding + exit/redeployment costs.
    *   [[regime-deterioration-exit]]: Off-chain [[gamma-exposure-gex]] signals (e.g., spot near [[zero-gamma-level]], rising volatility, wall envelope movement, range asymmetry, LVR rate > fee production), with hysteresis.
*   **[[cl-closing-procedure]]:** Coordinated sequence of stopping liquidity, withdrawing CL, reconciling inventory, recomputing/resizing hedge, confirming balances, restoring reserves, and calculating final equity.
*   **[[cl-success-metrics]]:**
    *   Hard requirements: Reserves preserved, no collateral breach/liquidation, valid boundaries, reconciled withdrawal.
    *   Primary objective: `E_close > E_start`.
    *   Secondary objective: `E_close > E_HODL_benchmark`.
## Where it matters
This strategy is fundamental for designing and operating automated market-making bots on concentrated liquidity protocols. It informs decisions on capital allocation, risk limits, deployment parameters (range width), hedging policies, and when to enter or exit positions. It ensures the bot's long-term viability by prioritizing operational safety and economic rationality over maximizing short-term yield at all costs.
## Evidence and limits
This document is a policy recommendation from the source, outlining a desired operational framework. It does not present empirical evidence or backtesting results. Its effectiveness relies on the accurate implementation of its components, particularly the forecasting of volatility, LVR, and the reliability of GEX signals. The strategy is designed for a specific CL market-making context, likely involving SOL/USDC pairs.
## Related
[[cl-market-making]]
[[inventory-accounting]]
[[blueprint-ev-policy]]
[[blueprint-risk-guardrails]]
[[adr-index]]
[[m07-inventory-and-market-making-theory]]
[[m08-hedging-lp-exposure]]
[[m05-fee-economics]]
[[m04-lvr-and-impermanent-loss]]
[[blueprint-liquidity-position-manager]]
[[blueprint-hedge-engine]]