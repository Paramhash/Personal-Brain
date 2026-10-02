---
domain: cl-market-making
tags:
- solana
- cost-accounting
- dlmm
- blockchain-mechanics
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-f-026-the-ev-gate-has-no-rent-term-so-wider-ranges-look-cheaper-than-they-are.md
ingest_hashes:
- d0f1fd12285a35c4
---
# Solana Rent
**In one line:** A cost on the Solana blockchain for storing data on-chain, which can be either permanently sunk or recoverable, and is critical for accurate cost accounting in [[cl-market-making]] strategies.
## Intuition
Solana rent is akin to a storage fee for data kept on the blockchain. Just as you might pay a deposit for a rental property that you get back when you move out, some on-chain storage costs are recoverable. However, other storage costs are like a non-refundable setup fee for a permanent structure, which you never get back.
## Mechanism / math
Solana rent is charged for storing data on-chain. For [[dlmm-bins]] deployments, it manifests in two primary forms:
1.  **Sunk Bin-Array Rent**: This portion is permanently paid by the entity that first initializes a bin array. Bin arrays are program-owned shared state that cannot be closed by the depositor, meaning the initial cost is not recoverable. This cost scales directly with the [[range-planning|width of the deployed range]] (i.e., the number of bins).
2.  **Recoverable Rent**: This applies to user-owned accounts, such as position accounts and associated token accounts (ATAs). The rent paid for these accounts can be recovered when the accounts are closed.
## Where it matters
Accurate accounting of [[solana-rent]] is crucial for evaluating the true cost and profitability of [[cl-market-making]] strategies, particularly for [[dlmm-bins]] deployments. Failure to include sunk rent terms in economic decision gates, such as the [[ev-gate]], can lead to:
-   **Misleading Cost Estimates**: Wider liquidity ranges may appear cheaper than they are, biasing deployment decisions.
-   **Capital Misallocation**: Strategies might deploy capital into ranges that are not economically viable when all sunk costs are considered.
-   **Unforeseen Losses**: The actual cost of maintaining or exiting a position could be significantly higher than initially calculated.

The finding `[[dlmm-2026-ev-gate-no-rent-term]]` demonstrated that sunk bin-array rent could be orders of magnitude larger than transaction fees, highlighting its importance in the overall cost structure.
## Evidence and limits
The `[[dlmm-2026-ev-gate-no-rent-term]]` finding revealed that sunk bin-array rent for a 203-bin range was 1,429 times the placeholder transaction fee, and for a 940-bin range, it was 5,001 times the placeholder. This quantitative evidence underscores the significant impact of this cost term. The issue was addressed by [[adr-040-sunk-deployment-rent-is-an-ev-term]], which incorporated `deploy_rent_sunk` into the [[ev-gate]]'s calculations.
## Related
[[dlmm-bins]], [[ev-gate]], [[adr-040-sunk-deployment-rent-is-an-ev-term]], [[adr-039-deploy-reserve-is-derived-from-the-plan]], [[cost-of-capital-spreads]], [[cl-market-making]], [[range-planning]]