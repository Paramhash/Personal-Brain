---
domain: cl-market-making
tags:
- gex
- options
- market-structure
- dlmm
- market-making-strategy
- findings
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
ingest_hashes:
- dc59ac9501467104
- 52d23b21164bbaf5
updated: '2026-10-02'
sources:
- dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
- dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md
---
# Call Wall
**In one line:** A significant concentration of gamma exposure (GEX) from call options at a specific strike price, acting as a potential resistance level for the underlying asset's price.
## Intuition
Large open interest in call options at a particular strike can create a "wall" where [[derivatives]] dealers become increasingly short gamma above that strike. As the price approaches or moves above this level, dealers are forced to sell into rallies to re-hedge their delta, effectively capping the price movement.
## Mechanism / math
A [[call-wall]] is typically identified by analyzing the aggregate [[gamma-exposure-gex|GEX]] across different strike prices, specifically looking for strikes with extreme (e.g., highest absolute) `totalNetDollarGex1Pct` for call options. The strike with the most significant GEX concentration is then designated as the call wall.
## Where it matters
[[call-wall]]s are crucial for [[cl-market-making]] strategies, particularly in [[range-planning]]. They are used to define potential [[market-boundaries-cl]] for deploying [[liquidity-concentration]]. An unstable or oscillating call wall can lead to:
*   Excessive [[cl-rebalancing-condition|repositioning]] of liquidity, incurring high [[transaction_costs_in_options|gas and swap friction]].
*   A deployed plan that frequently disagrees with the current market signal, leading to suboptimal [[capital-allocation-liquidity-shape]].
## Evidence and limits
The source `[[dlmm-2026-call-wall-oscillates]]` demonstrates that call walls can be "bistable" if two strikes have similar aggregate gamma. In one observation, the call wall alternated between 150 and 121 strikes nine times in 6.7 hours, while the underlying asset moved only 1.41%. This oscillation was attributed to the selection rule lacking [[hysteresis]], causing rapid flips between near-tie strikes. This instability can lead to significant changes in planned range width (e.g., 939 bins vs. 402 bins).
## Related
[[gamma-exposure-gex]], [[market-boundaries-cl]], [[dlmm-bins]], [[range-planning]], [[call-wall-oscillation]], [[zero-gamma-level]]

## Update from dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md (2026-10-02)

# Call Wall
**In one line:** The strike price on the call side that exhibits the peak dollar [[gamma-exposure-gex|gamma]], often indicating a significant level of dealer hedging activity.
## Intuition
The call wall is conceptually a level where a large amount of call options are concentrated, leading to high gamma. Dealers hedging these positions may create a "pin" or "magnet" effect on the underlying price, as they need to buy/sell the underlying to maintain delta neutrality around this strike.
## Mechanism / math
The [[gex-intelligence]] engine identifies the call wall by calculating dollar gamma for all call strikes and selecting the strike with the maximum value.
## Where it matters
The call wall is intended to serve as the upper bound of the [[wall-envelope]] in [[range-planning]] for [[cl-market-making|concentrated liquidity market making]] strategies. It helps define the permissible range for liquidity deployment.
## Evidence and limits
*   **ATM Pin Behavior (F-024):** Analysis revealed that the call wall, as defined by peak dollar gamma, routinely sits very close to the [[spot-price]] (median 0.36% distance). This makes it function as an "at-the-money (ATM) pin" or "magnet" rather than a true upper bound or ceiling.
*   **Rejection Driver:** This ATM pin behavior frequently leads to the [[spot-price]] moving *above* the call wall, causing [[active-bin-out-of-range]] rejections (observed in 36% of ticks) because the [[wall-envelope]] fails to contain the active bin.
*   **Oscillation:** The call wall was observed to oscillate between a near-ATM pin (e.g., 121) and a far-out-of-the-money (OTM) strike (e.g., 150). However, the core issue is its function as a pin when near spot, not just its oscillation.
*   **Design Flaw:** The design step that did not hold was treating a peak-gamma strike (which is maximized at the money) as an upper bound.
*   **Resolution:** [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] was ratified to redefine wall selection, requiring the call wall to be side-constrained (i.e., always selected above the [[spot-price]]). This aims to ensure it functions as a proper upper bound for the [[wall-envelope]].
## Related
[[put-wall]], [[wall-envelope]], [[gamma-exposure-gex]], [[gex-intelligence]], [[range-planning]], [[spot-price]], [[active-bin-out-of-range]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]], [[dlmm-2026-wall-envelope-narrower-than-sigma-width|F-024]]
