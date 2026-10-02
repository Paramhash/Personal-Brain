---
domain: cl-market-making
tags:
- dlmm
- smart-contract
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-fee-counter-g1-2026-09-30.md
ingest_hashes:
- aeaed0c8317f9341
---
# DLMM Program
**What it is:** The smart contract or on-chain program that implements the core logic and mechanics of a Dynamic Liquidity Market Maker (DLMM).
## Key facts
*   **Concentrated Liquidity:** Manages liquidity provision across discrete price ranges, or `[[dlmm-bins]]`.
*   **Fee Accounting:** Incorporates mechanisms like the `[[dlmm-fee-counter]]` and `[[fee-amount-per-token-stored]]` to accurately track and distribute trading fees to liquidity providers.
*   **Protocol Share:** Configurable `[[protocol-fee]]` mechanism to allocate a portion of trading fees to the protocol itself.
*   **Data Structures:** Utilizes specialized on-chain accounts, such as `[[binarray-account|BinArray]]` accounts, to store and manage bin data efficiently.
*   **Evolution:** The program's data structures can evolve; for example, `[[binarray-account|BinArray]]` accounts may repurpose fields (e.g., for limit-order data) over time.
## How it is used here
The `[[dlmm-program]]` is the subject of ongoing verification and auditing to ensure its financial logic, particularly regarding fee collection and distribution, operates as intended. The fee counter verification (FEE_COUNTER_G1) directly assessed the correctness of its internal fee accounting.
## Related
[[dlmm-bins]]
[[dlmm-fee-counter]]
[[binarray-account]]
[[fee-amount-per-token-stored]]
[[protocol-fee]]