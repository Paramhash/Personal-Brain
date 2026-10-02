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
- d84ea5720a2a0985
---
# FEE_COUNTER_G1 — ADR-050 Gate G1: The Per-Bin Fee Counters Verify (2026)
**Type:** docs
## Claim
The per-bin fee counters within the DLMM program accurately record liquidity provider (LP) fees, demonstrating reconciliation with pool-wide protocol fees within a 0.02% tolerance and exhibiting strict monotonicity. This validates the fundamental fee accounting mechanism for concentrated liquidity bins.
## Method and data
The verification was conducted on a mainnet SOL/USDC DLMM pool (bin step 4, protocol share 1000 bps) over a 20-minute interval (3 samples, 600 seconds apart) on 2026-09-30. A read-only JavaScript script (`docs/operations/fee_counter_spike.js`) was used to query and decode 8 `[[binarray-account|BinArray]]` accounts covering a ±10% range around the active bin. The SDK's claimable-fee formula `(supply_b >> 64) · Δ feeAmountPerTokenStored_b >> 64` was used for arithmetic. Raw account bytes from the first sample were used as a decoder fixture.
## Key results
*   **Layout and scale:** All 8 `[[binarray-account|BinArray]]` accounts (10,136 bytes each) decoded successfully via the SDK's account coder. The 2⁶⁴ scaling factor for fee amounts was confirmed.
*   **Net of protocol share:** LP fees consistently represented 90.00% of total fees, with the protocol share at 10.00%, matching the configured 1000 bps.
*   **Reconciliation (replacement check):** A replacement check (due to the absence of per-bin swap-input counters in the current program version) compared in-range LP fees with the pool-wide `[[protocol-fee]]` counter. This reconciliation passed within 0.02% (well within the required 5% tolerance).
    *   For SOL, LP fees were 0.397019 and 0.479788 for two 10-minute intervals, with corresponding protocol fees of 0.044100 and 0.053227.
    *   For USDC, LP fees were 69.3840 and 64.7640 for two 10-minute intervals, with corresponding protocol fees of 7.7080 and 7.1932.
    *   LP ÷ total ratios were consistently around 0.9000.
*   **Monotonicity:** No decreases were observed across 1,120 bin comparisons, confirming that fee counters only increase.
*   **Fee distribution:** Fee growth was concentrated in 5–6 bins near the active bin, which moved 2 bins per interval.
*   **Supply drift:** Using end-of-interval supply vs. start-of-interval supply changed LP fees by ≤ 0.04%, indicating a 5-minute cadence for fee recording is sufficient.
*   **Data volume:** Each sample generated ~113 KB of JSON data for 560 bins, translating to ~32 MB/day at a 5-minute cadence, which is below the ADR-050 estimate of 100–200 MB/day.
*   **RPC usage:** 1 RPC call per sample, fetching ~81 KB of account data.
*   **Indicative volume:** Whole-pool LP fees were ~$117–122 per 10 minutes, implying ~ $47M/day swap volume at a 0.040% fee rate, against a pool TVL of ~$4.4M. This suggests 38–40 bps/day on the whole pool's value.
## Assumptions and limits
The findings are based on a short 20-minute observation window on a single DLMM pool. The original check 3, which relied on per-bin swap-input counters, was not runnable due to changes in the `[[dlmm-program]]`'s `[[binarray-account|BinArray]]` structure (now holding limit-order fields). The replacement check, while effective, covers the whole pool for reconciliation.
## Concepts introduced or used
[[dlmm-fee-counter]]
[[binarray-account]]
[[fee-amount-per-token-stored]]
[[protocol-fee]]
[[dlmm-program]]
[[dlmm-bins]]
[[fee-yield]]
[[adr-050-fee-yield-from-on-chain-bin-fee-counters]]