---
domain: cl-market-making
tags:
- dlmm
- on-chain-data
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-fee-counter-g1-2026-09-30.md
ingest_hashes:
- 786491ad77245c23
---
# BinArray Account
**In one line:** A data structure within a Dynamic Liquidity Market Maker (DLMM) program that stores a contiguous range of concentrated liquidity bins on-chain.
## Intuition
To manage concentrated liquidity efficiently, a DLMM groups individual price bins into larger, manageable data structures. A `[[binarray-account|BinArray]]` account serves this purpose, holding a fixed number of `[[dlmm-bins]]` that span a specific price range. This allows for fetching and processing multiple bins with a single on-chain query.
## Key facts
*   **Size:** Each `[[binarray-account|BinArray]]` account is 10,136 bytes in size.
*   **Capacity:** Each account typically stores 70 individual `[[dlmm-bins]]`.
*   **Content:** Contains data for each bin, including liquidity supply, and fee counters like `[[fee-amount-per-token-stored]]`. In the current `[[dlmm-program]]` version, it also holds limit-order specific fields (`limitOrderFeeAskSide`, `limitOrderFeeBidSide`) which replaced older swap-input counters.
## How it is used here
`[[binarray-account|BinArray]]` accounts are fundamental for accessing and decoding the state of `[[dlmm-bins]]`. In the context of fee counter verification, multiple `[[binarray-account|BinArray]]` accounts are fetched to retrieve the `[[fee-amount-per-token-stored]]` values for all bins within a specified active range, enabling the calculation and reconciliation of LP fees.
## Related
[[dlmm-bins]]
[[dlmm-fee-counter]]
[[dlmm-program]]
[[fee-amount-per-token-stored]]