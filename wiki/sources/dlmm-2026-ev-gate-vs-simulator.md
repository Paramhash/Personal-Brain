---
domain: cl-market-making
tags:
- dlmm
- ev-gate
- simulator
- cost-model
- lvr
- hedging
- fee-economics
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-vs-simulator-2026-10-01.md
ingest_hashes:
- 3327573c78a220bf
---
# EV gate vs simulator: why the gate's cost side is an order of magnitude low (DLMM Team, 2026)
**Type:** paper
## Claim
The DLMM [[ev-gate]]'s cost calculations for [[cl-position|concentrated liquidity]] positions are significantly underestimated compared to a detailed model and simulator. This discrepancy primarily stems from the gate's failure to account for range-dependent [[loss-versus-rebalancing|LVR]] and its complete omission of a [[hedge-drag|hedge-cost]] term. If measured [[fee-yield]] is ratified without addressing these cost model flaws, the gate would approve unprofitable positions.
## Method and data
The analysis compares three cost models:
1.  The live [[ev-gate]] implementation (`evCalculator.ts`).
2.  A more detailed model described in [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] (`hurdleMath.ts`), used for display only.
3.  A [[dlmm-simulator]] (referenced from `dlmm/reports/cl-policy-report-2026-10-01|CL_POLICY_REPORT_2026-10-01.md`).

The comparison uses live state data from 2026-10-01T13:50:27Z, including a 202-bin window (approx. ±4%), 50 SOL-equivalent capital, a curve shape, a placeholder sigma (1.4e-4/s), and operator-supplied funding (1 bps per 8 hours).
## Key results
*   **Total Cost Discrepancy:**
    *   [[ev-gate]]: 62.5 bps/day (fails against a 10 bps placeholder).
    *   [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model: 442.9 bps/day.
    *   [[dlmm-simulator]] break-even: 270–330 bps/day.
*   **LVR Calculation Flaw:** The [[ev-gate]] calculates [[loss-versus-rebalancing|LVR]] as `((σ_s²·3600/8)·1.8)·24 h`, effectively `0.225·σ_d²`, which is [[uniswap-v2|Uniswap v2]]'s full-range LVR multiplied by a fixed [[dlmm-concentration-multiplier]] of 1.8. This implies an effective [[rho-bar]] of 0.45. In contrast, the live 202-bin curve has an actual [[rho-bar]] of ~21.7, making the gate's LVR calculation approximately **48 times lower** than the model's.
*   **Missing Hedge Cost:** The [[ev-gate]]'s `net_ev` calculation (`fees − LVR − funding − rent`) completely omits the cost of [[delta_hedging|delta-hedging]] the position. For a narrow range with high gamma, this cost is substantial, estimated by the simulator and model at 110–190 bps/day and 190.8 bps/day, respectively.
*   **Model vs. Simulator Residual:** The [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model overestimates the simulator's LVR and hedge costs by a factor of 1.4–3.2 (median ~2). A hypothesis suggests this is because the model evaluates [[rho-bar]] once at the open (where density is highest), while the simulator integrates over the price path, accounting for density changes and out-of-range periods.
*   **Consequence of Ratification:** Measured [[fee-yield]] for top policies is 80–141 bps/day. If this is ratified into the current [[ev-gate]], it would pass positions that the simulator indicates lose 150–240 bps/day.
## Assumptions and limits
*   The [[ev-gate]] is currently "safe" only because its placeholder [[fee-yield]] is low.
*   The analysis assumes the [[dlmm-simulator]] provides a more accurate representation of actual costs.
*   The proposed fixes (replacing the 1.8 constant with actual [[rho-bar]], adding a [[hedge-drag|hedge-taker]] term, and calibrating to the simulator) are necessary before [[adr-050-fee-yield-from-on-chain-bin-fee-counters|Route 4]] fee yield ratification.
## Concepts introduced or used
[[ev-gate]], [[dlmm-simulator]], [[loss-versus-rebalancing]], [[hedge-drag]], [[dlmm-bins]], [[economic-hurdle-rate-cl]], [[fee-yield]], [[adr-046-real-time-hurdle-rate-restates-the-ev-gate]], [[adr-050-fee-yield-from-on-chain-bin-fee-counters]], [[dlmm-concentration-multiplier]], [[rho-bar]], [[delta_hedging]], [[cl-position]], [[uniswap-v2]], [[constant-function-market-maker]], [[inventory-accounting]], [[slippage]], [[transaction-latency]], [[network-congestion]], [[sol-execution-reserve]], [[sol-rent-reserve]], [[sol-inventory]], [[markouts]], [[rebalancing-arbitrage]], [[rebalancing-strategy]], [[cl-rebalancing-condition]], [[cl-hedge-target]], [[cl-provider-strategy]], [[cl-entry-strategy]], [[cl-exit-strategy]], [[cl-position-monitoring]], [[cl-success-metrics]], [[capital-allocation-liquidity-shape]], [[capital-allocation-rule-cl]], [[decision-gate-cl-bot]], [[sigma-forecast-error]], [[usdc-inventory]], [[warehouse-manager-cl-inventory-strategy]], [[zero-growth-baseline]], [[adr-040-sunk-deployment-rent-is-an-ev-term]], [[adr-034-range-width-rule-for-fine-binned-pools]], [[cl-policy-report-2026-10-01]], [[finding-ev-gate-calibration-2026-10-01]], [[finding-f-026-the-ev-gate-has-no-rent-term-so-wider-ranges-look-cheaper-than-they-are]], [[blueprint-ev-policy]], [[blueprint-range-planning]], [[blueprint-hedge-engine]], [[blueprint-risk-guardrails]], [[blueprint-liquidity-position-manager]], [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]], [[m04-lvr-and-impermanent-loss]], [[m08-hedging-lp-exposure]], [[m05-fee-economics]], [[m03-bin-based-cl-dlmm]], [[m07-inventory-and-market-making-theory]], [[m11-strategic-lps-and-the-decision-rule]], [[m10-timing-as-regime-conditional-deployment]], [[m02-concentrated-liquidity-math]], [[m01-amm-fundamentals]], [[m09-perpetuals-and-funding]], [[m06-volatility-estimation-and-forecasting]]