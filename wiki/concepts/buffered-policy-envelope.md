---
domain: cl-market-making
tags:
- concentrated-liquidity
- risk-management
- range-planning
- gex
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 95c3ffc7e4c2a095
---
# Buffered Policy Envelope
**In one line:** A set of hard deployment boundaries for a [[cl-position]], derived from raw GEX wall signals and adjusted by a volatility allowance to provide a safety margin.
## Intuition
While raw [[gamma-exposure-gex]] walls might indicate significant market interest at certain price levels, relying solely on them can be risky due to their dynamic nature and potential for rapid shifts. The [[buffered-policy-envelope]] adds a safety buffer, creating a wider, more conservative range that acts as the ultimate constraint for liquidity deployment, protecting against sudden market movements.
## Mechanism / math
The source states that the [[buffered-policy-envelope]] should be used as the "hard deployment boundary." The actual liquidity placement occurs within a narrower [[sigma-derived-deployed-window]], which is contained within this envelope.
The [[cl-entry-strategy]] requires the active bin to lie inside this envelope. The [[cl-exit-strategy]] considers the distance to these boundaries for proactive withdrawal.
## Where it matters
This envelope is a critical component of the [[market-boundaries-cl]] and the bot's risk management framework. It ensures that even if the more granular [[sigma-derived-deployed-window]] is aggressive, the overall position remains within a safe, predefined range. It directly influences the [[boundary-threat-exit]] trigger.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly distinguishes the "buffered policy envelope" from the "raw GEX wall envelope" and the "actual sigma-derived deployed window." It mandates using the buffered envelope as the "hard deployment boundary," indicating its role as a primary risk control.
## Related
[[market-boundaries-cl]]
[[sigma-derived-deployed-window]]
[[gamma-exposure-gex]]
[[volatility]]
[[cl-entry-strategy]]
[[cl-exit-strategy]]
[[blueprint-range-planning]]
[[adr-041-wall-buffer-and-proximity-exit-are-one-policy]]