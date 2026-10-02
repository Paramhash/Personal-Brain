---
domain: cl-market-making
tags:
- dlmm
- range-width
- parameters
- strategy
- volatility-forecasting
- range-planning
- market-making-strategy
- findings
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
ingest_hashes:
- ef374bb262f7c094
- cdb75d1714411a16
updated: '2026-10-02'
sources:
- dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
- dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md
---
# Deploy Width Sigma Multiple
**In one line:** A configurable parameter that scales the forecasted [[implied-volatility|sigma]]-horizon product to determine the target half-width of the [[sigma-derived-deployed-window]] for concentrated liquidity.
## Intuition
This multiplier allows for fine-tuning the concentration of deployed liquidity. A higher multiple results in a wider deployed range, aiming to keep the price within the range for longer, while a lower multiple results in a narrower, more concentrated range, aiming to maximize fee capture per unit of capital. It's a key lever for balancing fee yield against the risk of being out of range.
## Mechanism / math
The `deployWidthSigmaMultiple` is used in the calculation of the `targetHalfWidthPct` as part of the [[range-planning]] process:

$$ \text{targetHalfWidthPct} = \text{deployWidthSigmaMultiple} \times \text{sigmaHorizon} $$

where `sigmaHorizon` is the product of the forecasted [[implied-volatility|sigma]] ($\sigma$) and the square root of the `horizonSeconds`.

The resulting `targetHalfWidthPct` is then converted into `targetHalfBins`, which contributes to the final `width` of the [[sigma-derived-deployed-window]].
## Where it matters
*   **Liquidity Concentration:** Directly controls how tightly liquidity is concentrated around the active price.
*   **Fee Yield:** A smaller multiple leads to higher concentration and potentially higher [[fee-yield|fee yield]] per unit of capital, assuming the price stays within the narrower range.
*   **Out-of-Range Frequency:** A larger multiple reduces the frequency of the price moving out of the deployed range, but at the cost of diluting liquidity and potentially lowering [[fee-yield|fee yield]].
*   **Risk Management:** Influences the trade-off between maximizing returns and minimizing [[impermanent-loss|impermanent loss]] and [[hedge-churn-artifact|hedge churn]].
## Evidence and limits
As noted in [[dlmm-2026-planner-deploys-wall-envelope|F-022]], the `deployWidthSigmaMultiple` is currently **UNRATIFIED** and defaults to 1. The finding explicitly states that ±1σ does not imply a 68% chance of staying in range, as this figure describes the terminal distribution, not the probability that a price path never leaves the band. This highlights the need for further research and ratification, which is tracked by `observation_archive.md` §6 question 3.
## Related
[[sigma-derived-deployed-window]]
[[range-planning]]
[[implied-volatility]]
[[fee-yield]]
[[hedge-churn-artifact]]
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]
[[dlmm-2026-planner-deploys-wall-envelope]]

---

## Update from dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md (2026-10-02)

# Deploy Width Sigma Multiple
**In one line:** A configurable multiplier applied to a volatility estimate (e.g., [[sigma-forecast-error]]) to determine the desired width of a [[liquidity-concentration|concentrated liquidity]] position.
## Intuition
This multiple allows a liquidity provider to dynamically adjust the width of their deployed range based on market volatility. A higher multiple implies a wider range, potentially capturing more trades but also exposing more capital to [[impermanent-loss|impermanent loss]] or [[loss-versus-rebalancing|LVR]].
## Where it matters
The `deployWidthSigmaMultiple` is a key parameter in [[range-planning]] for [[cl-market-making|concentrated liquidity market making]] strategies. It directly influences the [[sigma-derived-deployed-window]], which is the target width for a liquidity position.
## Evidence and limits
*   **Effectiveness Constraint (F-024):** The effectiveness of this multiple is contingent on the [[wall-envelope]] being wider than the [[sigma-derived-deployed-window]]. If the wall envelope is narrower, it becomes the binding constraint, and the `deployWidthSigmaMultiple` has no effect.
*   **Initial Misdiagnosis (F-024):** Early observations suggested the `wall-envelope` was routinely narrower, implying the multiple was often inoperative.
*   **Corrected Understanding (F-024):** Further analysis over 1336 records revealed that the `wall-envelope` is typically *wider* than the sigma-implied width (median 402 bins vs. 203 bins sigma-implied). This means the `deployWidthSigmaMultiple` *does* bind in the median case and is not irrelevant.
*   **Coupling with Wall Placement:** The utility of this multiple is also affected by the placement of the [[wall-envelope]]. If the walls fail to bracket [[spot-price]], the strategy may be blocked entirely, regardless of the desired sigma-derived width.
*   **Ratification:** Ratifying the `deployWidthSigmaMultiple` is important because it is an operative lever in typical market conditions, but its impact must be re-evaluated after changes to wall selection (e.g., [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]) that affect the `wall-envelope`.
## Related
[[sigma-derived-deployed-window]], [[wall-envelope]], [[range-planning]], [[sigma-forecast-error]], [[dlmm-bins]], [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]], [[dlmm-2026-wall-envelope-narrower-than-sigma-width|F-024]]
