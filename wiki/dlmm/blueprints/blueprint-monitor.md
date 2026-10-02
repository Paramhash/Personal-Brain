---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/monitor.md
bot_commit: e532796
source_sha256: f3aa5eb7d7a7fa6346bb0edfc497cf5f462e2ff31fa97bf3c538f65ec3385096
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/monitor.md` at commit `e532796`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Monitor — Read-Only GEX and Concentrated-Liquidity Display

**Domain owner:** the local operator monitor, live and replay
**Status:** authored and binding (2026-09-28, [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]). Codifies TICKET P's standing scope
(`todo/research/DRAFT_TICKET_P_GEX_And_Concentrated_Liquidity_Monitor.md`), which governed `src/monitor/` before
this file existed, and adds the venue adapter (§6).

---

## 1. Scope

This blueprint governs `src/monitor/`: a local, read-only application that displays the SOL GEX profile, spot,
pool price, walls, ZGL, the wall envelope and the [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] recommended window, live and from recorded files.

It **displays**; it does not decide. It does not own GEX construction (`gex_intelligence.md`), range planning
(`range_planning.md`), the archive (`observation_archive.md`), or any position, hedge or FSM behaviour. It calls
those domains' functions and renders their outputs. A formula that exists in a domain is never re-derived here.

---

## 2. Boundary

1. **No execution graph.** No reachable module under `src/execution/` or `src/decision/fsm/`, no `src/index.ts`,
   no signing, transaction-construction or order-placement identifier, no authenticated Binance path. Enforced by
   `__tests__/importGraph.test.ts` (P90–P95).
2. **Third-party allowlist (P94):** exactly `@meteora-ag/dlmm`, `@solana/web3.js`, `ws`, `zod`. A new package
   fails the test and needs an ADR ([[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] §2 for any `@orca-so/*`).
3. **One composition root.** `monitorMain.ts` is the only file that constructs a client or binds a socket. Every
   other module takes its reads as injected ports and is testable without a socket.
4. **Loopback only.** `MONITOR_HOST` must be a loopback address. The ready line prints the port, never an address.
5. **Configuration.** Monitor keys are listed in `KNOWN_MONITOR_KEYS` (`monitorConfig.ts`); an unknown
   `MONITOR_*` key fails startup by name, never by value. The DLMM pool and RPC come from the observer
   configuration boundary. No endpoint, credential, local path or environment value reaches the browser, a log
   line, or a fixture.
6. **Own build tree.** The monitor runs from `dist-monitor-live/` (`npm run build:monitor-live`) — never `dist/`
   (the recorder) nor `dist-recon/` (TICKET T).
7. **Never reads the archive.** `assertReplayRootIsolated` refuses a replay root at or inside
   `OBSERVER_ARCHIVE_ROOT` (`monitor_rpc_budget.md` §"On not sharing the recorder's archive").
8. **Writes only its logs — except its own frame recording ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] and Amendment 1, §8).** Either monitor may append
   its own frames to `MONITOR_RECORD_ROOT`, never at or inside `OBSERVER_ARCHIVE_ROOT`, and on DLMM never the same as
   or nested with `MONITOR_REPLAY_ROOT`.

---

## 3. Live data flow

```text
DeribitWsClient (latched snapshot) ─┐
                                    ├─► collector tick ─► buildViewModel ─► FrameHub ─► SSE /events, GET /api/frame
PoolVenue.read()  (one per tick)  ──┘      (gexEngine, rangePlanner — called, not re-implemented)
```

- **One server-side cadence** (`MONITOR_CADENCE_MS`, default 30 s). The browser never drives a venue read; a tab
  refresh opens no connection. Slow consumers drop frames, never queue them (F-025).
- **A failed tick publishes nothing** and is counted. The previous frame stays on screen under its own timestamp.
  A partial frame is never published (`gex_intelligence.md` §9).
- **The pool read's cost is measured, not assumed** — `docs/operations/monitor_rpc_budget.md`. Any change to
  what a tick reads, or a second monitor process, invalidates it until re-measured.

---

## 4. View model and labelling

- One versioned schema (`MONITOR_SCHEMA_VERSION`, `presentation.ts`), shared with the page by `import type` only.
- **The wall envelope and the recommended window are distinct fields and distinct visual regions.** One is never
  labelled as the other.
- **Unratified parameters are labelled as such** in the schema, not only in text (`deployWidthSigmaMultiple`,
  σ placeholder).
- **Wall distances are displayed, never thresholded** (`gex_intelligence.md` §6): no colour, label or warning
  keyed to them. A `CONTESTED` label is a display diagnostic and never alters the planner's input.
- Pool-quote prices share the USD strike axis on the assumption USDC ≈ USD; the frame shows both spot and pool
  price so the basis is visible.
- **Hurdle panel ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]], schema 7):** the **model** hurdle for the recommended window, at the display capital
  `MONITOR_HURDLE_CAPITAL_BASE`, labelled UNRATIFIED in the schema and on the page.
  - **No verdict.** The monitor computes no EV payload, so it shows no gate hurdle and no PASS/FAIL, and says where
    they are printed (`npm run hurdle`).
  - **Funding** is "not read" (there is no Binance feed) and is excluded from the total, with that stated.
  - **Orca:** the Orca-derived position yield is shown, and labelled as Orca's.
  - **[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] (TICKET 028):** the model's LVR and hedge rates are the EV gate's own (`rangeCostRates`: ρ̄, the pool
    σ ratio, the burst factor). The two pool factors were measured on the Meteora pool; on Orca they are applied
    unmeasured. A running monitor shows this only after a restart, which needs approval.
- **Measured σ ([[adr-047-provisional-sigma-estimator|ADR-047]], schema 8, TICKET Z):** `sigmaEstimate` — the [[adr-047-provisional-sigma-estimator|ADR-047]] chain (trailing 24 h → 6 h →
  placeholder, 300 s returns, ≥ 80% coverage, no gap over 30 min) over the monitor's own in-memory spot history.
  - **Part B ([[adr-047-provisional-sigma-estimator|ADR-047]] Active):** it sizes the window and the hurdle (`inForce: true`). The σ row reads "measured,
    [[adr-047-provisional-sigma-estimator|ADR-047]] (<link>)", or "UNRATIFIED placeholder ([[adr-047-provisional-sigma-estimator|ADR-047]] warming up)", and a "sigma source ([[adr-047-provisional-sigma-estimator|ADR-047]])" row gives the link
    and coverage.
  - **Kill switch `SIGMA_SOURCE=placeholder`:** `inForce: false`; the Part A behaviour. It is shown as "measured, not
    used" and the width and hurdle take the placeholder. Frames recorded before Part B lack `inForce` and read the same
    way.
  - The history starts empty at every start, so the placeholder shows as "warming up" for the first 6 h.
  - The arithmetic is `src/intelligence/volatility/trailingSigma.ts`, which research §H also uses.

---

## 5. Replay

- Reads `decisions-YYYY-MM-DD.jsonl` files from `MONITOR_REPLAY_ROOT`, via two GET routes that expose names only.
  A name is matched against the file pattern undecoded; refusal and read failure are one fixed 404.
- Playback runs in the browser (`ReplayController`); the server holds no playback state.
- Recorded timestamps and gaps are preserved, never interpolated. Data a record does not carry (the per-strike
  curve) is shown as not recorded, never fabricated.
- DLMM replay is bin-denominated and reads TICKET N/T decision records. **Orca replay** reads only the Orca
  monitor's own recordings (§8, [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]]); `MONITOR_REPLAY_ROOT` stays refused for the Orca venue.

---

## 6. Venue adapter ([[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]])

### 6.1 The port

The collector reads its pool through one venue-neutral port. Everything downstream consumes only this:

| Field | Meaning |
| --- | --- |
| `venue` | `'meteora-dlmm'` or `'orca-whirlpool'` |
| `priceQuotePerBase` | Pool price, quote per whole base token, decimals applied |
| `baseDecimals`, `quoteDecimals` | From the mints, never assumed |
| `grid` | `{ kind: 'bin' \| 'tick', stepLn, spacing }` — the venue's price lattice |
| `currentIndex` | Active bin id (DLMM) or `tickCurrentIndex` (Whirlpool) |
| `liquidity` | Optional profile: `{ lowerPrice, upperPrice, liquidityQuote }[]` over a bounded band; absent ≠ zero |

Grid rules, both venues: `indexToPrice(i) = p₀ · e^(i·stepLn)`; `priceToIndex` rounds **inward** for bounds that
must stay inside a constraint and **outward** for a recommended width, and always to a multiple of `spacing`.

| | Meteora DLMM | Orca Whirlpool |
| --- | --- | --- |
| `stepLn` | `ln(1 + binStep/1e4)` | `ln(1.0001)` |
| `spacing` | 1 | `tickSpacing` |
| price | `(1+binStep/1e4)^bin · 10^(dx−dy)` | `(sqrtPriceX64/2^64)^2 · 10^(dA−dB)` |
| "active" | active bin | current tick plus in-range liquidity `L` |

### 6.2 Meteora DLMM implementation

Wraps today's `DLMM.create` / `refetchStates` / `getActiveBin` read unchanged. **Parity rule:** for the same
inputs it produces the same frame numbers as before the port existed; the DLMM path is the reference.

### 6.3 Orca Whirlpool implementation

- **Read:** one `getMultipleAccounts` per tick for the Whirlpool account and the fixed tick arrays covering a
  bounded band (default ±10%) around the current tick. Tick-array addresses are PDAs
  (`["tick_array", whirlpool, startTickIndex]`); start indices are multiples of `tickSpacing · 88`.
- **Decode:** a pure module over raw bytes. It checks each account's owner program, 8-byte discriminator and
  size before reading a field. Any mismatch — wrong owner, unknown discriminator, wrong size, a tick array that
  names a different whirlpool — **fails the tick**; no field is read from an account that failed validation.
- **Dynamic tick arrays** (variable size) are decoded. Their layout was verified on 2026-09-28 against Orca's
  `dynamic_tick_array.rs` **and** two populated mainnet accounts (TICKET U fixtures): header 60 bytes, then 88 Borsh
  entries, each a tag byte plus 112 bytes when initialised; the bitmap must agree with every tag, and trailing bytes
  are refused. The main pool had 138 such arrays at capture; the ±10% band was all fixed arrays.
- **Startup checks (fail closed):** the configured pool's mints equal the expected base and quote mints, in that
  orientation, and its `tickSpacing` equals the configured value. Orientation is checked, never inferred.
- **Liquidity profile:** start from `L` at `tickCurrentIndex`; walk initialised ticks upward adding
  `liquidityNet`, downward subtracting it. Quote value per step uses the standard CL amount formulas.
- **Not read:** positions, rewards, fee-growth-derived yield. Orca's HTTP API only as §6.6 allows.

### 6.4 Process model and configuration

- One monitor process per venue, each on its own port. The Meteora process's configuration and behaviour are
  unchanged by the Orca process existing.
- Venue selection and the Orca pool, expected mints and tick spacing are `MONITOR_*` keys added to
  `KNOWN_MONITOR_KEYS` (`config_contract.md`). The Orca process does not reuse the observer's pool key.
- **One planner for both venues, unmodified.** A Whirlpool is presented to `planDeployRange` in grid indices
  `k = tick / tickSpacing` with the equivalent step `(1.0001^tickSpacing − 1)·1e4` bps, through a `BinConversion`
  built from `spacing·ln(1.0001)` (`venue/poolVenue.ts`). The planner's width rule, placement, clamp and rejections
  therefore apply unchanged and no formula of theirs is restated. A test pins the Orca σ window's price width to the
  DLMM window's within one grid step, and envelope ticks inside the walls. `minBinsPerPosition` is applied per
  tick-spacing step and the page says so.
- **Grid-index semantics.** Every `*BinId` field in a frame is a grid index; the venue index is `k × spacing`.
  In range for a Whirlpool is the venue's rule, `lowerTick ≤ tickCurrentIndex < upperTick`, computed by the page from
  ticks rather than taken from the planner's inclusive bin flag.

### 6.5 Not authorised

Orca in the observation archive, Orca in `src/backtest/research/`, any Orca HTTP call other than §6.6's, any
`@orca-so/*` dependency, and any path from the adapter to a signer or transaction. Each needs its own ADR. (Orca
replay of the monitor's own recordings is authorised by [[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]], §8.)

### 6.6 Measured pool volume ([[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] amendment, 2026-09-28)

- **One call:** `GET https://api.orca.so/v2/solana/pools/<configured pool>`, from the Orca monitor process only.
  Host and path are code constants; the pool address is the validated configured one. No key, query string, other
  route, or cross-host redirect. Built-in `fetch`/`node:https`; no new package.
- **Own cadence** (`MONITOR_ORCA_STATS_CADENCE_MS`, default 5 min, minimum 1 min), decoupled from the pool tick. A
  stats failure never fails or delays a pool tick; the stats panel shows the last value with its age, or
  "unavailable".
- **Validated** with zod to the fields displayed (24 h / 7 d / 30 d volume and fees, TVL, price, slot) and the pool
  address; anything missing or foreign is "unavailable", never defaulted.
- **Labelled** in the schema, not only the page: source `orca-api`, scope `pool`, fetched-at. "Whole-pool measured
  volume — not a position's fee income; not [[adr-033-fee-yield-measurement-route|ADR-033]] ratification." Pool fee yield = fees / TVL, shown as the pool's.
- **Display only:** not persisted, not archived, not an input to planning, EV, or research.
- Response bodies, headers and error objects never reach a log or the browser.

---

## 7. Invariants the tests hold

- Import graph: P90–P95 (§2); the adapter modules are inside the walked set.
- View-model mapping from frozen fixtures, including every planner rejection and stale state.
- Replay: UTC file boundaries, gaps, legacy records.
- Decoder: captured Whirlpool and tick-array bytes; price from `sqrtPrice` agrees with `1.0001^tickCurrentIndex`
  within one tick; the profile returns `L` at the current tick; every validation failure fails the tick.
- Grid: `priceToIndex(indexToPrice(i)) = i`; Orca bounds are multiples of `tickSpacing`.
- No test contacts a venue or a paid endpoint.

---

## 8. Orca frame recording and replay ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]])

### 8.1 What is written

- **Where:** `MONITOR_RECORD_ROOT` (Orca venue only). Refused at startup if it is, or is inside,
  `OBSERVER_ARCHIVE_ROOT`. Daily UTC files `orca-frames-YYYY-MM-DD.jsonl`, append-only, one JSON record per line.
- **One writer:** the Orca monitor process holds a lock file in the root for its lifetime; a process that finds a
  live lock refuses to record (and still displays).
- **Records** (each carries `record`, `schema`, `run_id`, `seq`, `observed_at_ms`):
  - `run_start` / `run_stop` / `record_stop` — process start, clean stop, and a recording stop with its reason code.
  - `tick` — every published frame, compact: spot, pool price, current tick, walls and ZGL with distances, causes and
    accumulation fraction, status and rejection, window / envelope / buffered envelope as grid indices and prices,
    liquidity summary (band, value, peak depth, step count), and the stats `fetched_at_ms` in force.
  - `snapshot` — every 5 minutes: the per-strike GEX curve, the liquidity profile re-bucketed to a fixed 0.1%
    price grid within the band (value per bucket), and the full pool statistics.
- **Never written:** endpoints, credentials, local paths, environment values, raw account bytes, error objects.

### 8.2 Failure and the disk floor

- **A write never affects a tick.** Failures are counted; the frame is published regardless.
- **Floor:** recording stops when free space on the record volume is below `MONITOR_RECORD_MIN_FREE_BYTES`
  (default 50 GiB, fifty times the archive's [[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]] floor), writing `record_stop` first. The display continues.
  Restart the process to resume once space is freed.
- `/api/health` reports `recording` (`on` | `off` | `stopped:<reason>`), records written, and write failures.

### 8.3 Replay

- On the Orca monitor, the replay routes list and serve `orca-frames-YYYY-MM-DD.jsonl` from `MONITOR_RECORD_ROOT`,
  with the same name-only, undecoded-pattern and single-404 rules as §5.
- Each `tick` becomes a frame labelled `orca-whirlpool`. Its strike curve, liquidity bars and full stats come from the
  latest `snapshot` at or before it, **stated with the snapshot's age**, and are omitted (shown as not available) when
  that snapshot is older than 10 minutes. Nothing is interpolated; a gap between records is a gap.
- A truncated last line (a process stopped mid-write) is skipped and counted, never parsed partially.
- **Layout:** on a wide window the GEX chart (from the snapshot) is drawn above the recorded time series; at 900 px
  or less only the time series is drawn, as for DLMM, because the fixed-height page cannot fit both legibly.

### 8.4 Readers and retention

Only this replay reads the files. They are not archive data, not [[adr-033-fee-yield-measurement-route|ADR-033]] evidence, and not research input — except
that research §H reads `observedAtMs` and `sigmaEstimate` from them, offline ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1 A4). No
automatic deletion; the operator manages retention, and the floor bounds the worst case.

### 8.5 The DLMM monitor's recording ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1, TICKET Z)

- 7761 records with the same recorder, record kinds, floor, lock and content rule, into `dlmm-frames-YYYY-MM-DD.jsonl`
  under its own `MONITOR_RECORD_ROOT` (`C:\observation\monitor-dlmm-frames\`). The run id starts `dlmm-` and
  `run_start` says `meteora-dlmm`.
- DLMM frames carry no liquidity profile, so a DLMM snapshot holds the GEX curve and `liquidity: null`.
- **Not replayed** (A2): 7761's replay still reads TICKET T decision records from `MONITOR_REPLAY_ROOT`.
- Research §H reads `observedAtMs` and `sigmaEstimate` only (A4).

---

## 9. Health notifier ([[adr-048-health-alarms-to-the-operators-discord|ADR-048]])

- **A separate process,** `src/monitor/notify/`, posts health alarms to the operator's Discord webhook. It changes
  nothing in the monitors, the recorder or TICKET T. It holds no signer, imports no execution or FSM code, and accepts
  no inbound connections.
- **Observes, read-only:**
  - the monitors' `GET /api/health`;
  - file **metadata** only (mtime, size) of the archive, TICKET T, Orca-recording and DLMM-recording day files —
    never their content;
  - the last line of `logs\health.log`;
  - free space via `statfs`;
  - whether the pids in the known pid files are alive.
- **Posts** only to `https://discord.com/api/webhooks/…`. The URL is in `C:\observation\notifier.env`
  (`NOTIFIER_DISCORD_WEBHOOK_URL`), created by the operator. It is never logged and never in a message. Redirects are
  refused.
- **Messages carry only** a fixed check name, state (ALERT / RESOLVED / HEARTBEAT), ages, counts, UTC time and a reason
  code. No URLs, paths, pids, hostnames, errors, or market or strategy data.
- **Discipline:**
  - an ALERT needs 2 consecutive failures (60 s cadence);
  - RESOLVED on recovery;
  - an unresolved alert is repeated at most hourly;
  - a daily HEARTBEAT is sent;
  - Discord 429 responses are honoured;
  - a failed post never blocks a check.
- **Never acts** on an alarm.

### 9.2 Market events and the daily summary ([[adr-049-market-events-and-daily-summary-to-discord|ADR-049]], TICKET Y)

- **Reads** each monitor's `GET /api/frame` on loopback once a tick (7761 for events and statistics, 7762 for Orca pool
  facts). It parses a validated subset: numbers and fixed enum labels, schema 7 and live mode only. Another schema is
  ignored whole. It does not import the view model.
- **Events:** status, call wall, put wall, spot's side of the ZGL, regime. A new value must be seen on 2 consecutive new
  frames. The first frame is a silent baseline. A window recentring is not an event.
- **Rate limit:** at most `NOTIFIER_MARKET_MAX_PER_HOUR` (default 6) market messages in a rolling hour. The excess is
  counted and posted as one "N more" line once room returns.
- **Daily summary** at `NOTIFIER_SUMMARY_UTC_TIME` (default 00:05Z): spot high/low/last, walls and their change counts,
  ZGL, status shares, window, the model hurdle labelled UNRATIFIED, and Orca figures labelled "whole pool, not a
  position". Coverage counts only gaps of 2 min or less.
- **Channel:** `NOTIFIER_DISCORD_MARKET_WEBHOOK_URL` if set, else the alarm webhook. Market messages have their own
  queue, so they never delay an alarm. Every message passes `safeContent`.
- **Never acts** on what it reports.

### 9.3 Additional health checks (TICKET Z, TICKET 027)

- `dlmm-recording` ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1): 7761's own frame recording, with the same rules as `orca-recording`.
- `fee-growth` ([[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]], `fee_growth.md` §7):
  - the sampler's `/api/health` on 7763 is reachable;
  - `recording` is `on`;
  - `sampleFailures` is not rising;
  - the newest `fee-growth-*.jsonl` is under 10 minutes old.

  Metadata only.
