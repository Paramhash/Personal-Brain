---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-045
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/045-orca-monitor-records-its-own-frames-for-replay.md
bot_commit: ab766fb
source_sha256: 2db2d662ea1b09b710c5a7a10ea7ada9c68049c036d327f98f67870d58111d54
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/045-orca-monitor-records-its-own-frames-for-replay.md` at commit `ab766fb`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] — The Orca Monitor May Record Its Own Frames, to Its Own Root, for Its Own Replay

- **Date:** 2026-09-28
- **Status:** **Active. Decided by the dispatcher 2026-09-28** ("Option 2": record the Orca monitor's frames so they
  can be replayed; the alternative, replaying Meteora DLMM decision records on 7762, was declined).
- **Amends:** [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] §5, which listed "Orca replay" and "recording Orca" as not authorised — **for the Orca monitor's
  own frame recording and replay only**. Recording Orca into the observation archive, and Orca in the research
  simulator, remain unauthorised.
- **Owns:** `docs/architect/monitor.md` §8; root `src/monitor/record/`.

## Context

The Orca monitor (TICKET U, port 7762) displays live state only. Replay on 7761 works because TICKET N/T recon
processes record decision records; nothing records Orca, so an Orca replay has nothing to play. The monitor itself was
designed to write nothing but its two log files (`monitor.md` §2, `monitor_operator_note.md`), and [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] §5
excluded Orca replay and Orca recording.

Two constraints shape how a recording may be added:

1. **It shares `C:` with the irreplaceable archive run** ([[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]]). The archive halts at a 1 GiB free-space floor; any
   new writer on the volume must stop long before that point, so it can never be the cause of the archive halting.
2. **Frames are large.** A live Orca frame is ~146 KB (615 liquidity steps plus the strike curve); recording every
   30 s tick in full would be ~420 MB/day. Most of that is the liquidity profile and GEX curve, which change slowly.

## Decision

1. **The Orca monitor process may record the frames it publishes**, append-only, to its own root
   (`MONITOR_RECORD_ROOT`) as daily UTC files `orca-frames-YYYY-MM-DD.jsonl`. **One writer:** only the 7762 process;
   a second process finding the root in use refuses to record.
2. **Two record kinds, to bound size:**
   - a compact **tick** record for every published frame — time, spot, pool price, current tick, walls, ZGL, their
     distances and causes, status and rejection, window / envelope / buffered envelope (grid indices and prices),
     liquidity summary (band, value, peak depth), and the latest pool statistics' identity (fetch time);
   - a **snapshot** record every 5 minutes — the per-strike GEX curve, the liquidity profile (re-bucketed to a fixed
     0.1% price grid within the band), and the full pool statistics.
   Records carry numbers, enum labels, public addresses and timestamps only — never an endpoint, credential, local
   path or environment value.
3. **Replay reads only this root.** On the Orca monitor, replay lists and plays `orca-frames-*` files. A replayed
   frame is labelled `orca-whirlpool`; its curve and liquidity come from the latest snapshot at or before it, shown
   with that snapshot's age, and are **not shown at all** if the snapshot is older than 10 minutes. Nothing is
   interpolated; gaps stay gaps. `MONITOR_REPLAY_ROOT` stays refused for the Orca venue (it names DLMM decision
   records).
4. **Disk floor, above the archive's.** Recording stops — the live display does not — when free space on the record
   volume falls below `MONITOR_RECORD_MIN_FREE_BYTES`, default **50 GiB** (fifty times the archive's floor). The stop is
   written as a `record_stop` record while space remains, logged by reason, and shown in `/api/health`.
5. **Recording never costs the display.** A write failure or a floor stop never fails, delays or alters a tick; it is
   counted and reported. The root is refused at startup if it is, or is inside, `OBSERVER_ARCHIVE_ROOT`.
6. **Readers.** Only the monitor's replay reads these files. They are **not** archive data, **not** [[adr-033-fee-yield-measurement-route|ADR-033]] evidence,
   and **not** research-simulator input; the measured pool-volume series they contain (one per stats fetch) stays
   display-only until a separate decision says otherwise.
7. **No automatic deletion.** Retention is the operator's; the floor bounds the worst case.

## Consequences

- Orca history accumulates from the moment recording starts; there is none before it.
- The GEX curve is recorded for the first time (every 5 minutes), so Orca replay can show the curve — something the
  DLMM replay cannot, because recon records never stored it.
- **Recorded cost — a second writer on the archive's volume.** Bounded by the 50 GiB floor and an estimated
  ~10–15 MB/day (measured at implementation). The archive's own floor and halt path are unchanged.
- **Recorded cost — the monitor is no longer write-free.** `monitor.md` §2 and the operator note change accordingly;
  stopping 7762 with `Stop-Process` can now cut a record mid-line, which the reader must tolerate (the last partial
  line of a file is skipped and counted, as the archive reader does).
- The Meteora DLMM monitor (7761) is unaffected: it records nothing, and its replay still reads TICKET T records.

## Reversed by

A decision to move Orca recording into the observation archive (its own ADR under `observation_archive.md`); disk
pressure making the 50 GiB floor bind; or evidence that recording affects tick latency.

## Implementation note — 2026-09-28 (TICKET V)

- **Size, measured** (replacing the ~10–15 MB/day estimate above): 2.7 KB per tick record and 56 KB per 5-minute
  snapshot on a live frame — **~23.3 MB/day**, ~8.5 GB/year. The snapshot is larger than estimated because the full
  Deribit strike curve and ~250 re-bucketed liquidity buckets are kept. Against 1.2 TB free and the 50 GiB floor this
  changes nothing in the decision.
- **Cost to the tick, measured:** `record()` median 0.28 ms, p95 2.4 ms, max 3.8 ms, after publication, on a 30 s
  cadence.
- Recording on 7762 began 2026-09-28 into `C:\observation\monitor-orca-frames\`.

## Amendment 1 — 2026-09-30: the Meteora DLMM monitor records its frames too; research may read σ from both

- **Status:** **Active. Decided by the dispatcher 2026-09-30**, for TICKET Z ([[adr-047-provisional-sigma-estimator|ADR-047]]): the measured σ goes into "both
  7761 and 7762 live frames and Orca and Meteora recording". A4 is tied to [[adr-047-provisional-sigma-estimator|ADR-047]]'s review; see "Reversed by".
- **Amends:**
  - Consequences, last bullet ("7761 is unaffected: it records nothing");
  - Decision §6 ("not research-simulator input") — for one field only, see A4.

### Context

[[adr-047-provisional-sigma-estimator|ADR-047]] proposes replacing the 1.4e-4/s σ placeholder with a trailing 24 h estimator, and its 2026-10-18 review needs
out-of-sample evidence: σ as the live chain computed it, compared against σ realized afterwards.
- TICKET Z Part A computes that σ in both monitors and publishes it in the frame (`sigmaEstimate`). The frame is not
  kept.
- The Orca recording keeps its frames, but [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] §6 bars them from research.
- 7761 records nothing: its replay reads TICKET T decision records, which `dist-recon/` writes and which are not being
  rebuilt.

Without this amendment, the only record of the live σ chain would be one venue's, and research could not read it.

### Decision

- **A1 — 7761 may record its own frames under the same rules as 7762.**
  - Decision §1–§5 and §7 apply unchanged, with `dlmm-frames-YYYY-MM-DD.jsonl` in place of `orca-frames-*`.
  - Same record kinds: a compact tick record every frame, and a 5-minute snapshot carrying the GEX curve and the pool's
    liquidity profile, re-bucketed to the same 0.1% price grid.
  - Same content rule: numbers, enum labels, public addresses and timestamps only.
  - Same 50 GiB floor and archive-root refusal, and a write failure never affects a tick.
  - One writer per root, enforced by the existing `recording.lock`. The default root is
    `C:\observation\monitor-dlmm-frames\`, separate from the Orca root.
  - `MONITOR_RECORD_ROOT` and `MONITOR_RECORD_MIN_FREE_BYTES` become valid for the DLMM venue; the `MONITOR_ORCA_*` keys
    stay Orca-only.
- **A2 — 7761 replay is unchanged.** It still reads TICKET T decision records through `MONITOR_REPLAY_ROOT`. Replaying
  `dlmm-frames-*` is **not** authorised by this amendment; it needs its own decision if wanted.
- **A3 — Both recordings carry `sigmaEstimate`**, TICKET Z Part A: σ per second, the chain link used, coverage, reason
  code and ratio to the placeholder.
- **A4 — One research read, bounded.**
  - The offline research σ forecast check (`research/sigmaForecast.ts`, report §H) may read `observedAtMs` and
    `sigmaEstimate` — **those fields only** — from both recordings. It scores them against σ realized from the
    observation archive.
  - Nothing else in these files becomes research, simulator or [[adr-033-fee-yield-measurement-route|ADR-033]] input.
  - The read is offline, by the research CLI; no runtime process reads them apart from each monitor's own replay (Orca
    only).
- **A5 — The notifier watches it.** [[adr-048-health-alarms-to-the-operators-discord|ADR-048]]'s check list gains `dlmm-recording`, the counterpart of `orca-recording`,
  with the same thresholds and a `NOTIFIER_DLMM_RECORD_ROOT` key. Metadata only, as [[adr-048-health-alarms-to-the-operators-discord|ADR-048]] requires.

### Consequences

- **A third writer on the archive's volume.** Measured at about 23–26 MB/day for Orca, so both recordings total about
  50 MB/day, about 1 GB over the 21-day run. That is against 1.2 TB free and a 50 GiB floor per recorder. The archive's
  floor and halt path are unchanged.
- **7761 is no longer write-free.** `monitor.md` §2/§8 and the operator note change at implementation.
  - Stopping 7761 with `Stop-Process` can cut a record mid-line; the reader already skips and counts a partial last
    line.
- DLMM frame history exists only from the moment recording starts. Nothing before it is reconstructed.
- The GEX curve is recorded on the DLMM side for the first time, as a by-product of the 5-minute snapshot. It stays
  display-only under A2 and A4.

### Reversed by

- [[adr-047-provisional-sigma-estimator|ADR-047]] being rejected at its review: recording on 7761 may then stop, and A4 lapses.
- Disk pressure making the floor bind.
- Evidence that recording affects 7761's tick latency.
