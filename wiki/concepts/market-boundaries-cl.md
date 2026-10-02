---
domain: cl-market-making
tags:
- concentrated-liquidity
- risk-management
- range-planning
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 09b3c041b85a19a0
---
# Market Boundaries CL
**In one line:** The upper and lower price limits that define the permissible and safe range for a [[cl-position]] deployment in a concentrated liquidity pool.
## Intuition
These boundaries act as guardrails, preventing the bot from deploying liquidity in price ranges that are deemed too risky or outside the intended operational scope. They provide a high-level safety envelope for the more granular liquidity placement.
## Mechanism / math
The source distinguishes between:
1.  **Raw GEX wall envelope:** Initial signals from [[gamma-exposure-gex]] data.
2.  **[[buffered-policy-envelope]]:** A wider, safer envelope derived from the raw GEX walls and a volatility allowance. This is used as the *hard deployment boundary*.
3.  **[[sigma-derived-deployed-window]]:** A narrower, volatility-based range used for the *actual CL placement* within the buffered envelope.

The [[cl-entry-strategy]] requires both boundaries to be valid and the active bin to be inside the [[buffered-policy-envelope]]. The [[cl-exit-strategy]] is triggered if the projected price path threatens to cross these boundaries.
## Where it matters
[[market-boundaries-cl]] are crucial for defining the risk profile of a [[cl-position]]. They directly inform the [[cl-entry-strategy]] by setting the outer limits for deployment and are a primary trigger for the [[cl-exit-strategy]] to prevent significant losses or unwanted inventory exposure. They are a key component of the bot's overall risk guardrails.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] mandates the use of two boundaries for the deployed position (downside and upside protection). It specifies that the [[buffered-policy-envelope]] should be used as the "hard deployment boundary." This policy is designed to prevent deployments into excessively risky or unmanageable price ranges.
## Related
[[buffered-policy-envelope]]
[[sigma-derived-deployed-window]]
[[gamma-exposure-gex]]
[[volatility]]
[[cl-entry-strategy]]
[[cl-exit-strategy]]
[[blueprint-range-planning]]
[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot]]