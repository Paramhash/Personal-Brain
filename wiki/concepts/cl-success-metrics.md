---
domain: cl-market-making
tags:
- performance-evaluation
- risk-management
- profitability
- capital-efficiency
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 94551e79f26042c2
---
# CL Success Metrics
**In one line:** The hierarchical criteria used to evaluate the performance of a [[cl-position]] and the overall market-making bot strategy, encompassing operational safety and financial returns.
## Intuition
Defining success clearly is essential for any automated trading system. These metrics provide a framework to objectively assess whether the bot is achieving its goals, guiding development, backtesting, and strategic adjustments. They prioritize operational survival before focusing on profitability.
## Mechanism / math
Success is defined hierarchically:
### Hard requirements
*   [[sol-rent-reserve]] preserved.
*   No collateral breach.
*   No forced liquidation.
*   No invalid or stale [[market-boundaries-cl]] used.
*   Withdrawal completes with both liquidity and hedge reconciled.

### Primary objective
$$
E_{close} > E_{start}
$$
The bot's final equity ($E_{close}$) must be greater than its starting equity ($E_{start}$), after valuing both [[sol-inventory]] and [[usdc-inventory]] at a defined reference price and subtracting all costs.

### Secondary objective
$$
E_{close} > E_{HODL\ benchmark}
$$
The bot's final equity must exceed that of a passive [[hodl-benchmark]] strategy, indicating outperformance.
## Where it matters
These metrics are fundamental for evaluating the effectiveness of the [[warehouse-manager-cl-inventory-strategy]]. They provide clear targets for the bot's operation and are used in backtesting and live performance monitoring. By prioritizing hard requirements, they ensure the bot's long-term viability before considering profit maximization.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] dedicates a section to "What Counts as Success?", outlining these hierarchical criteria. It acknowledges that a CL position changes inventory composition, making a simple profit calculation insufficient, thus requiring valuation at a reference price.
## Related
[[cl-position]]
[[equity-accounting]]
[[hodl-benchmark]]
[[sol-rent-reserve]]
[[market-boundaries-cl]]
[[blueprint-observability-contract]]
[[financial-trading-performance-metrics]]