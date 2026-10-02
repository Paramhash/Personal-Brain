---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-050
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/050-fee-yield-from-on-chain-bin-fee-counters.md
bot_commit: c717b09
source_sha256: faad5a7ee301ac3c0e1d2142bef4cab05cb33b53a486222e3fcecc908967ce12
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/050-fee-yield-from-on-chain-bin-fee-counters.md` at commit `c717b09`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] — Fee Yield Is Measured Without Capital From Each Bin's On-Chain Fee-Per-Share Counters (Route 4)

- **Date:** 2026-09-30
- **Status:** **Active. Decided by the dispatcher 2026-09-30 ~16:30Z**, after G1 passed:
  - the replacement for G1 check 3 (reconciliation against the pool-wide protocol-fee counter) is accepted;
  - **D1 = yes:** Route 4 may ratify the fee-yield constant under [[adr-033-fee-yield-measurement-route|ADR-033]]'s unchanged threshold;
  - **D2 = ±10%** and **D3 = the first sample, 2026-09-30 16:48:24Z**, decided 2026-10-01 13:55Z (see the decision note below).
- **Amendment 1 (Active, ratified by the dispatcher 2026-10-01 14:38Z):** a ratified Route 4 value does not replace the gate's fee placeholder until
  [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] is implemented. See the end of this file.
- **Amends:** [[adr-033-fee-yield-measurement-route|ADR-033]], by adding a fourth fee-measurement route. [[adr-033-fee-yield-measurement-route|ADR-033]]'s Route 3 (direct accrual on a real position)
  and its capital gate are unchanged, as is its ratification threshold. §D1 decides what Route 4 may ratify.
- **Would own (if accepted):** a new read-only sampler and its own root; `observation_archive.md` gains a pointer, but
  the archive itself is untouched; `backtest_research.md` gains a measured fee side.
- **Touches:**
  - [[adr-032-observation-archive-ownership-and-isolation|ADR-032]] and [[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]] (the archive and its volume floor);
  - [[adr-033-fee-yield-measurement-route|ADR-033]] (the fee route and its ratification rules);
  - [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] and [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] (the gate and the hurdle consume the fee yield);
  - [[adr-048-health-alarms-to-the-operators-discord|ADR-048]] (a new notifier check).

## Context

**Fee income is the one EV and hurdle input that has never been measured on DLMM.**
- Every other term is now measured or modelled: σ ([[adr-047-provisional-sigma-estimator|ADR-047]]), rent ([[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]]), LVR, hedge cost and lifespan ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]),
  gas and slippage.
- The fee side of the research simulator is still expressed in units of volume V, and the gate's fee yield is the 10
  bps/day placeholder.
- [[adr-033-fee-yield-measurement-route|ADR-033]] put the gate boundary at about 7.38 bps/day, so the placeholder's 35% headroom is the single largest
  unknown in the go/no-go decision.

**[[adr-033-fee-yield-measurement-route|ADR-033]]'s chosen route cannot start.**
- Route 3 needs a small real position, and its capital gate is unapproved.
- So `fee_observation` has been `null` for the whole 21-day archive run, and [[adr-033-fee-yield-measurement-route|ADR-033]]'s fee window has not begun.
- [[adr-033-fee-yield-measurement-route|ADR-033]] rejected the other two routes:
  - **Route 1, reserve deltas:** these confound swaps with LP flow.
  - **Route 2, swap parsing:** it measures pool volume, and bridging from there to a position's accrual needs per-swap
    bin attribution. The archive's 30 s liquidity samples cannot reconstruct that attribution, and the resulting share
    model's error is as large as the decision margin.

**The program already keeps the quantity Route 3 would read.** The DLMM SDK (`@meteora-ag/dlmm`) exposes, on every bin
of a `BinArray` account:
- `feeAmountXPerTokenStored` / `feeAmountYPerTokenStored`: cumulative fees credited per unit of the bin's liquidity
  share. A position's pending fee in a bin is its share × the growth of these counters since its last update. This is
  how the program itself credits LPs, so it is Route 3's quantity per unit share.
- `amountXIn` / `amountYIn`: cumulative swap input into the bin, which is DLMM volume measured per bin.
- `liquiditySupply`: the bin's total share supply, already sampled by `bin_samples`.

Route 2's objection does not apply. The program attributes each swap's fee to the bins it crossed, at the slot it
happened. This route reads the program's own attribution; it does not reconstruct it.

**The recorder cannot carry this.** `dist/` is frozen until the archive run ends on 2026-10-18 ([[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]]), and the
archive has one writer.

## Gate G1 — verification before anything is built (read-only spike)

This ADR is accepted only if a read-only spike confirms all of the following on the mainnet SOL/USDC pool. The spike
makes a handful of account reads, writes nothing and runs no process.

1. **Layout and scale.**
   - The counters decode from the `BinArray` accounts with the documented layout.
   - Their fixed-point scale is known and documented (expected Q64-style u128; to be confirmed, not assumed).
   - Values are recorded as exact integer strings.
2. **Net of the protocol share.** Whether the per-share counters exclude the protocol fee. The measurement must be what
   an LP receives.
3. **Reconciliation.** Over at least two intervals of about 10 minutes, the fees implied by the counters,
   Σ_b Δ(feePerToken_b) × liquiditySupply_b, must match Σ_b Δ(amountIn_b) × fee rate × (1 − protocol share) within
   **5%** on each token side. The fee rate is the recorded `pool_base_fee_bps` plus `pool_variable_fee_bps`.
4. **Monotonicity.** Counters never decrease, and a bin array that is re-initialised or closed is detectable.

If G1 fails, this ADR is withdrawn and the finding is recorded in `todo/findings/`.

## Decision (proposed)

1. **Route 4, `BIN_FEE_GROWTH`.** Fee yield is measured from the per-bin fee-per-share counters.
   - A **hypothetical position** of stated capital and range, the same one the research simulator already places, is
     credited Σ_b share_b × Δ(feePerToken_b) over each interval.
   - `share_b` = the position's liquidity ÷ (the bin's supply + the position's liquidity), using the simulator's own
     shape weights ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]).
   - This is the only modelled term: the position's dilution of each bin. It is the same arithmetic the program applies
     to a real deposit.
2. **Collection.** A separate read-only sampler process, not the recorder and not a monitor:
   - **One `getMultipleAccounts` every 5 minutes** for the `BinArray` accounts within ±10% of the active bin (about 7
     arrays at bin step 4), on the existing RPC. It adds no new network host.
   - **Cumulative raw counters** (`feeAmount*PerTokenStored`, `amount*In`, `liquiditySupply`) per bin, as exact
     strings, into daily files under its own root (default `C:\observation\dlmm-fee-growth\`).
     - Because the counters are cumulative, a missed sample loses no fees, only resolution.
     - A gap is marked, never interpolated.
   - The same [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] disciplines apply:
     - one writer, with a lock file;
     - a 50 GiB free-space floor;
     - refused at or inside the archive root;
     - numbers, enum labels, public addresses and timestamps only.
   - The notifier gains a `fee-growth` check ([[adr-048-health-alarms-to-the-operators-discord|ADR-048]] discipline: metadata only).
3. **Readers.** Only the offline research CLI reads these files. Research gains a measured fee section:
   - fee yield in bps/day for the policy grid;
   - per UTC day and per [[adr-033-fee-yield-measurement-route|ADR-033]] 3-day sub-window, the same partition the rest of the report uses;
   - with the simulator's fee side converted from units of volume V to measured quote.
4. **Cross-check, not evidence.** Orca's measured whole-pool fees ÷ TVL (7762's pool statistics) are reported beside the
   DLMM figures as a consistency check. They are a different venue and a whole-pool figure, and ratify nothing.

## Decision points for the dispatcher

- **D1 — May Route 4 ratify the fee-yield constant?**
  - **Recommended:** yes, under [[adr-033-fee-yield-measurement-route|ADR-033]]'s unchanged threshold:
    - 21 consecutive days at ≥95% coverage;
    - seven 3-day sub-windows;
    - max/min ≤ 3×;
    - the **10th-percentile** sub-window yield.
  - **Alternative:** Route 4 is evidence only, and ratification still needs Route 3's position.
- **D2 — The ±10% bin range.** A wider range covers wider simulated windows at more RPC per sample; ±10% covers the
  [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] σ window and the buffered envelope at today's σ.
- **D3 — Start date.** The run should start as soon as G1 passes and the ticket is built. A start around 2026-10-01
  completes 21 days around 2026-10-22, four days after the archive run ends. Route 4's window is its own and does not
  need to align with the archive's.

## What this route does not measure

These must not be presented as measured:
- **Fees in bins with no liquidity.** Swaps skip empty bins, so their counters do not move. A position there would
  attract flow that did not happen. Credited as zero, which is conservative.
- **Own-position effects on flow.** A real position's liquidity changes the bins' prices and depth, and so the routing
  of swaps. The dilution in §1 covers the share, not any change in volume.
- **Claiming, compounding and rent.** Those are [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]]'s and the simulator's, not this route's.
- **Anything off the pool.** Other SOL/USDC venues and aggregator routing are observed only through this pool's
  counters.

## Consequences

- The simulator's break-even stops being "in units of V". The report can say, per policy, whether measured fees cover
  modelled costs, and the [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] hurdle gains a measured fee line to compare against.
- A fourth writer on the archive's volume, bounded by the 50 GiB floor. Rough size: 7 arrays × 70 bins × a few hundred
  bytes, every 5 minutes, is about 100–200 MB/day. To be measured in G1, and a compact record may shrink it.
- Route 3 remains available and would still be the stronger evidence, since it is a real position's own accrual. Route
  4 makes it unnecessary for ratification only if D1 says so.

## Alternatives considered

- **Route 3 now.** Needs capital approval, which is outside this ADR.
- **Meteora's public pair API** (24 h and cumulative volume and fees). A new network host, like the [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] amendment
  for Orca, and a whole-pool figure. Kept as a fallback if G1 fails.
- **Adding the read to the 7761 monitor.** It would work for RPC budget, but it mixes a research input into a display
  process, and [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1 A4 limits research reads of its recording to σ.
- **Changing the recorder.** Frozen until 2026-10-18, and the archive has one writer.
- **Calibrating from Orca alone.** A different venue and a whole-pool figure; the cross-check in §4 is the most it
  supports.

## Reversed by

- G1 failing.
- A program upgrade that changes the `BinArray` layout or the counters' meaning (detected by the decoder's discriminator
  and size checks; fail closed).
- Route 3 evidence contradicting Route 4 by more than the [[adr-033-fee-yield-measurement-route|ADR-033]] 3× stability band.

## G1 result — 2026-09-30 16:27Z (TICKET 027 Part 0)

- **G1 passes, with check 3 replaced.** See `todo/findings/FEE_COUNTER_G1_2026-09-30.md`.
  - Checks 1, 2 and 4 pass.
  - LP fees in ±10% ÷ (LP + the pool-wide protocol-fee counter) = 0.90000–0.90014, against 0.9 expected, on both
    sides over two 10-minute intervals.
- **Correction to Context.** The program's current `BinArray` has **no** per-bin swap-input counters. The SDK's
  `amountXIn`/`amountYIn` belong to an older layout; those bytes now hold limit-order fields. Check 3 as written
  (volume × fee rate) cannot run. The protocol-fee reconciliation replaces it, subject to the dispatcher's acceptance.
  It is stronger, because the protocol counter is pool-wide and so also confirms the ±10% range holds every fee-earning
  bin.
- **Sizing:** about 32 MB/day, below the 100–200 MB/day estimated in Consequences. One RPC call of about 81 KB per
  sample.

## Acceptance note — 2026-09-30 ~16:30Z

- Accepted by the dispatcher.
- **G1 check 3 is replaced:** in-range LP fees ÷ (LP fees + the pool-wide `protocolFee` counter Δ) must equal
  1 − protocolShare, within 5%. The sampler re-runs this reconciliation on every interval without a protocol-fee claim.
  It is a standing data-quality check, not a one-off.
- **D1 = yes.** Route 4 is a ratification route in its own right. Ratification needs [[adr-033-fee-yield-measurement-route|ADR-033]]'s threshold, unchanged:
  - 21 consecutive days at ≥ 95% coverage;
  - seven 3-day sub-windows, with max/min ≤ 3×;
  - the ratified value is the 10th-percentile sub-window yield.
- **Ratification is separate.** It stays a dispatcher act on the evidence, per [[adr-033-fee-yield-measurement-route|ADR-033]]'s ratification path. It is not
  automatic when the window completes.

## Decision note — 2026-10-01 13:55Z: D2 and D3

- **D2 = ±10%, unchanged.** The reason given under D2 above is wrong, and is corrected here:
  - ±10% does **not** cover the buffered envelope. Across 8,966 TICKET T run 2 records the buffered envelope spans
    644–858 bins (median 712), and the raw envelope 854–1,142. ±10% at bin step 4 is 479 bins.
  - That does not matter for this route. Fees accrue only in bins that price trades through, and the sampler re-centres
    on the active bin every sample, so the range must cover the active bin's move between samples, not a position's
    width. Over the first 252 consecutive sample pairs, |Δ active bin| per 5 min was median 2, p99 13 and max 16 bins,
    against 239 each side: about 15× headroom.
  - A bin missing from either sample of an interval is credited zero (`lpFeesByBin` pairs only bins present in both).
    That is exact while price never trades beyond the range within one interval, which the move data above shows.
  - Widening would add storage for no gain. Narrowing would save little (about 36 MB/day) and needs a restart, which
    leaves a gap in the window.
- **D3 = the first sample, 2026-09-30 16:48:24Z** (run `feegrowth-2026-09-30T16-48-24-240Z-29660`), which is what
  "start when built" produced. The 21-day window completes 2026-10-21 16:48Z. The 3-day sub-windows run from this start,
  so the first closes 2026-10-03 16:48Z. The window stays independent of the archive's.

## Implementation note — 2026-09-30 16:31Z–16:45Z (TICKET 027 Parts 1–6)

- **Built:**
  - the blueprint `fee_growth.md`;
  - `src/feegrowth/`: record, counters, accrual, sample builder, writer, config and the sampler on 7763;
  - the notifier `fee-growth` check;
  - research §I;
  - the launcher `fee-growth`.
  - Tests: 1126/1126, with decoding and the reconciliation checked against the G1 spike's real mainnet bytes.
- **Per-interval reconciliation is noise-prone; the aggregate is the check.**
  - Found in the smoke run: a 1-minute interval read USDC LP ÷ total = 0.74.
  - Summing "all LP fees" as opening supply × Δ fee-per-share misses fees earned by liquidity that enters and leaves
    between samples (just-in-time).
  - A position's own accrual (own shares × Δ fee-per-share) is unaffected.
  - So the per-interval flag is logged as informational, and research §I reports the aggregate over all intervals,
    which is the standing check.
- **§4's Orca cross-check is deferred.** Reading 7762's recorded pool statistics for research would exceed [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]]
  Amendment 1 A4 (research reads `observedAtMs` and `sigmaEstimate` only). It needs an A4 extension.
- **Record size:** about 125 KB per sample (560 bins), about 36 MB/day at a 5-minute cadence.

## Amendment 1 — 2026-10-01: Route 4's value does not reach the gate until [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] is implemented

- **Status:** **Active. Ratified by the dispatcher 2026-10-01 14:38Z.** In the dispatcher's words: "maintain the lock that prevents
  Route 4 measured fees from driving the live EV gate until the cost engine reflects the calibrated model". It does not
  change the sampler, the window or D1–D3.
- **How the lock is held today:**
  - The gate's fee input is the constant `PLACEHOLDER_FEE_YIELD_PER_HORIZON` (`evCalculator.ts:115`).
  - Nothing under `src/decision/` imports the fee-growth sampler or its records. Route 4 data reaches only research
    (§I), the sampler itself and the notifier.
  - So the lock is a governance rule on that constant. Changing it while A1 stands needs this amendment reversed.
- **Amends:** D1 ("Route 4 may ratify the fee-yield constant") — it adds a condition on **using** a ratified value,
  not on ratifying one.

### Context

- §I measures 80–141 bps/day for the top policies. The gate's hurdle on today's live state is 62.5 bps/day, because
  its LVR is range-blind and it has no hedge-cost term
  (`todo/findings/EV_GATE_VS_SIMULATOR_2026-10-01.md`).
- A Route 4 value written into `PLACEHOLDER_FEE_YIELD_PER_HORIZON` today would make the gate pass positions the
  simulator nets at −150 to −240 bps/day.
- The earliest ratification is when the window completes, 2026-10-21 16:48Z.

### Decision

- **A1.** Route 4 may still ratify a fee yield under D1 and [[adr-033-fee-yield-measurement-route|ADR-033]]'s threshold. The ratified value is recorded, but it
  **does not replace** `PLACEHOLDER_FEE_YIELD_PER_HORIZON` until [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] is Active **and** implemented in the root
  that is being promoted. [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] is the range-dependent LVR and the hedge-drag term.
- **A2.** Until then, research and the monitors may show the ratified value beside the gate, labelled "ratified, not
  in the gate ([[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] A1)".
- **A3.** If [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] is rejected, A1 stands until a different ADR fixes the gate's cost side. The fee input does not
  move on its own.

### Reversed by

[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] implemented and promoted (A1 is then spent), or the dispatcher accepting a gate that prices fees against an
unchanged cost side.
