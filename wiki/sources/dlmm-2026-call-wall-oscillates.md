---
domain: cl-market-making
tags:
- dlmm
- gex
- range-planning
- simulation
- findings
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
ingest_hashes:
- e6dacce2ec73e3a3
---
# F-021 — The call wall oscillates between strikes, and the planner accepts bounds that do not contain spot (DLMM, 2026)
**Type:** docs
## Claim
This finding identifies two critical issues in the DLMM hedge bot's range planning: first, the [[call-wall]] selection mechanism is "bistable," causing rapid oscillations between strikes and leading to excessive repositioning costs; second, the `planDeployRange` function incorrectly returns `ok` for liquidity ranges that do not contain the current spot price, resulting in deployments that are entirely one asset and earn no fees. It also clarifies that a significant portion of simulated [[hedge-churn]] was an artifact of the simulation model, not actual hedging activity.
## Method and data
The findings are derived from a 6.7-hour live decision run of the DLMM bot in an "observe-only" mode, generating 808 records at 30-second intervals. The data was analyzed from `C:\observation\recon-sim-2026-09-27`.
## Key results
*   **Call Wall Bistability:** Over 6.7 hours, the [[call-wall]] (identified by `totalNetDollarGex1Pct`) oscillated nine times between 150 and 121 strikes, while spot price moved only 1.41%. The put wall remained stable at 103. This oscillation led to proposed range widths varying significantly (939 bins vs. 402 bins). The underlying cause was a near-tie in aggregate gamma between the two strikes, and the selection rule lacked [[hysteresis]].
*   **Uncontaining Bounds Acceptance:** The `planDeployRange` function reported success (`plan_ok` was `true` on all 808 ticks) even when the proposed range excluded the current spot price. In the 121-regime, spot (~121.7) was at or above the upper bound, meaning the proposed range contained no current price. This was due to an unimplemented part of the [[adr-034-range-width-rule-for-fine-binned-pools]] rule (§2b, step 3) which requires a containment check. 35% of ticks would have resulted in a deployment with price outside its own bounds.
*   **Hedge Churn Artifact:** The total simulated [[hedge-churn]] of 543 SOL over 6.7 hours (extrapolating to 212% of position value annually in taker fees) was largely an artifact. 95.2% (279.9 SOL) of this churn came from the nine wall flips, as the simulation treated bounds changes as instantaneous inventory jumps rather than distinct repositioning events. The actual "within-bounds drift" was estimated at ≈10% per year.
*   **Pipeline Soundness:** The core pipeline produced 808/808 plans with zero rejections, stale snapshots, or tick failures against live Deribit and Solana.
*   **Zero-Gamma Level Stability:** The [[zero-gamma-level]] was stable (104.68–105.98 across 807 ticks), contrasting with earlier short-sample observations.
## Assumptions and limits
*   The initial churn figures were inflated because the simulation lacked a proper reposition model, summing within-bounds drift and bounds-change jumps.
*   The analysis of wall stability was re-based by [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot]], which clarified that 121 was a "pin" and 150 a "resistance level," making 121 ineligible when price was above it. However, the 0.150% price move in the 24 frames after ADR-038's ratification was insufficient to test wall stability across a significant price move.
## Concepts introduced or used
[[call-wall-oscillation]], [[uncontaining-bounds-acceptance]], [[hedge-churn-artifact]], [[call-wall]], [[gamma-exposure-gex]], [[range-planning]], [[dlmm-bins]], [[simulated-base-inventory]], [[hedge-churn]], [[adr-034-range-width-rule-for-fine-binned-pools]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot]], [[ev-gate]], [[cl-rebalancing-condition]], [[dlmm-simulator]], [[zero-gamma-level]], [[hysteresis]]