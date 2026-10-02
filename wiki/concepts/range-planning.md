---
domain: cl-market-making
tags:
- liquidity-concentration
- dlmm
- strategy
- capital-allocation
- market-making
- range-width
- deployment
- adr
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
ingest_hashes:
- 39a2357e7c9f4829
- 19b3d778dcc655bc
updated: '2026-10-02'
sources:
- dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
- dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
---
# Range Planning
**In one line:** The process of determining the optimal price range for deploying [[liquidity-concentration|concentrated liquidity]] in an Automated Market Maker (AMM) pool to maximize fee capture and manage risk.
## Intuition
A [[cl-market-making|concentrated liquidity market maker]] must strategically choose the upper and lower bounds of their liquidity position. This decision directly impacts their exposure to [[impermanent-loss]], their ability to capture [[fee-yield]], and their [[inventory-accounting|inventory]] management. The goal is to place liquidity where it is most likely to be traded, while minimizing adverse effects.
## Mechanism / math
In the DLMM context, [[range-planning]] involves several steps:
1.  **Signal Extraction:** Identifying key market signals, such as [[gamma-exposure-gex]] walls (e.g., [[call-wall]], put wall) or [[zero-gamma-level|zero-gamma levels]], which can act as potential [[market-boundaries-cl]].
2.  **Envelope Definition:** Using these signals to define a broader "envelope" for potential liquidity deployment.
3.  **Deployed Width Calculation:** Deriving a narrower, "deployed width" from [[volatility-forecasting|volatility forecasts]] (e.g., [[sigma-derived-deployed-window]]) and centering it on the active bin or current spot price.
4.  **Containment Checks:** Ensuring the proposed range actually contains the current market price or active bin, as outlined in rules like [[adr-034-range-width-rule-for-fine-binned-pools]].
5.  **Approval Discipline:** Adhering to approved-bounds discipline to prevent excessive [[cl-rebalancing-condition|repositioning]].
## Where it matters
Effective [[range-planning]] is fundamental to the success of any [[cl-provider-strategy]]. It directly influences:
*   **Capital Efficiency:** How effectively capital is deployed to earn fees.
*   **Risk Exposure:** Management of [[impermanent-loss]] and [[inventory-accounting]].
*   **Operational Costs:** The frequency and cost of [[cl-rebalancing-condition|repositioning]] liquidity.
*   **Profitability:** The overall [[fee-yield]] and [[alpha-like-component-lp-returns|alpha-like returns]] of the LP position.
## Evidence and limits
The `[[dlmm-2026-call-wall-oscillates]]` finding highlights critical issues in [[range-planning]]:
*   **Unstable Signals:** [[call-wall-oscillation]] can lead to rapid, costly repositioning if the underlying signals used for bounds are unstable.
*   **Uncontaining Bounds:** The planner may fail to implement crucial checks (e.g., [[adr-034-range-width-rule-for-fine-binned-pools]] §2b step 3), leading to the acceptance of ranges that do not contain the current spot price. Such deployments are entirely one asset and earn no fees until the price re-enters the range.
*   **Churn Artifacts:** Flaws in simulation models can misrepresent the cost of range changes, leading to an inflated [[hedge-churn-artifact]].
## Related
[[dlmm-bins]], [[liquidity-concentration]], [[cl-entry-strategy]], [[capital-allocation-rule-cl]], [[gamma-exposure-gex]], [[call-wall]], [[adr-034-range-width-rule-for-fine-binned-pools]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot]], [[impermanent-loss]], [[fee-yield]], [[cl-rebalancing-condition]], [[market-boundaries-cl]], [[sigma-derived-deployed-window]]

## Update from dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md (2026-10-02)

# Range Planning
**In one line:** The process of determining the optimal price range (defined by bins) for deploying concentrated liquidity in an Automated Market Maker (AMM) pool.
## Intuition
Effective range planning aims to balance maximizing fee capture by concentrating liquidity where price is expected to trade, with minimizing [[impermanent-loss|impermanent loss]] and [[hedge-churn-artifact|hedge churn]] by avoiding frequent rebalancing or being out of range. It involves forecasting price movement and defining bounds for liquidity deployment.
## Mechanism / math
As defined by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]], the range planning process for a DLMM pool involves several steps to determine the deployed width:

