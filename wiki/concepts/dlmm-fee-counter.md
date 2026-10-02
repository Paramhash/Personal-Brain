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
- 0cb1c077da944b5d
---
# DLMM Fee Counter
**In one line:** A mechanism within a Dynamic Liquidity Market Maker (DLMM) program that tracks fees earned by liquidity providers (LPs) on a per-bin basis.
## Intuition
In a concentrated liquidity AMM like a DLMM, liquidity is segmented into discrete price ranges or "bins." Each bin can accumulate fees independently as trades occur within its price range. The DLMM fee counter provides a granular record of these fees, allowing for precise calculation of earnings for LPs whose capital is deployed in specific bins. This ensures that LPs are compensated accurately based on the trading activity their specific liquidity positions facilitate.
## Mechanism / math
The fee credited to all LPs of a specific bin $b$ over an interval is calculated using the formula:
$$ \text{LP Fees}_b = (\text{supply}_b \gg 64) \cdot \Delta \text{feeAmountPerTokenStored}_b \gg 64 $$
Where:
*   $\text{supply}_b$ is the total liquidity supply in bin $b$.
*   $\Delta \text{feeAmountPerTokenStored}_b$ is the change in the `[[fee-amount-per-token-stored]]` counter for bin $b$ over the interval.
*   The `>> 64` operation indicates a right bit shift by 64, effectively dividing by $2^{64}$, which is used for scaling fixed-point numbers in the program.

This mechanism relies on the `[[fee-amount-per-token-stored]]` value, which accumulates fees per unit of liquidity.
## Where it matters
*   **LP Compensation:** Directly determines the fees earned by liquidity providers for their positions in specific `[[dlmm-bins]]`.
*   **Fee Yield Measurement:** Essential for calculating `[[fee-yield]]` for different liquidity strategies and ranges.
*   **Protocol Economics Validation:** Allows for verification that the distribution of fees between LPs and the `[[protocol-fee]]` is correct and consistent with the protocol's configuration.
*   **On-chain Data Analysis:** Provides granular data for analyzing trading activity and fee generation across different price points.
## Evidence and limits
Verification of a SOL/USDC DLMM pool showed that the per-bin fee counters reconcile with the pool-wide `[[protocol-fee]]` counter within 0.02% and exhibit strict monotonicity (counters only increase). This confirms the accuracy and integrity of the fee recording. However, the original design's per-bin swap-input counters were found to be repurposed for limit-order fields, necessitating a replacement reconciliation check.
## Related
[[dlmm-bins]]
[[fee-yield]]
[[adr-050-fee-yield-from-on-chain-bin-fee-counters]]
[[protocol-fee]]
[[dlmm-program]]
[[fee-amount-per-token-stored]]