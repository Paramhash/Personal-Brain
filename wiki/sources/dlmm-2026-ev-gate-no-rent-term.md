---
domain: cl-market-making
tags:
- dlmm
- ev-gate
- solana-rent
- cost-accounting
- adr
aliases:
- F-026
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-026-the-ev-gate-has-no-rent-term-so-wider-ranges-look-cheaper-than-they-are.md
ingest_hashes:
- 594900663e3e9b91
---
# F-026 — The EV gate has no rent term, so wider ranges look cheaper than they are (DLMM Project, 2026)
**Type:** paper
## Claim
The [[ev-gate]] in the DLMM hedge bot, responsible for authorizing capital deployments, critically lacked a term for sunk Solana bin-array rent. This omission caused wider liquidity ranges to appear artificially cheaper than they truly were, creating a dangerous bias in deployment decisions, especially given other policies (like [[adr-034-range-width-rule-for-fine-binned-pools]] and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot]]) that encourage wider ranges.
## Method and data
The finding emerged from an internal code review of `src/decision/ev/evCalculator.ts` during the grounding of [[adr-039-deploy-reserve-is-derived-from-the-plan]]'s reserve arithmetic. It involved quantitatively comparing the magnitude of the missing sunk bin-array rent against the existing placeholder for transaction fees (`PLACEHOLDER_DEPLOY_LAMPORTS`).
## Key results
- Sunk bin-array rent, which scales with range width, was entirely absent from the [[ev-gate]]'s cost calculations.
- For a 203-bin range (today's σ-derived width), sunk bin-array rent was measured at 0.2857 SOL, which is **1,429 times** the 0.0002 SOL placeholder for transaction fees.
- For a 940-bin range (the [[wall-envelope]] bound from [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot]]), sunk bin-array rent was 1.0001 SOL, **5,001 times** the placeholder.
- The omission created a bias towards wider ranges, as their true sunk costs were not factored into the decision to deploy.
- No actual capital deployment failures were observed because the EV estimators were uncalibrated placeholders, meaning the gate had not yet been the binding constraint for real deployments.
## Assumptions and limits
The finding was pre-emptive, identifying a defect before it caused real capital risk. The EV estimators remained uncalibrated placeholders at the time of the finding, meaning the [[ev-gate]] was not yet making economic judgments. The fix (ADR-040) addresses the missing term but does not calibrate the estimators.
## Concepts introduced or used
[[ev-gate]], [[solana-rent]], [[dlmm-bins]], [[range-planning]], [[adr-039-deploy-reserve-is-derived-from-the-plan]], [[adr-040-sunk-deployment-rent-is-an-ev-term]], [[adr-031-funding-drag-numeraire-and-unknown-cost-policy]], [[wall-envelope]]