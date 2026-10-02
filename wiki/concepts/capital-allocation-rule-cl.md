---
domain: cl-market-making
tags:
- capital-management
- risk-management
- decision-making
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 218f579a9fb5ff1e
---
# Capital Allocation Rule CL
**In one line:** A policy that determines the maximum amount of capital that can be deployed into a [[cl-position]], ensuring that critical operational reserves and risk limits are respected.
## Intuition
Even if a [[cl-position]] appears economically attractive, over-allocating capital can jeopardize the bot's overall stability or ability to manage other risks. This rule acts as a safeguard, ensuring that deployments are always within prudent limits, preserving the bot's capacity for future operations and unexpected events.
## Mechanism / math
The rule for deployed capital ($C_{deploy}$) is defined as the minimum of three limits:
$$
C_{deploy} = \min( C_{economic\ limit}, C_{reserve\text{-}safe\ limit}, C_{collateral\text{-}safe\ limit} )
$$
*   `C_economic_limit`: The maximum capital justified by the expected economic returns.
*   `C_reserve-safe_limit`: The maximum capital that can be deployed while keeping [[sol-rent-reserve]] and [[sol-execution-reserve]] untouched.
*   `C_collateral-safe_limit`: The maximum capital that can be deployed without breaching collateral requirements or other risk guardrails.
## Where it matters
This rule is a crucial part of the [[cl-entry-strategy]] and overall [[warehouse-manager-cl-inventory-strategy]]. It prevents the bot from deploying its full inventory, ensuring that a portion remains liquid and available for operational needs or to absorb unexpected losses. It directly contributes to the bot's resilience and long-term survival.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly recommends this rule as a "practical capital allocation rule" for deploying "surplus capital." This highlights its role in ensuring that deployments are always within safe and sustainable bounds.
## Related
[[cl-entry-strategy]]
[[sol-rent-reserve]]
[[sol-execution-reserve]]
[[cl-position]]
[[risk-management-team-agent]] (conceptual link to risk management)
[[blueprint-risk-guardrails]]