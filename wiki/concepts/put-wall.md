---
domain: cl-market-making
tags:
- dlmm
- gex
- market-making-strategy
- findings
aliases: []
created: 2026-10-02
reviewed: false
source_origin: dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md
ingest_hashes:
- 3df16beb178ce745
---
# Put Wall
**In one line:** The strike price on the put side that exhibits the peak dollar [[gamma-exposure-gex|gamma]], often indicating a significant level of dealer hedging activity.
## Intuition
Similar to the [[call-wall]], the put wall represents a strike where a large concentration of put options leads to high gamma. Dealer hedging around this level can influence the underlying price. However, put open interest often clusters below [[spot-price]] as downside protection, displacing the gamma peak downwards.
## Mechanism / math
The [[gex-intelligence]] engine identifies the put wall by calculating dollar gamma for all put strikes and selecting the strike with the maximum value.
## Where it matters
The put wall is intended to serve as the lower bound of the [[wall-envelope]] in [[range-planning]] for [[cl-market-making|concentrated liquidity market making]] strategies. It helps define the permissible range for liquidity deployment.
## Evidence and limits
*   **Effective Lower Bound (F-024):** Unlike the [[call-wall]], the put wall was consistently found to be significantly below the [[spot-price]] (median 14.98% distance). This displacement allows it to function effectively as a lower bound for the [[wall-envelope]].
*   **No Rejections Below:** In the observed data (1336 records), the [[spot-price]] was never found to be below the put wall, indicating its robust performance as a lower boundary.
*   **Structural Asymmetry:** The effectiveness of the put wall as a lower bound is attributed to the structural clustering of put open interest well below spot, which displaces the peak gamma downwards. This contrasts with the [[call-wall]]'s tendency to act as an at-the-money (ATM) pin.
*   **Resolution:** While the put wall generally functioned as intended, [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] was ratified to redefine wall selection for both sides, ensuring that the put wall is explicitly side-constrained (always selected below the [[spot-price]]) to maintain its role as a lower bound.
## Related
[[call-wall]], [[wall-envelope]], [[gamma-exposure-gex]], [[gex-intelligence]], [[range-planning]], [[spot-price]], [[active-bin-out-of-range]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]], [[dlmm-2026-wall-envelope-narrower-than-sigma-width|F-024]]