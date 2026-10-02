---
domain: cl-market-making
tags:
- range-planning
- dlmm
- error-handling
- strategy-design
- capital-allocation
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
ingest_hashes:
- ec3faaa2b547282c
---
# Uncontaining Bounds Acceptance
**In one line:** A flaw in [[range-planning]] where the liquidity deployment planner accepts and reports success for a proposed price range that does not contain the current spot price or active bin.
## Intuition
A fundamental requirement for a [[liquidity-concentration|concentrated liquidity]] position to be active and earn fees is that the current market price must fall within its defined range. If the planner proposes a range that excludes the current price, the deployed position will be entirely composed of one asset and will not facilitate swaps or earn fees until the price moves back into the range.
## Mechanism / math
This issue arises when the `planDeployRange` function (or equivalent) fails to implement a crucial containment check. Even if other checks pass (e.g., walls present, finite, positive, correctly ordered, bin step valid), the absence of a check for whether the active bin or current spot price is *within* the proposed range allows invalid ranges to be accepted. This was identified as an unimplemented step (step 3) of a ratified rule ([[adr-034-range-width-rule-for-fine-binned-pools]] §2b).
## Where it matters
Accepting uncontaining bounds leads to:
*   **Zero Fee Capture:** The deployed position is immediately out of range, holding only one asset (e.g., all base or all quote) and earning no [[fee-yield]] until the price re-enters the range.
*   **Inefficient Capital Allocation:** Capital is deployed ineffectively, sitting idle and exposed to [[impermanent-loss]] without generating revenue.
*   **Misleading Success Metrics:** The planner reports `ok`, masking a critical operational failure.
## Evidence and limits
The `[[dlmm-2026-call-wall-oscillates]]` finding provided empirical evidence for this flaw. In a 6.7-hour observation run, `plan_ok` was `true` on all 808 ticks, yet in the 121-regime, the proposed range often excluded the spot price (~121.7). This meant 35% of ticks would have resulted in a deployment where the price was outside its own bounds. This finding served as direct evidence for the necessity of the containment check previously recommended in [[ev-gate]] and specified in [[adr-034-range-width-rule-for-fine-binned-pools]].
## Related
[[range-planning]], [[dlmm-bins]], [[adr-034-range-width-rule-for-fine-binned-pools]], [[ev-gate]], [[liquidity-concentration]], [[cl-entry-strategy]], [[fee-yield]], [[impermanent-loss]]