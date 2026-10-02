---
domain: cl-market-making
tags:
- dlmm
- fee-economics
- on-chain-data
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-fee-counter-g1-2026-09-30.md
ingest_hashes:
- a588578f1039032d
---
# Fee Amount Per Token Stored
**In one line:** A per-bin counter in a Dynamic Liquidity Market Maker (DLMM) that accumulates fees earned per unit of liquidity supplied to that specific bin, scaled by $2^{64}$.
## Mechanism / math
This counter is a critical component of the `[[dlmm-fee-counter]]` mechanism. When a trade occurs within a bin, a portion of the trade's value (the fee) is added to this counter, proportional to the liquidity in the bin. The value is scaled by $2^{64}$ to maintain precision for fractional fee amounts.

The change in this counter ($\Delta \text{feeAmountPerTokenStored}_b$) is used in conjunction with the bin's liquidity supply ($\text{supply}_b$) to calculate the actual LP fees for bin $b$ over an interval:
$$ \text{LP Fees}_b = (\text{supply}_b \gg 64) \cdot \Delta \text{feeAmountPerTokenStored}_b \gg 64 $$
## Where it matters
*   **Accurate LP Fee Calculation:** It is the fundamental building block for determining how much each liquidity provider earns from trading activity in their deployed `[[dlmm-bins]]`.
*   **Fee Distribution:** Ensures that fees are distributed proportionally to the amount of liquidity and the duration it was active within a specific bin.
*   **On-chain State:** Represents the immutable, accumulating record of fees within each bin, enabling transparent and verifiable fee accounting.
## Related
[[dlmm-fee-counter]]
[[dlmm-bins]]
[[dlmm-program]]
[[fee-economics]]