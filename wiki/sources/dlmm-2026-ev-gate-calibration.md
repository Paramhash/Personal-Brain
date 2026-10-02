---
domain: cl-market-making
tags:
- ev-gate
- calibration
- lvr
- hedge-drag
- dlmm
- volatility-forecasting
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-calibration-2026-10-01.md
ingest_hashes:
- a96f977bd8746114
---
# EV gate calibration (2026-10-01)
**Type:** article
## Claim
The initial [[ev-gate]] model, using the instantaneous density measure [[rho-0]], fails to accurately estimate [[loss-versus-rebalancing|LVR]] and [[hedge-drag]] due to significant shape dependence and other biases. A revised model incorporating [[rho-bar]] (a life-averaged density), the pool's actual lower [[realized-volatility]], and a [[burst-factor]] for price movements significantly improves accuracy, explaining the previously observed discrepancies and bringing model estimates within 2-3% of simulator results.
## Method and data
The calibration used the `dist-research/` simulator's accounting over a 6 UTC day archive span (2026-09-26 to 2026-10-01), covering two [[adr-033-fee-yield-measurement-route|ADR-033]] sub-windows. It tested 96 $\sigma$-window policies at 50 SOL. The model's inputs were swapped between:
*   **[[rho-0]]**: the active-bin weight divided by the log step (today's model).
*   **[[rho-bar]]**: a life-averaged density derived from the occupation density of driftless Brownian motion.
*   **Oracle $\sigma$**: the $\sigma$ realized over the next 24 hours, used in place of the trailing 24-hour $\sigma$ for form testing.
Ratios of model output to simulator output were calculated for LVR (vs. hedged loss) and hedge drag (vs. taker cost). Scripts from `docs/operations/ev_gate_calibration/` were used.
## Key results
1.  **Shape Dependence (ρ(0) vs. ρ̄):**
    *   [[rho-0]] overstates "Curve" LVR (1.58x) and hedge (2.07x) while understating "BidAsk" LVR (0.36x) and hedge (0.43x).
    *   [[rho-bar]] successfully removes this shape dependence, causing LVR ratios to converge to 1.1-1.5x and hedge ratios to 1.5-1.7x across all shapes.
2.  **Out-of-range accrual:** Found to be negligible, moving medians by $\le$ 0.07.
3.  **Per-day spread:** Largely attributed to [[sigma-forecast-error]]. With trailing $\sigma$, the model/simulator ratio tracks daily volatility inversely. With oracle $\sigma$, 5 of 6 days fall within 0.93–1.36 for LVR.
4.  **Residual form bias (ρ̄, oracle $\sigma$):** Even with [[rho-bar]] and oracle $\sigma$, the model still overstated LVR by 1.3-1.7x and hedge by 1.5-1.85x. This was *not* due to the hedge band.
5.  **Explanation of Residual Bias (Step 2 findings):**
    *   **Pool's $\sigma$ is lower than spot's:** The pool's active-price $\sigma$ (9.37e-5/s) is 0.882x that of Deribit spot (1.06e-4/s) at a 30s cadence. Incorporating the pool's realized $\sigma$ significantly reduced LVR overstatement (e.g., Curve LVR from 1.28 to 0.98).
    *   **Pool's price moves in bursts:** The pool's active bin price is unchanged in 50.6% of 30s checks, and its `E|r| / (sd·√(2/π))` is 0.739 (vs. 0.878 for Deribit spot). This implies 1.35x less trading than a Gaussian model assumes.
6.  **Refined Model Accuracy:** With [[rho-bar]], the realized pool $\sigma$, and the [[burst-factor]] (0.739), the "Curve" shape LVR and hedge ratios agree with the simulator to within 2-3% (LVR 0.98, hedge 0.97 overall).
## Assumptions and limits
The data used for calibration was provisional, covering 4 full days and one complete sub-window. Re-runs at 21 days are recommended for final validation. The initial [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D2 test criteria were found to be too broad, failing the model for estimator errors rather than form errors.
## Concepts introduced or used
[[ev-gate-calibration]]
[[rho-0]]
[[rho-bar]]
[[hedge-drag]]
[[burst-factor]]
[[sigma-forecast-error]]
[[loss-versus-rebalancing]]
[[dlmm-bins]]
[[ev-gate]]
[[realized-volatility]]
[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost]]
[[adr-046-real-time-hurdle-rate-restates-the-ev-gate]]
[[adr-047-provisional-sigma-estimator]]