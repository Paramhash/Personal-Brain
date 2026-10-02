---
domain: cl-market-making
tags:
- dlmm
- range-planning
- gex
- market-making-strategy
- findings
aliases:
- F-024
created: 2026-10-02
reviewed: false
source_origin: dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md
ingest_hashes:
- 93f23ce6ddc03fb7
---
# F-024 — The wall envelope is routinely narrower than the σ-derived width, so ADR-034's rule never binds (DLMM, 2026)
**Type:** docs
## Claim
The `wall-envelope`, derived from GEX walls, often fails to bracket the spot price or is too narrowly placed, rendering the `deploy-width-sigma-multiple` rule in [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] ineffective and leading to frequent `ACTIVE_BIN_OUT_OF_RANGE` rejections. This is primarily due to the `call-wall` acting as an at-the-money (ATM) pin rather than an upper bound.
## Method and data
The finding is based on observations from a live frame (2026-09-27) against a real SOL/USDC pool and a 398-instrument [[deribit]] chain, corroborated by a recon run's 1336 records. The `buildGexProfile` and `planDeployRange` components were verified to behave as specified.
## Key results
*   **Initial Observation (single frame):** The `wall-envelope` was 21 bins (0.80% wide), significantly narrower than the `sigma-implied-width` of 203 bins (8.4% wide). This caused the envelope to bind the deployed range, making the `deploy-width-sigma-multiple` inoperative.
*   **Rejection Rate:** In 36% of the 1336 observed ticks, the strategy was `BLOCKED` with `ACTIVE_BIN_OUT_OF_RANGE` because the pool price was *above* the `call-wall`. Price was never observed below the `put-wall`.
*   **Envelope Width Distribution:** Over 1336 records, the `wall-envelope` span was: min 19 bins, median 402 bins, max 939 bins. 17 records (1.3%) were at or below the 20-bin floor (`MIN_BINS_PER_POSITION`). This corrected the initial misdiagnosis, showing the envelope is *routinely wider* than the sigma-implied width in the median case.
*   **Wall Placement Asymmetry:** Median absolute distance from spot: `call-wall` 0.36%, `put-wall` 14.98%. This 42x asymmetry indicates the `call-wall` acts as an ATM "pin" (due to peak dollar gamma being maximized at the money), while the `put-wall` is displaced downward by actual open interest, functioning as a proper lower bound.
## Assumptions and limits
The initial diagnosis of the `wall-envelope` being "routinely narrower" was based on a single frame and later corrected by analyzing a larger dataset. The duration of observed market regimes (minutes, not days) limits conclusions about long-term persistence.
## Concepts introduced or used
[[wall-envelope]], [[deploy-width-sigma-multiple]], [[active-bin-out-of-range]], [[call-wall]], [[put-wall]], [[gex-intelligence]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]], [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]], [[range-planning]], [[gamma-exposure-gex]], [[dlmm-bins]], [[spot-price]]