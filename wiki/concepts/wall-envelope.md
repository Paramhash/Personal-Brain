---
domain: cl-market-making
tags:
- dlmm
- range-width
- gex
- strategy
- range-planning
- market-making-strategy
- findings
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
ingest_hashes:
- 98fa9cccf55e6053
- 7b6e581556c0400b
updated: '2026-10-02'
sources:
- dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
- dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md
---
# Wall Envelope
**In one line:** The outer bounds, derived from [[gamma-exposure-gex|GEX]] walls (e.g., [[call-wall|call walls]]), that constrain the maximum possible width and placement of a deployed concentrated liquidity range in a DLMM pool.
## Intuition
The wall envelope acts as a "fence" or a permissible region for liquidity deployment. It defines the widest possible range that a liquidity provider might consider based on significant [[gamma-exposure-gex|GEX]] levels, but it is not necessarily the actual range where liquidity is deployed. The actual deployed range, the [[sigma-derived-deployed-window]], is typically narrower and must fit within this envelope.
## Mechanism / math
The wall envelope is determined by converting the prices of identified [[call-wall|GEX walls]] (or other significant price levels) into corresponding [[dlmm-bins|DLMM bins]]. For example, a call wall at a certain strike price translates to an upper bin ID, and a put wall to a lower bin ID, defining the `lowerBinId` and `upperBinId` of the envelope.

According to `range_planning.md` §2b (introduced by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]):
1.  Both walls are converted to bins.
2.  The system rejects an inverted envelope (where `lowerBinId` > `upperBinId`) or one narrower than `MIN_BINS_PER_POSITION`.
3.  It also rejects if the [[active-bin-out-of-range|reconciled active bin lies outside the envelope]].

The actual deployed range, the [[sigma-derived-deployed-window]], is then calculated separately and clamped to ensure it stays within the `envelopeBins` (the total width of the wall envelope).
## Where it matters
*   **Constraint on Deployment:** The wall envelope serves as an upper bound for the width of the deployed liquidity range, preventing deployments that extend beyond significant [[gamma-exposure-gex|GEX]] levels.
*   **Risk Management:** It helps in defining a safe zone for liquidity, ensuring that positions are not placed in areas where market makers might face extreme gamma exposure or rapid price movements.
*   **Distinction from Deployed Range:** It's crucial to distinguish the wall envelope from the actual deployed range. As highlighted in [[dlmm-2026-planner-deploys-wall-envelope|F-022]], incorrectly deploying the full wall envelope as the liquidity range can lead to suboptimal liquidity concentration and inaccurate performance metrics.
## Evidence and limits
[[dlmm-2026-planner-deploys-wall-envelope|F-022]] revealed that the DLMM hedge bot's planner initially misused the wall envelope by deploying it directly as the liquidity range, rather than using it as a constraint for a narrower, sigma-derived window. This led to wider-than-intended liquidity positions and understated [[hedge-churn-artifact|hedge churn]] measurements. The resolution of F-022 ensured that the wall envelope is correctly used as an outer boundary, with the actual deployed range being a more concentrated window within it.
## Related
[[range-planning]]
[[sigma-derived-deployed-window]]
[[dlmm-bins]]
[[call-wall]]
[[gamma-exposure-gex]]
[[active-bin-out-of-range]]
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]
[[dlmm-2026-planner-deploys-wall-envelope]]

---

## Update from dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md (2026-10-02)

# Wall Envelope
**In one line:** The price range defined by the [[put-wall]] and [[call-wall]], intended to serve as an outer boundary for [[liquidity-concentration|concentrated liquidity]] deployment.
## Intuition
The wall envelope aims to define a safe or strategically relevant region for liquidity deployment, based on significant [[gamma-exposure-gex|GEX]] levels. It acts as a constraint, ensuring that deployed liquidity does not extend beyond these perceived market boundaries.
## Mechanism / math
The wall envelope is determined by identifying the [[call-wall]] (strike with peak dollar gamma on the call side) and the [[put-wall]] (strike with peak dollar gamma on the put side). These strikes then define the upper and lower bounds of the envelope.
## Where it matters
The wall envelope is a critical input for [[range-planning]] in [[cl-market-making|concentrated liquidity market making]] strategies. It is used to constrain the [[sigma-derived-deployed-window]], ensuring that the deployed range respects these GEX-derived boundaries.
## Evidence and limits
*   **Initial Observation (F-024):** A single live frame showed the wall envelope (21 bins, 0.80% wide) to be significantly narrower than the [[sigma-derived-deployed-window]] (203 bins, 8.4% wide). In this scenario, the envelope became the binding constraint, rendering the [[deploy-width-sigma-multiple]] inoperative.
*   **Corrected Understanding (F-024):** Over 1336 records, the median envelope span was 402 bins, suggesting it is *routinely wider* than the sigma-implied width in typical cases. The initial observation was closer to a 1.3% tail event.
*   **Placement Issue:** The primary problem identified was the *placement* of the wall envelope relative to the [[spot-price]]. In 36% of observed ticks, the price was *above* the [[call-wall]], leading to [[active-bin-out-of-range]] rejections. This was due to the [[call-wall]] acting as an at-the-money (ATM) pin rather than a true upper bound.
*   **Asymmetry:** The [[call-wall]] was found to be very close to spot (median 0.36% distance), while the [[put-wall]] was typically much further below spot (median 14.98% distance), functioning effectively as a lower bound.
*   **Resolution:** [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] was ratified to redefine wall selection, ensuring that walls are side-constrained (call wall above spot, put wall below spot) to address the placement issue and ensure the envelope functions as intended.
## Related
[[call-wall]], [[put-wall]], [[gamma-exposure-gex]], [[range-planning]], [[sigma-derived-deployed-window]], [[deploy-width-sigma-multiple]], [[active-bin-out-of-range]], [[dlmm-bins]], [[gex-intelligence]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]], [[dlmm-2026-wall-envelope-narrower-than-sigma-width|F-024]]
