---
domain: cl-market-making
tags:
- gex
- dlmm
- range-planning
- market-structure
- stability
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds.md
ingest_hashes:
- 430932d5ae7fe214
---
# Call Wall Oscillation
**In one line:** The phenomenon where a [[call-wall]] frequently switches between different strike prices due to a lack of [[hysteresis]] in its selection mechanism, even with minimal underlying price movement.
## Intuition
When the aggregate [[gamma-exposure-gex|GEX]] at two or more strike prices is very close, the algorithm used to identify the [[call-wall]] may flip between these strikes with minor fluctuations in open interest or market data. This creates an unstable signal for [[range-planning]].
## Mechanism / math
The oscillation occurs because the wall selection rule, which typically identifies the strike with the most extreme aggregate gamma (e.g., `totalNetDollarGex1Pct`), lacks a mechanism to maintain stability when two or more strikes are in a "near-tie." Without [[hysteresis]] or a tie-breaking rule, the wall can flip on consecutive market data ticks if the relative GEX values shift slightly.
## Where it matters
This instability has significant implications for [[cl-market-making]] strategies:
*   **Ruinous Repositioning:** Each flip of the [[call-wall]] can trigger a [[cl-rebalancing-condition|repositioning]] of [[liquidity-concentration]], leading to high [[transaction_costs_in_options|gas and swap friction]] from multiple withdraw-and-redeploy cycles.
*   **Invalidated Plans:** The deployed liquidity plan may routinely be based on a signal that the current market conditions contradict, leading to suboptimal [[capital-allocation-liquidity-shape]].
*   **Distorted Width:** Oscillating walls lead to large, rapid changes in the proposed range width (e.g., 19% price difference, 939-bin vs. 402-bin ranges), which can cause the deployed range to exclude the current spot price entirely.
## Evidence and limits
The `[[dlmm-2026-call-wall-oscillates]]` finding observed a [[call-wall]] oscillating nine times between 150 and 121 strikes over 6.7 hours, while the underlying spot price moved only 1.41%. This included instances where the wall flipped on consecutive 30-second ticks. The mean `totalNetDollarGex1Pct` for the two strikes differed by only ~5%, indicating a near-tie. The finding suggests solutions like implementing [[hysteresis]], a minimum dwell time, or a tie-margin rule in the [[gex-intelligence]] module.
## Related
[[call-wall]], [[gamma-exposure-gex]], [[range-planning]], [[dlmm-bins]], [[hedge-churn]], [[hysteresis]], [[market-boundaries-cl]]