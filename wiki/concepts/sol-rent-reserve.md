---
domain: cl-market-making
tags:
- solana
- operational-risk
- capital-management
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 04178413fe62f4bd
---
# SOL Rent Reserve
**In one line:** A dedicated portion of a Solana-based market-making bot's [[sol-inventory]] that is explicitly set aside to cover the ongoing rent requirements for its on-chain accounts.
## Intuition
On the Solana blockchain, accounts require a minimum balance of SOL to remain active (rent). If an account's SOL balance falls below this threshold, it can be deallocated, leading to loss of data or operational failure. The [[sol-rent-reserve]] ensures that the bot's critical accounts are always funded, guaranteeing operational continuity regardless of market-making activities.
## Mechanism / math
The [[sol-rent-reserve]] is subtracted from the total [[sol-inventory]] (`SOL_wallet`) before determining the `SOL_free` amount available for deployment:
$$
SOL_{free} = SOL_{wallet} - SOL_{rent\ reserve} - SOL_{execution\ reserve}
$$
This reserve is considered "untouched" and is a hard constraint for the [[cl-entry-strategy]].
## Where it matters
This reserve is a critical component of the bot's operational risk management. Failure to maintain the [[sol-rent-reserve]] could lead to the deactivation of the bot's on-chain programs or liquidity positions, resulting in significant losses or complete operational shutdown. It is a non-negotiable prerequisite for any capital deployment.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly states that the "Rent and execution reserves remain untouched" as a primary condition for entering a position. This highlights its importance as a hard requirement for the bot's survival.
## Related
[[sol-inventory]]
[[sol-execution-reserve]]
[[cl-entry-strategy]]
[[cl-closing-procedure]]
[[cl-success-metrics]]
[[adr-030-deployment-sol-reserve]]