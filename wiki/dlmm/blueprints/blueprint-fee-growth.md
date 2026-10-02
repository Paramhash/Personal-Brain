---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/fee_growth.md
bot_commit: 1fa5166
source_sha256: 28cf31a4bf65482fc7520a4a3c6ee5997b3bd7b18d919f8f38b734c68c08448c
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/fee_growth.md` at commit `1fa5166`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Fee Growth Sampler — Blueprint ([[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]], TICKET 027)

> Owns: `src/feegrowth/`; the sampler process; its root (default `C:\observation\dlmm-fee-growth\`); research §I's
> reader (`src/backtest/research/feeGrowthReader.ts`).
> Decision: [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] (Active 2026-09-30 ~16:30Z; G1 passed; D1 = yes). Amends [[adr-033-fee-yield-measurement-route|ADR-033]] by adding Route 4.

## 1. Scope

The sampler measures what a DLMM position in any range would earn in fees, without holding one, by recording each bin's
on-chain fee-per-share counters.
- **Source:** the program's own per-bin attribution of each swap's fee (`feeAmountX/YPerTokenStored`). Nothing is
  reconstructed from volume.
- **Readers:** the offline research simulator only.
- **What it is not:**
  - no position, no signer, no transaction;
  - not the observation archive, and not the recorder;
  - not a monitor;
  - not a runtime input to the EV gate. The gate's fee constant changes only by ratification ([[adr-033-fee-yield-measurement-route|ADR-033]], [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] D1).

## 2. Boundary

1. **Read-only.** One `getMultipleAccountsInfo` per sample: the `LbPair` account plus the `BinArray` accounts covering
   ±`FEEGROWTH_RANGE_PCT` of the active bin, on the observer's existing RPC endpoint. **No new network host.**
2. **Endpoint secrecy.**
   - The RPC is resolved by `resolveObserverConfig` from `observer.env`, by key name.
   - No endpoint, credential, path or environment value is printed, logged, written or served.
   - Errors are reduced to fixed reason codes (`observability_contract.md` §2).
3. **Its own root, with the [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] disciplines:**
   - one writer (`recording.lock`, holding the pid; a live holder refuses);
   - a free-space floor, `FEEGROWTH_MIN_FREE_BYTES` (default 50 GiB, never below 10 GiB), checked before every append,
     with a `record_stop` written while space remains;
   - refused at startup if the root is, or is inside, `OBSERVER_ARCHIVE_ROOT`;
   - a failed append is counted and never ends the run.
4. **Imports.**
   - `src/feegrowth/` may import `src/observation/observerConfig` (the RPC) and the DLMM SDK.
   - It imports nothing from `src/execution/`, `src/decision/fsm/`, `src/index.ts` or any signer.
   - The pure modules (`feeGrowthRecord`, `binCounters`, `accrual`) import no SDK and no filesystem.
5. **Loopback health only.** `GET /api/health` on `127.0.0.1:FEEGROWTH_PORT` (default 7763). Numbers and enum labels
   only; nothing else is served.

## 3. Record schema (`schema: 1`)

Daily UTC files `fee-growth-YYYY-MM-DD.jsonl`, append-only. Every u128 is an exact decimal string.

- **`run_start`:**
  - `venue: "meteora-dlmm"`, `pool`, `bin_step`, `decimals_x`, `decimals_y`, `range_pct`, `cadence_ms`;
  - the envelope `schema`, `run_id`, `seq`, `observed_at_ms`.
- **`sample`:**
  - `slot`, `active_bin_id`, `protocol_share_bps`, `protocol_fee_x`, `protocol_fee_y`;
  - `missing_arrays` (array indices not initialised);
  - `bins[]` of `{bin_id, amount_x, amount_y, liquidity_supply, fee_x_per_token, fee_y_per_token, lo_fee_ask,
    lo_fee_bid}`, for bins with non-zero supply or any non-zero counter;
  - `counter_decreases` (against the previous sample, per bin; expected 0);
  - `reconciliation`, per interval with the previous sample: `{lp_fraction_x, lp_fraction_y, protocol_fee_claimed}`
    or `null`.
- **`run_stop`** (reason `sigint` or `sigterm`) and **`record_stop`** (reason `free_space_below_floor`).

A missed sample loses no fees, because the counters are cumulative; it loses resolution only. A gap is a gap, never
interpolated. A bin absent from one sample is a gap for that bin.

## 4. Cadence and range

- The cadence is `FEEGROWTH_CADENCE_MS` (default 300000; at least 60000), aligned to the UTC clock.
- The range is ±`FEEGROWTH_RANGE_PCT` (default 0.10, [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] D2; at most 0.5) of the active bin at the previous sample,
  as whole `BinArray`s of 70 bins.
  - If the active bin has left the previous range, that sample is recorded with the arrays it read.
  - The next sample re-centres on the new active bin.

## 5. The standing reconciliation ([[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] acceptance note)

For each interval between two samples with no protocol-fee claim:

in-range LP fees ÷ (in-range LP fees + Δ `protocolFee`) should equal 1 − `protocol_share_bps` / 10 000.

- The fee credited to all LPs of bin b is `(supply_b >> 64) · Δ fee_per_token_b >> 64`.
- A value outside ±5% of the expected fraction is a data-quality flag. It is recorded in the sample and counted in
  `/api/health`.
- A claim (a negative Δ `protocolFee`) marks the interval `protocol_fee_claimed: true` and skips the check.

## 6. Research use (§I)

- **Accrual.** A hypothetical position with quote value `v_b` in bin b is credited, per interval,
  `share_b × LP fees_b`, where `share_b = v_b / (V_b + v_b)` and `V_b = amount_x·price_b + amount_y` from the interval's
  opening sample. Zero-supply bins credit 0.
- **Coverage.** The simulator credits only whole fee-growth intervals during which a position was open throughout.
  - Partial intervals at open and close are not credited, which is conservative.
  - They are reported as uncovered seconds.
- **Report §I.**
  - Measured fee yield in bps/day per policy, beside the break-even yield (the same loss accounting as §A–§B).
  - Per UTC day, and per 3-day sub-window counted from the sampler's first `run_start` ([[adr-033-fee-yield-measurement-route|ADR-033]]'s partition).
  - The 10th-percentile sub-window.
- **Units.** Where no fee-growth sample covers an interval, fees remain in units of V and are labelled so.
- **No Orca cross-check from recordings.** [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1 A4 limits research reads of 7762's recording to
  `observedAtMs` and `sigmaEstimate`, so [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] §4's Orca cross-check needs an extension of A4 before it can be built.

## 7. Operations

- **Build:** `npm run build:feegrowth` → `dist-feegrowth/`, its own tree. Never `dist/` or `dist-recon/`.
- **Start:** through `docs/operations/start_observation_process.ps1 -Name fee-growth` (scheduled task
  `dlmm-fee-growth`, at logon with a 60 s delay, restarting on failure). Pid file `C:\observation\fee-growth.pid`.
- **Notifier:** check `fee-growth` ([[adr-048-health-alarms-to-the-operators-discord|ADR-048]]): health reachable, `recording` on, failures not rising, newest day file under
  10 minutes old. Metadata only.
