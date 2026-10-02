---
domain: cl-market-making
tags:
- dlmm
- range-width
- strategy
- findings
- adr
aliases:
- F-022
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
ingest_hashes:
- 4f2aa12f73ba6726
---
# F-022 — The planner deploys the wall envelope as the range, and never implements ADR-034's width rule (DLMM Hedge Bot Team, 2026)
**Type:** docs
## Claim
The range planner in the DLMM hedge bot incorrectly deployed the full GEX [[wall-envelope]] as the liquidity range, instead of a narrower, [[sigma-derived-deployed-window]] as mandated by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]. This led to significantly understated [[hedge-churn-artifact|hedge churn]] measurements and failed to implement critical deployment rejection conditions, violating the contract specified in `range_planning.md` §2b and §5.
## Method and data
The finding was raised on 2026-09-27 by an independent review and confirmed against the contract and code. Analysis included a 6.7-hour live run (TICKET N) with 808 records at a 30-second cadence on 2026-09-27. The issue was closed on 2026-09-27 by TICKET O, which implemented the correct logic and added comprehensive unit tests.
## Key results
*   **Incorrect Range Deployment:** The planner returned a width of 939 bins (with the call wall at 150) and 402 bins (at 121), which represented the full [[wall-envelope]], not the narrower, derived width.
*   **Failed Rejection Conditions:** `plan_ok` was true for all 808 ticks, including 269 of 280 ticks in the 121 regime where the [[active-bin-out-of-range|active bin lay outside the returned interval]]. These should have been rejected by `range_planning.md` §2b step 3.
*   **Understated Churn:** Previous [[hedge-churn-artifact|hedge churn]] figures were understated by a factor of approximately 4.64x (calculated as `envelopeBins / width`), because the [[simulated-base-inventory]] model assumed a wider position than what should have been deployed.
*   **Resolution:** The fix implemented ADR-034's five steps: deriving the envelope, rejecting envelopes below `MIN_BINS_PER_POSITION`, rejecting active bins outside the envelope, clamping the sigma-derived width, and centering the window on the active bin.
*   **Verification:** Live verification showed the planner returning a 203-bin window inside a 402-bin envelope, with the active bin contained. The predicted increase in inventory sensitivity (and thus churn) was confirmed, with one bin of drift moving a simulated 100 SOL position by 0.495 SOL (vs. 0.1066 SOL previously), a 4.64x increase.
## Assumptions and limits
The finding highlights a critical gap between contract specification (ADR-034) and implementation. The `deployWidthSigmaMultiple` parameter remains unratified (defaulting to 1), and the [[adr-030-deployment-sol-reserve|ADR-030]] `0.25 SOL` reserve is not yet width-aware, potentially leading to deployment breaches for even tight ranges. [[finding-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds|F-021]]'s wall stability issue (bistable call wall producing conflicting legal plans) also remains open.
## Concepts introduced or used
[[range-planning]]
[[wall-envelope]]
[[sigma-derived-deployed-window]]
[[deploy-width-sigma-multiple]]
[[active-bin-out-of-range]]
[[hedge-churn-artifact]]
[[dlmm-bins]]
[[call-wall]]
[[ev-gate]]
[[sol-execution-reserve]]
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]
[[adr-030-deployment-sol-reserve|ADR-030]]

---