1.  **Calculate Sigma Horizon:**
    $$ \text{sigmaHorizon} = \sigma \times \sqrt{\text{horizonSeconds}} $$
    where $\sigma$ is the forecasted volatility and $\text{horizonSeconds}$ is the planning horizon.
2.  **Determine Target Half-Width Percentage:**
    $$ \text{targetHalfWidthPct} = \text{deployWidthSigmaMultiple} \times \text{sigmaHorizon} $$
    where `deployWidthSigmaMultiple` is a configurable multiplier.
3.  **Calculate Target Half Bins:**
    $$ \text{targetHalfBins} = \lceil \ln(1 + \text{targetHalfWidthPct}) / \ln(1 + \text{binStep} / 10\_000) \rceil $$
    where `binStep` is the percentage price difference between adjacent bins.
4.  **Clamp the Width:** The final `width` is determined by clamping the derived width between a minimum floor and the [[wall-envelope]]:
    $$ \text{width} = \text{clamp}( 2 \times \text{targetHalfBins} + 1, \text{MIN\_BINS\_PER\_POSITION}, \text{envelopeBins} ) $$
    where `MIN_BINS_PER_POSITION` is a minimum number of bins required for a position, and `envelopeBins` is the total width of the [[wall-envelope]].
5.  **Center and Shift:** The liquidity window of `width` bins is then placed [[sigma-derived-deployed-window|centered on the active bin]], shifted inward only as far as needed to stay within the [[wall-envelope]]. An odd remainder in centering goes to the lower side first.

**Historical Implementation Gap:**
Prior to the resolution of [[dlmm-2026-planner-deploys-wall-envelope|F-022]], the planner incorrectly deployed the full [[wall-envelope]] as the liquidity range, rather than the narrower, sigma-derived window. This meant that the `sigma`, `horizon`, `MIN_BINS_PER_POSITION`, `envelope`, `targetHalfBins`, `deployWidth`, and `activeBin` parameters were not being used in the range calculation, leading to wider-than-intended deployments and inaccurate performance measurements.
## Where it matters
*   **Liquidity Concentration:** Directly impacts the concentration of deployed capital, influencing fee capture and capital efficiency.
*   **Risk Management:** Determines exposure to [[impermanent-loss|impermanent loss]] and the frequency/magnitude of rebalancing (and thus [[hedge-churn-artifact|hedge churn]]).
*   **Deployment Decisions:** Informs the decision of where and how wide to deploy liquidity, impacting the overall profitability and stability of a [[cl-provider-strategy|CL provider strategy]].
*   **System Integrity:** Adherence to the specified range planning rules (e.g., rejecting deployments where the active bin is outside the planned range) is crucial for preventing immediate out-of-range positions and maintaining capital safety.
## Evidence and limits
[[dlmm-2026-planner-deploys-wall-envelope|F-022]] demonstrated that the failure to implement ADR-034's derived width rule led to significant mismeasurements of [[hedge-churn-artifact|hedge churn]] (understated by ~4.64x) and a failure to reject invalid deployments. The fix for F-022 corrected this, ensuring that the deployed range is a narrower, sigma-derived window constrained by the envelope.

However, the `deployWidthSigmaMultiple` remains unratified, and the interaction with [[adr-030-deployment-sol-reserve|ADR-030]]'s SOL reserve (which is not width-aware) still presents a challenge, as even tight ranges can breach the reserve.
## Related
[[dlmm-bins]]
[[wall-envelope]]
[[sigma-derived-deployed-window]]
[[deploy-width-sigma-multiple]]
[[active-bin-out-of-range]]
[[hedge-churn-artifact]]
[[impermanent-loss]]
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]
[[dlmm-2026-planner-deploys-wall-envelope]]

---
