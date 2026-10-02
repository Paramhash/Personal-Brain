---
domain: cl-market-making
tags:
- dlmm
- range-width
- risk-management
- deployment
- range-planning
- market-making-strategy
- findings
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
ingest_hashes:
- ef5812a6321bee1e
- 62f854429fd37137
updated: '2026-10-02'
sources:
- dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
- dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md
---
# Active Bin Out of Range
**In one line:** A critical condition where the current active price bin of a DLMM pool falls outside the proposed [[wall-envelope]] for liquidity deployment, leading to the rejection of the deployment plan to prevent immediate out-of-range positions.
## Intuition
Deploying liquidity in a range that does not contain the current market price (the active bin) would result in an immediate out-of-range position, making the liquidity inactive and unable to earn fees from the start. This check acts as a fundamental safeguard to ensure that any deployed liquidity is immediately active and capable of participating in market making.
## Mechanism / math
The check is a simple boolean evaluation:
`pool.activeBinId >= plan.lowerBinId && pool.activeBinId <= plan.upperBinId`

If this condition is false, meaning the `activeBinId` is outside the `lowerBinId` and `upperBinId` of the proposed deployment range (or its [[wall-envelope]]), the deployment is rejected, and an `ACTIVE_BIN_OUT_OF_RANGE` error is reported. This check is mandated by `range_planning.md` §2b step 3.
## Where it matters
*   **Capital Safety:** Prevents capital from being deployed into an immediately inactive state, where it cannot earn fees and might be subject to [[impermanent-loss|impermanent loss]] without corresponding fee income.
*   **Deployment Integrity:** Ensures that all deployments adhere to a fundamental rule of active market making.
*   **Decision Gate:** Serves as an early and cheap failure point in the deployment process, preventing more complex issues down the line.
## Evidence and limits
[[dlmm-2026-planner-deploys-wall-envelope|F-022]] highlighted that prior to its resolution, the DLMM hedge bot's planner failed to implement this crucial check. During a live run, `plan_ok` was reported as true for 269 out of 280 ticks in a specific regime, even when the active bin was outside the *returned interval* (which was the [[wall-envelope]]). This demonstrated a contract-versus-implementation gap, where the planner lacked the active bin input to perform the mandated rejection. The fix for F-022 explicitly implemented this check, ensuring that deployments are now rejected if the active bin is not contained within the proposed range.
## Related
[[range-planning]]
[[wall-envelope]]
[[dlmm-bins]]
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]
[[dlmm-2026-planner-deploys-wall-envelope]]

---

## Update from dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md (2026-10-02)

# Active Bin Out of Range
**In one line:** A rejection status indicating that the current [[pool-price]] (derived from the active [[dlmm-bins|bin]]) falls outside the proposed [[wall-envelope]] for [[liquidity-concentration|concentrated liquidity]] deployment.
## Intuition
This status signifies that the market's current price is not contained within the boundaries set by the strategy's [[range-planning]] logic, specifically the [[wall-envelope]]. It prevents deploying liquidity in a range that does not encompass the current market price, which would be immediately out of range.
## Mechanism / math
The `ACTIVE_BIN_OUT_OF_RANGE` rejection occurs when the [[pool-price]] is either above the [[call-wall]] or below the [[put-wall]] as defined by the [[wall-envelope]]. Since the pool price is derived from the active bin, and the wall envelope is scaled, this condition primarily fires when the walls themselves fail to bracket the [[spot-price]].
## Where it matters
This rejection directly impacts the ability of a [[cl-market-making|concentrated liquidity market making]] strategy to deploy or reposition liquidity. Frequent occurrences indicate a fundamental misalignment between the market's price action and the strategy's defined operating range.
## Evidence and limits
*   **Frequent Occurrence (F-024):** In a live observation period, the strategy was `BLOCKED` with `ACTIVE_BIN_OUT_OF_RANGE` in 36% of observed ticks. This indicates it is a routine state, not a rare corner case.
*   **One-Sided Failure:** The rejection was consistently due to the [[pool-price]] being *above* the [[call-wall]]; it was never observed to be below the [[put-wall]].
*   **Root Cause:** This one-sided failure was traced to the [[call-wall]] acting as an at-the-money (ATM) "pin" (due to its definition as the peak dollar gamma strike) rather than a true upper bound. When [[spot-price]] moves above this pin, the envelope fails to contain the active bin.
*   **Resolution:** [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] was ratified to redefine wall selection, ensuring that the [[call-wall]] is always chosen above spot, which is expected to reduce the frequency of `ACTIVE_BIN_OUT_OF_RANGE` rejections caused by wall misplacement.
## Related
[[wall-envelope]], [[call-wall]], [[put-wall]], [[range-planning]], [[dlmm-bins]], [[spot-price]], [[gex-intelligence]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]], [[dlmm-2026-wall-envelope-narrower-than-sigma-width|F-024]]
