---
domain: cl-market-making
tags:
- operational-workflow
- risk-management
- inventory-management
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 7845bd09d63780d3
---
# CL Closing Procedure
**In one line:** A coordinated, multi-step sequence of actions taken to safely unwind a [[cl-position]] and reconcile the bot's inventory and hedging positions.
## Intuition
Closing a [[cl-position]] is not just about withdrawing liquidity; it's a complex process that involves disentangling the bot's various financial and operational components. A structured closing procedure ensures that all aspects are handled correctly, minimizing residual risk, preventing errors, and preparing the bot for future deployments.
## Mechanism / math
The closing procedure involves the following steps:
1.  Stop adding or concentrating liquidity.
2.  Withdraw CL liquidity from the pool.
3.  Reconcile the remaining [[sol-inventory]] and [[usdc-inventory]].
4.  Recompute the [[cl-hedge-target]] based on the *remaining* SOL inventory (`q*unwind = -x_remaining`).
5.  Resize or close the hedge position.
6.  Confirm all venue balances.
7.  Restore [[sol-rent-reserve]] and [[sol-execution-reserve]].
8.  Calculate final equity.
## Where it matters
This procedure is critical for ensuring operational integrity and accurate accounting after a [[cl-position]] is closed. It prevents situations where residual inventory or unmanaged hedges could expose the bot to unexpected risks. By restoring reserves, it also ensures the bot is ready for subsequent deployments.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] dedicates a section to "Closing Procedure," detailing these seven steps. It specifically highlights the importance of recomputing the hedge target based on *remaining* inventory during unwinding, rather than the original position inventory.
## Related
[[cl-exit-strategy]]
[[cl-position]]
[[sol-inventory]]
[[usdc-inventory]]
[[sol-rent-reserve]]
[[sol-execution-reserve]]
[[cl-hedge-target]]
[[equity-accounting]]
[[blueprint-liquidity-position-manager]]