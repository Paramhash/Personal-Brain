---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/FEE_COUNTER_G1_2026-09-30.md
bot_commit: 1fa5166
source_sha256: 384e00b1a0c073692c5592a0dac5f65f31234e342e8c2cc9a4d52746415893c9
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/FEE_COUNTER_G1_2026-09-30.md` at commit `1fa5166`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# FEE_COUNTER_G1 — [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Gate G1: The Per-Bin Fee Counters Verify (TICKET 027 Part 0)

- **Run:** 2026-09-30 16:07:06Z → 16:27:08Z. 3 samples 600 s apart (slots 452013622 → 452018118), plus a 30 s smoke run
  at 16:05Z.
- **Pool:** `5rCf1DM8LjKTw4YqhnoLcngyZYeNnQqztScTogYHAS6` (mainnet SOL/USDC, bin step 4, protocol share 1000 bps).
- **Range:** ±10% of the active bin = ±239 bins → 8 `BinArray` accounts (all initialised), 560 bins, one
  `getMultipleAccountsInfo` per sample.
- **Script:** `docs/operations/fee_counter_spike.js` (read-only). **Raw data:** `FEE_COUNTER_G1_2026-09-30.data.json`,
  including the first sample's raw account bytes as the Part 2 decoder fixture (public on-chain data).
- **Arithmetic:** the SDK's own claimable-fee formula. The fee credited to all LPs of bin b over an interval is
  `(supply_b >> 64) · Δ feeAmountPerTokenStored_b >> 64`.

## Result: G1 passes, with one check replaced

| G1 check | Result |
|---|---|
| 1. Layout and scale | **Pass.** 8/8 arrays decode through the SDK's account coder, 10,136 bytes each. The 2⁶⁴ scale is confirmed by check 3's agreement to 0.02%. |
| 2. Net of the protocol share | **Pass.** LP fees are 90.00% of all fees, and the protocol share is 10.00%. |
| 3. Reconciliation — as written (volume × fee rate) | **Not runnable.** The program's current `BinArray` has **no per-bin swap-input counters**. `amountXIn`/`amountYIn` in the SDK's older types now hold limit-order fields. [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]]'s Context is wrong on this point. |
| 3. Reconciliation — replacement (pool-wide protocol-fee counter) | **Pass, within 0.02%** (required: 5%). The table below gives the figures. |
| 4. Monotonicity | **Pass.** 0 decreases in 1,120 bin comparisons (and 0 in the smoke run). |

The replacement for check 3 compares the LP fees credited in range with the pool-wide `protocolFee` counter. It tests the
scale, the net-of-protocol question, and that ±10% holds every fee-earning bin, all at once, because the protocol counter
covers the whole pool.

| Interval | Side | LP fees (range) | Protocol fee Δ (pool-wide) | LP ÷ total | Expected |
|---|---|---:|---:|---:|---:|
| 16:07→16:17 | SOL | 0.397019 | 0.044100 | 0.900027 | 0.9 |
| 16:07→16:17 | USDC | 69.3840 | 7.7080 | 0.900015 | 0.9 |
| 16:17→16:27 | SOL | 0.479788 | 0.053227 | 0.900139 | 0.9 |
| 16:17→16:27 | USDC | 64.7640 | 7.1932 | 0.900035 | 0.9 |
| smoke (30 s) | USDC | 6.9015 | 0.7668 | 0.900001 | 0.9 |

## Other measurements

- **Fees land in few bins.** 5–6 bins showed fee growth per 10-minute interval, all near the active bin, which moved 2 bins
  per interval.
- **Supply drift inside an interval is negligible.** Crediting with end-of-interval supply instead of start-of-interval
  supply changes LP fees by ≤ 0.04%, so a 5-minute cadence is fine.
- **Record size:** about 201 bytes per bin as JSON, so 560 bins is about 113 KB per sample, or **about 32 MB/day** at a
  5-minute cadence. That is below [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]]'s 100–200 MB/day estimate, and dropping zero-supply bins would shrink it
  further.
- **RPC:** 1 call per sample, about 81 KB of account data.
- **Indicative only, not evidence (20 minutes, one hour of one day).**
  - Whole-pool LP fees were about $117–122 per 10 min: 0.40–0.48 SOL plus $65–69.
  - At the fee rate of about 0.040%, total fees of about $130 per 10 min imply roughly $47M/day of swap volume.
  - Against the pool's ≈ $4.4M TVL, that is roughly 38–40 bps/day on the **whole pool's** value. In-range liquidity near
    the active bin earns more per unit.
  - For scale, the gate's boundary is about 7.38 bps/day ([[adr-033-fee-yield-measurement-route|ADR-033]]). No conclusion is drawn from one 20-minute window;
    this is what Route 4 exists to measure properly.

## Open items for Part 2

1. **Limit-order fields.** `limitOrderFeeAskSide` / `limitOrderFeeBidSide` are non-zero in 22 of 560 bins. Two
   questions:
   - are limit-order fees a separate stream from `feeAmount*PerTokenStored`?
   - could a limit-order fill move the LP counters differently?

   The 0.02% agreement with the protocol counter says nothing is missing from the LP side over these intervals. The
   decoder should still record the two fields, and the reconciliation should be re-run on a day of data.
2. **Protocol-fee claims.** A claim resets `protocolFee` downward. The sampler must detect a negative Δ and skip that
   interval's reconciliation. None occurred here.
3. **Bin-array edges.** The ±10% range spans whole arrays (70 bins each). If the active bin moves near an array edge, the
   set of arrays changes. The sampler recomputes the set every sample, and a bin missing from one sample is a gap for that
   bin only.

## Decisions this needs ([[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]])

- **Accept the replacement for check 3,** since the as-written check cannot run on this program version, and record the
  correction to [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]]'s Context.
- **D1:** may Route 4 ratify the fee constant? **D2:** the ±10% range. **D3:** the start date.
- **Mark [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Active.** Then TICKET 027 Parts 1–7 can start.
