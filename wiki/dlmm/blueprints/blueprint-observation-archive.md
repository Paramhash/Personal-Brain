---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/observation_archive.md
bot_commit: 3f1eec9
source_sha256: f5b3677d17897bbbbba2df36fdd24e2249627017920bda09f3e3d7afadd19252
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/observation_archive.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Observation Archive

**Domain owner:** Observation
**Status:** authored and binding
This file fixes the ownership, isolation, record schema, integrity rules, operational envelope,
retention policy, and non-goals for a durable observation series recorded for later calibration.

---

## 1. Scope

This blueprint governs:

- a durable, append-only series of observations recorded from read-only venue reads
- the record schema of that series and its versioning
- gap and integrity semantics for a series recorded over weeks
- the isolation guarantees that keep the recorder from affecting the trading process
- the operational envelope of a multi-week recording run
- retention of raw samples relative to any calibration derived from them

It does not make trading decisions, submit venue actions, hold a signer, or own restart state.

**Why this domain exists.** Four EV inputs are labelled `UNRATIFIED` in
`src/decision/ev/evCalculator.ts` — `PLACEHOLDER_FEE_YIELD_PER_HORIZON`,
`PLACEHOLDER_SIGMA_1S_STDDEV`, `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER` and
`PLACEHOLDER_DEPLOY_LAMPORTS`. None can be calibrated retrospectively, because the observations
required do not exist and cannot be manufactured after the fact. Observation quality is a function
of wall-clock time, which is what makes the recording capability urgent while the calibration
itself is not yet decidable.

---

## 2. Ownership — why this is not the State domain

`state_store.md` §2 fixes the State domain's contents as `PendingWithdrawalResumePoint`, the active
DLMM position state and the Binance hedge state, and states they "are not optional caches. They are
the minimum restart-recovery facts required to reconcile an interrupted process against live
venues." An observation series is none of those things, and folding it in would break three of that
blueprint's own rules rather than extend them.

| `state_store.md` rule | Why the archive does not fit it |
| --- | --- |
| §2 — contents are restart-recovery facts | The archive is never consulted to recover anything. A run that loses it loses data, not correctness. |
| §3 — stored state must be reconciled against live venues at boot before operational work resumes | There is nothing to reconcile. History is not a claim about current venue state, so there is no mismatch for the venue to win. |
| §5 — durability is snapshot replacement, via write-then-rename or an equivalent single commit | The archive is **append-only and unbounded**. Rewriting a multi-gigabyte series to add one record is not a durability strategy. |
| §6 — the State domain is the only module permitted to own durable restart state | Correct, and unaffected: the archive holds no restart state, so this exclusivity is preserved, not weakened. |

The decisive point is §3. Making the archive part of State would place a growing analysis dataset
inside the boot path of a trading process, where its absence or corruption could delay or block a
recovery that has no logical dependence on it. `state_store.md` §2's exclusion of caches is
deliberate and is left intact.

## 2a. Ownership — why this is not the Observability domain

`observability_contract.md` §1 scopes that domain to "structured application logging, execution and
reconciliation metrics, withdrawal-loop latency measurements, replay timing and production telemetry
emission" — telemetry emitted *by a running bot*. Three mismatches make it the wrong owner:

1. **Lifetime and consumer.** Telemetry serves an operator watching a live process. The archive
   serves an analyst weeks later. §4's requirement that "the same event schema must be usable for
   offline replay and production operation" is a constraint on the bot's event taxonomy, which has
   no bearing on a calibration series.
2. **Schema driver.** §2 requires records to "preserve the root event categories already declared by
   `OrchestratorEvent`: boot, tick, skipped tick, withdrawal, hedge, swap, deploy, and error." The
   archive's schema is driven by the constants it exists to calibrate, not by the bot's states.
3. **The recorder runs when the bot does not.** Telemetry presupposes a trading process to emit it.
   The recorder's whole purpose is to observe a pool the bot is not trading, before it trades it.

`observability_contract.md` §4's downstream-only rule is nonetheless inherited in spirit and
strengthened in §4 below: the archive may not write into any other domain either.

## 2b. The decision

A new domain, **Observation**, owns the archive. Implementation root **`src/observation/`**.
Recorded as [[adr-032-observation-archive-ownership-and-isolation|ADR-032]], which is also the authority `system_index.md` §1 requires before a new source
root may exist.

---

## 3. Isolation — the recorder is a separate process

The recorder is a **separate process with its own configuration**, not a mode of the trading binary
and not a thread inside it. This is a boundary, not a packaging preference.

**Required guarantees:**

1. **No signer, ever.** The recorder's environment must not contain `SOLANA_SIGNER_SECRET_KEY`. The
   absence of the key is the guarantee; a flag that could be flipped is not.
2. **No execution imports.** The recorder must not import `src/execution/`, construct a venue SDK
   client capable of writing, or hold Binance credentials. This is testable the way this repository
   already tests offline isolation — enumerate `require.cache` and assert zero `src/execution/`
   modules in the recorder's runtime graph.
3. **Separate configuration keys.** The recorder reads `OBSERVER_*` keys — at minimum
   `OBSERVER_POOL_ADDRESS` and `OBSERVER_SOLANA_RPC_URL`. It must not read `DLMM_POOL_ADDRESS`,
   `SOLANA_RPC_URL`, or any other key the trading binary reads. Distinct names are what prevent a
   mainnet observation target from reaching the trading binary's execution wiring by sharing a
   variable with it.
4. **Separate filesystem from the state store.** The archive must not share a partition with the
   State domain's durable files. `state_store.md` §5 requires write-then-rename atomicity, which a
   full partition defeats; an archive that grows unboundedly is exactly the thing that fills one.
   This is a binding operational requirement, not advice.

   > **Amended 2026-09-26 by [[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]].** The permanent production host is a single-volume Windows 11
   > machine, so this rule as written is unsatisfiable there rather than merely unmet. On a
   > single-volume host the archive **may** share a filesystem with the State domain, **only** where
   > the recorder enforces an absolute free-space floor on the archive volume —
   > `OBSERVER_ARCHIVE_MIN_FREE_BYTES`, default 1 GiB — below which it **halts the run** rather than
   > appending. A breach is never a skipped append: §7 rule 2 forbids a silently absent record, so the
   > floor is checked before any append and ends the run with the `RUN_STOP` that accounts for the
   > gap. Where two volumes exist, the original rule stands and is preferred — the substitution is
   > weaker, because a floor holds only while the code is correct and a partition held regardless.
5. **No shared handles or paths.** The trading process never opens an archive path. The recorder
   never opens a state-store path.
6. **Failure is local.** Recorder crash, disk pressure, RPC failure, throttling and restart must
   have no path to the trading process. A separate process with a separate partition and disjoint
   configuration achieves this structurally, which is why that shape is required rather than
   recommended.

   > **Qualified 2026-09-26 by [[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]].** On the single-volume production host the word
   > *structurally* no longer holds for disk pressure specifically. The separate process and disjoint
   > configuration still isolate crash, RPC failure, throttling and restart structurally; disk
   > pressure is isolated by the rule 4 floor, which is a control rather than a structure. The
   > requirement is unchanged — only the claim about how it is achieved is narrowed.

**What the trading process may read from the archive: nothing, ever, at any time.** A measured
quantity reaches the bot only as a ratified constant in `src/config/strategy.config.ts`, introduced
by an ADR. The archive is not a data source for the running system. This single rule is what keeps
the archive from becoming a live EV input by increment.

---

## 4. Data-flow position

The archive is a **sibling observer**. It is downstream of nothing in the trading pipeline and
upstream of nothing:

```text
marketdata → state → intelligence → decision → risk → execution → observability

        [ observation ]        ← reads venues read-only; writes only its own files
```

Binding consequences:

- The archive **writes to no other domain**, including observability.
- No other domain reads the archive at runtime.
- The archive imports **no** trading-pipeline module that could change under it. In particular it
  must not import `src/decision/`.

### 4a. The canonical active-bin price, without importing the decision domain

`ev_policy.md` §5a fixes the pool price in closed form:

```text
quotePerWholeBase = (1 + binStep / 10_000) ^ activeBinId * 10 ^ (baseDecimals - quoteDecimals)
```

The recorder must use **this formula**, and must not import `activeBinPriceQuotePerBase` from
`src/decision/ev/evCalculator.ts`, because §4 forbids coupling the archive to a module under active
revision.

Should a future implementation prefer shared code to a restated formula, the helper is **hoisted to
a shared module** — `src/types/` or a module local to `src/observation/` — and both callers import
the shared copy. The archive never imports `src/decision/`. That hoist is implementation-ticket
scope and is not performed by this design ticket.

---

## 5. Record schema

Adopted from `todo/research/DRAFT_TICKET_C_Fee_Observer_Schema_And_Run_Spec.md`, with one field
promoted to an explicit exception in §5e. **Amended 2026-09-26** under the authorisation of the
`Observation Recorder Implementation` ticket, which asked the Implementer to apply or reject the
`bin_samples` split: it is **applied**, because liquidity distribution is a slow variable and price is
not, and sampling the distribution at the price cadence multiplies the run's storage by an order of
magnitude for no analytical gain. Five append-only NDJSON streams, one UTC file per stream per day:

```text
pool_samples/YYYY-MM-DD.jsonl        periodic, 30 s — the primary scalar series
bin_samples/YYYY-MM-DD.jsonl         periodic, 5 min — liquidity distribution
cost_observations/YYYY-MM-DD.jsonl   event-driven, real transactions only
spot_samples/YYYY-MM-DD.jsonl        periodic, off-chain price
run_events/YYYY-MM-DD.jsonl          process lifecycle
```

**`schema_version` is carried per record, not per file.** A field added mid-run must leave earlier
records unambiguous, and a file-level version cannot express a version change inside a UTC day.

Schema version **1** includes `fee_observation` as a nullable field. Populating it later is
therefore **not** a version change, which is what satisfies the requirement that the archive admit
fee-accrual data from the first record without migration.

### 5a. `pool_samples` — the primary periodic record

| Field | Type | Purpose |
| --- | --- | --- |
| `schema_version` | int | per record |
| `observer_run_id` | string | one per process start; makes restarts visible in the data |
| `seq` | int | monotonic within a run; a missing `seq` is a detectable hole |
| `cluster` | string | guards against a Devnet record contaminating a mainnet set |
| `pool` | string | `lbPair` address |
| `intended_at_ms` | int | scheduled sample time |
| `observed_at_ms` | int | when the read actually answered |
| `sample_latency_ms` | int | separates a slow endpoint from a slow chain |
| `sample_status` | enum | `OK` \| `RPC_ERROR` \| `RATE_LIMITED` \| `TIMEOUT` \| `DECODE_ERROR` \| `SKIPPED_OVERRUN` |
| `slot` | int | the chain's own clock; authoritative ordering for on-chain state |
| `block_time_ms` | int \| null | chain time, so wall-clock drift is detectable against it |
| `active_bin_id` | int | σ, range drift, redeploy cadence |
| `bin_step_bps` | int | recorded every sample; configuration can change mid-run |
| `active_bin_price_quote_per_base` | number \| null | derived by §4a; see the §5e exception |
| `base_mint`, `quote_mint` | string | identity; detects a pool swapped under a run |
| `base_decimals`, `quote_decimals` | int | scale, and §4a inputs |
| `pool_base_fee_bps` | number | the fee tier in force |
| `pool_variable_fee_bps` | number \| null | the dynamic component moves with volatility; a blended figure cannot be decomposed later |
| `total_base_reserve`, `total_quote_reserve` | number | pool size, for liquidity share |
| `fee_observation` | object \| null | §5b; present as a field from schema version 1 |

The bin window moved to its own stream in the 2026-09-26 amendment — see §5a-bis.

### 5a-bis. `bin_samples` — the liquidity distribution, on its own slower cadence

| Field | Type | Purpose |
| --- | --- | --- |
| `schema_version`, `observer_run_id` | | as §5a |
| `seq` | int | **its own** monotonic counter, independent of `pool_samples` |
| `intended_at_ms`, `observed_at_ms`, `sample_latency_ms` | int | as §5a |
| `sample_status` | enum | the same set as §5a |
| `slot`, `block_time_ms` | int / int \| null | as §5a |
| `active_bin_id` | int | repeated here deliberately — it anchors the window, so a bin sample must be interpretable without a join |
| `bin_window_radius` | int | bins requested either side of active |
| `bin_window_lower`, `bin_window_upper` | int | the actual bounds captured, which may differ at bin-array edges |
| `bins[]` | array | `{bin_id, base_amount, quote_amount, liquidity_supply}` |
| `bins_truncated` | bool | true when liquidity existed outside the captured window |

`bins[]` is required rather than pool-wide totals alone: the concentration multiplier is a statement
about how liquidity is *distributed across bins*, and no aggregate can reconstruct it.

Both streams carry `slot` and timestamps, so joining distribution to price is the ordinary
nearest-sample join. The radius is recorded per record, so **changing it mid-run is legible to a
reader rather than corrupting** — which is what lets the recorder start before the deployment range
is decided.

### 5b. `fee_observation` — route-agnostic, and cumulative

| Field | Type | Notes |
| --- | --- | --- |
| `route` | enum | `RESERVE_DELTA` \| `SWAP_PARSE` \| `POSITION_ACCRUAL` |
| `position_pubkey` | string \| null | non-null only under `POSITION_ACCRUAL` |
| `fee_base_cumulative` | number | since position open, or since run start for inference routes |
| `fee_quote_cumulative` | number | as above |
| `position_liquidity_share` | number \| null | directly observable only under `POSITION_ACCRUAL` |
| `fee_base_delta`, `fee_quote_delta` | number \| null | convenience only; never the system of record |
| `delta_spans_gap` | bool | true when the previous `OK` sample was not `seq - 1` |

**Fee counters are cumulative and never interval-only.** This is binding, and it is the schema's
most consequential rule. Interval deltas lose the fees accrued during any missed sample
permanently, and the loss is invisible in the output. Cumulative counters remain differenceable
across a gap, and `delta_spans_gap` marks where that happened so an analyst may include or exclude
the interval deliberately.

The object's shape must not force a choice among the three routes. Route selection is the paired
fee-yield ADR's decision (§9).

### 5c. `cost_observations` — event-driven, `bin_count` mandatory

Written only when a real transaction against the pool is observed. This series calibrates
`PLACEHOLDER_DEPLOY_LAMPORTS`.

Required: `schema_version`, `observer_run_id`, `slot`, `block_time_ms`, `signature`, `instruction`,
`units_consumed`, `lamports_fee`, `tx_version`, `serialized_bytes`, and **`bin_count`**.

`bin_count` is mandatory because deploy compute is a function of deployment width, not a scalar.
Measured on the 2026-09-25 soak against the three runs before it:

| | soak12–soak14 | soak15 |
| --- | --- | --- |
| bins | 22 | 47 |
| units consumed | 212,181 | 367,740 |

The series must therefore support fitting `cost ≈ f(bin_count)`. A single observed lamport figure is
the wrong *shape* for this cost, and `212,181` must not be carried anywhere as a regression
threshold.

### 5d. `spot_samples` — and why σ is not sourced from RPC

Required: `schema_version`, `observer_run_id`, `seq`, `intended_at_ms`, `observed_at_ms`,
`sample_status`, `spot`, `spot_source`, and the existing staleness latch as `spot_stale`.

`PLACEHOLDER_SIGMA_1S_STDDEV` is a **per-second** standard deviation, and `realizedVol1m_t` is set
`null` at `src/index.ts:405` and never computed, so σ always falls back to that constant.

Polling Solana RPC once per second for three weeks is not viable and would be throttled long before
it was informative. Sampling at the pool cadence and scaling by `√t` assumes IID increments — which
is precisely what question 2 in §6 exists to test, so the scaling cannot be used to validate
itself.

**Binding rule:** spot is taken from the Deribit source already owned by
`data_ingestion_flow.md`, at its native push cadence or an explicitly documented downsample. The
pool is sampled at the slower cadence in §8. The pair yields the basis distribution, which is what
establishes whether off-chain σ is a legitimate proxy for pool σ at all.

### 5e. Derived values — the rule and its one exception

**The archive stores observations and statuses, never estimator outputs.** No
`estimator_shadow` field exists, and none may be added. Computing one at write time would require
importing `src/decision/ev/`, inverting §4's direction and coupling an irreplaceable dataset to a
module under revision. The residual series remains obtainable and safer: every estimator input is
stored, so the shadow is computed at analysis time from preserved inputs.

**The single permitted derived field is `active_bin_price_quote_per_base`**, admitted because it is
a pure function of four fields stored in the same record — `bin_step_bps`, `active_bin_id`,
`base_decimals`, `quote_decimals` — by a closed-form expression fixed in `ev_policy.md` §5a with no
free parameters. It therefore cannot silently encode an estimator change, and it is independently
re-derivable by any reader. It is stored for legibility of the primary series, and a reader who
distrusts it must recompute it from the four inputs rather than trust the field.

No further derived field may be added on this precedent without an ADR.

---

## 6. Required observation questions

The design is accepted only if the resulting series can answer all six after a multi-week run.
These are stated before collection because recording the wrong fields for weeks is detectable no
other way.

1. Realized fee yield per unit of in-range liquidity per day, with its variation across sub-windows.
2. Volatility of price at 1 s, 1 m and 1 h — and whether `√t` scaling holds between them.
3. The fraction of wall-clock time the active bin remained inside a range of width *W* around its
   deploy-time position, across a range of *W*.
4. Deployment cost as a function of `bin_count`, not as one scalar.
5. The distribution of basis between pool price and Deribit spot.
6. **The coverage ratio for every published result** — `OK` samples over intended samples, for the
   window that result describes.

Question 6 is what makes 1–5 admissible. A yield quoted without its coverage ratio is not a result,
and this blueprint treats it as one that may not be published.

### 6a. The observation target

The target is **the mainnet pool and real bin step the strategy intends to trade**.

The currently configured Devnet pool `3q8CRDUkH15QrNLoa9NNUiA6HShs9ueYc9XpbqArLS3A` is **excluded as
a calibration target** on three independent grounds, recorded so the question is not reopened:

1. **No volume, therefore no fees.** Five transactions in total as of 2026-09-25, dated
   2026-03-04, 04-10, 04-12 and two on 09-19. Fee yield there is structurally zero.
2. **Distorted price scale.** Its active-bin price is approximately 6,937,303 quote units per SOL
   against a real market near 120; [[adr-023-range-planner-devnet-scaling-and-containment|ADR-023]] exists to cope with that distortion. Any
   yield-per-notional figure derived from it is meaningless.
3. **Unrepresentative geometry.** `binStep: 80` is 0.8% per bin. Fee yield per unit of in-range
   liquidity is a strong function of bin width, so a constant measured at 80 bps does not transfer
   to the intended pool.

---

## 7. Integrity and gap semantics

`data_ingestion_flow.md` §4 forbids silently interpolating, extrapolating or republishing stale data
with a fresh timestamp, and latches staleness rather than hiding it. The archive inherits that
discipline and applies it to history. A recorder that drops out for an hour, and later has σ
computed across the gap as though the samples were contiguous, produces a wrong number silently and
with no symptom.

The rules are binding:

1. **Intended schedule time is recorded separately from actual observation time** —
   `intended_at_ms` and `observed_at_ms`.
2. **Every intended sample produces a record.** A failed, throttled or overrun sample is written
   with its `sample_status` and whatever fields were obtained. A missed sample is never silently
   absent. Absence of a record means the recorder was not running, and `run_events` says so.
3. **No interpolation and no backfilling across a gap**, ever, for any series.
4. **Volatility and return series may be computed only between records with consecutive `seq` and
   `sample_status: OK`.** Non-consecutive pairs are excluded, not bridged.
5. **Fee differences are cumulative-derived and gap-marked** — §5b, `delta_spans_gap`.
6. **Writes are append-only with `fsync` per record.** The writer never rewrites a record.
7. **A torn final line is the reader's responsibility:** discard it and truncate to the last valid
   newline. A partially written final record is an expected outcome of process death, not
   corruption.
8. **Restarts are visible in the dataset**, through `run_events` and a new `observer_run_id`.
9. **Every published result carries its coverage ratio** — §6 question 6.
10. **Each periodic stream carries its own `seq` and its own intended schedule, and rules 1–9 apply to
    each independently.** A `bin_samples` gap does not make the `pool_samples` series gapped, and
    coverage ratios are reported per stream.

---

## 8. Operational envelope

| Series | Cadence | Approx. 21-day count |
| --- | --- | --- |
| `pool_samples` | 30 s | ~60,480 |
| `bin_samples` | 5 min | ~6,048 |
| `spot_samples` | 1 s, from the existing Deribit source | ~1.8M |
| `cost_observations` | event-driven | pool-dependent |

- **Storage is a function of the configured radius, not a constant.** The figure this section
  previously carried silently encoded a ±34-bin assumption, which did not survive contact with a
  4 bps pool.

  ```text
  bytes  ≈  days × 86400 × ( 550/30  +  150/1  +  2 × radius × 110/300 )
                              scalars    spot        bin window
  ```

  At the recommended ±250-bin radius that is ~590 MB for 21 days and ~2.55 GB for 90 days,
  uncompressed. The per-record sizes are **estimates and must be re-measured in the first hour of
  the first run**, and the projection restated.

  **Provision 20 GB, alarm at 80%, never auto-delete.** Far above the computed need, because [[adr-033-fee-yield-measurement-route|ADR-033]]
  fixes 21 days as a floor and prescribes a longer window if its stability criterion fails; because
  the radius is downstream of a deployment-range decision not yet taken; and because a full partition
  is the one failure that destroys the dataset outright while also defeating `state_store.md` §5's
  write-then-rename if the two ever share a filesystem (§3 rule 4). Per §3 rule 4 that partition is
  not the State domain's.

- **Compression:** closed daily files are gzipped. Lossless, so §9's indefinite retention of raw
  samples is satisfied, and repetitive numeric NDJSON compresses roughly 6×. The current day's file
  stays uncompressed for appending.
- **RPC:** two calls per 30 s is roughly 0.07 calls/second. Modest, but the documented failure mode
  is real — the 2026-09-17 soak recorded 26 HTTP 429s against Devnet in 44 seconds and soak15
  recorded 9 retry lines in 37 seconds. **Sustained mainnet monitoring assumes a paid endpoint.**
  Note that `@solana/web3.js` emits its 429 retry lines through an internal logger that writes
  *outside* the structured sink; that path must not swallow a sample without writing a
  `RATE_LIMITED` record.
- **Supervision:** `launchd` on macOS or `systemd` on Linux, restart-on-exit. Every restart writes
  `RUN_START` with a reason.
- **Clock:** NTP required on the host. Both wall-clock and `block_time_ms` are recorded so drift is
  detectable rather than assumed absent.
- **Health criteria:** a running recorder that writes nothing but `RATE_LIMITED` is the failure mode
  uptime does not catch. Health is therefore defined as the newest `pool_samples` record being
  within two cadences of now **and** the count of non-`OK` statuses in the last hour being below a
  stated threshold.
- **Liveness check:** one command returning the newest `pool_samples` record's `intended_at_ms` and
  the non-`OK` count in the last hour.
- **Halt and escalation:** sustained rate limiting above the stated threshold is an **escalation**,
  not a restart — restarting into the same throttle produces gapped data that looks like a running
  recorder. Disk above the 80% alarm is an escalation before it is a deletion.

### 8a. Dual-LAN does not apply

`config_contract.md` §5's two-NIC requirement exists to separate execution traffic from intelligence
traffic. **The recorder has one read-only traffic class and performs no execution traffic, so
Dual-LAN separation is out of scope for it** and `assertNicBindings` is not a gate on this workload.

Stated explicitly because the next reader will otherwise apply it by analogy and reintroduce a
solved problem. It also means the DHCP-lease and manual-alias durability gap that blocks promoting
the *trading* binary does not block the recorder — sidestepped, not solved.

### 8b. Host verification does not transfer between hosts

Every network fact established on 2026-09-25 — `192.168.10.152` sole on `en5`, `192.168.10.57` sole
on `en0`, the duplicate `.56` alias absent — was measured on the **development Mac**. The production
NUC has its own interfaces and its own configuration, and nothing in this repository has observed
them. **Interfaces and configuration must be verified independently on the NUC** before a multi-week
run. Development-host observations must not be carried across.

> **Corrected 2026-09-26 ([[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]]).** There is no NUC, and the development Mac is no longer the
> development host. There is one host: Windows 11, `DESKTOP-PQP9JPL` — see
> `docs/operations/production_host.md`. With a single host this section has no second machine to
> guard against, but the operative conclusion is unchanged and now stronger: **no network fact in this
> repository was measured on the machine that will run the system.** The `en5`/`en0` observations
> describe macOS interfaces that do not exist here; the live interfaces are `Ethernet 2` and
> `Ethernet 3`, both on the same Realtek 2.5GbE controller family. Verification is still outstanding,
> and the same-family pairing makes the 2026-09-19 one-physical-path fault easier to create than it
> was on the Mac.

---

## 9. Retention

- **Raw samples are retained indefinitely** until an ADR explicitly authorizes their deletion. A
  three-week window cannot be re-run, and a derived calibration is not a substitute for the
  observations behind it.
- **Every derived calibration cites its provenance:** the `observer_run_id` set, the UTC date range,
  and the coverage ratio over that range.
- **A derived constant that cannot be traced to retained raw samples is not ratifiable.** This is
  the rule that makes §6 question 6 enforceable rather than advisory.

---

## 10. The unresolved fee-measurement decision

This blueprint makes the archive **route-ready** and does not choose a route. Route selection
belongs to the paired fee-yield ADR ticket.

The three routes the schema must admit without change:

1. **Reserve-delta inference** — read-only, no capital; conflates swaps with LP adds and removes,
   leaving an attribution error that cannot be bounded from the data itself.
2. **Swap-transaction parsing** — read-only, no capital; measures *pool* volume correctly, which is
   the wrong quantity by one step, since the gate needs what a position in a given range earns. It
   therefore requires a liquidity-share model.
3. **Direct accrual on a small real mainnet position** — measures the target quantity directly, in
   one observed number, with no decoding and no share model; **requires mainnet execution and
   capital at risk.**

Binding constraints until a route is chosen:

- **What is measured until then: nothing about fee yield.** The archive records the pool state
  around which fees would accrue, and `fee_observation` stays `null`.
- **Any route introducing an attribution error or a liquidity-share estimate leaves that quantity
  explicitly `UNRATIFIED`**, in the same terms the existing placeholders use. Replacing one guessed
  constant with a measurement plus a different guessed constant, and reporting the result as
  calibrated fee yield, is the specific failure this clause exists to prevent.
- **No capital is authorized by this blueprint.** Any mainnet position requires separate, explicit
  capital approval recorded in the fee-yield ADR.
- **No EV placeholder is ratified, replaced or moved** on the strength of this design. Until a
  measurement exists the labelled placeholder stands, which is strictly better than an unlabelled
  one.

---

## 11. Non-goals

The archive is:

- **not telemetry** — `observability_contract.md` governs what a running bot emits, for a different
  consumer and a different lifetime (§2a)
- **not a backtester** — replay consumes the archive later and is a separate domain; `src/backtest/`
  remains reserved for replay, scenarios and metrics
- **not restart state** — `state_store.md` remains the only owner of durable restart facts (§2)
- **not a dependency of the trading process** — for boot, decisions, or execution (§3)
- **not a live EV input** — calibration reaches the gate as ratified constants through an ADR, never
  as a data read (§3)
- **not an execution data source** — it holds no signer and cannot write to a venue (§3)

---

## 12. Prohibitions

- Do not place the archive under `state_store.md`, or let its absence or corruption affect boot.
- Do not let the trading process read the archive, at boot or at any later point.
- Do not import `src/decision/` from `src/observation/`; restate the `ev_policy.md` §5a formula or
  hoist the helper to a shared module.
- Do not add an `estimator_shadow` field, or any further derived field, without an ADR (§5e).
- Do not record fee accrual as interval-only deltas (§5b).
- Do not omit `bin_count` from a cost observation (§5c).
- Do not poll Solana RPC at one-second cadence to manufacture a volatility series (§5d).
- Do not sample `bins[]` at the `pool_samples` cadence. Liquidity distribution is a slow variable and
  price is not; sampling the distribution at the price cadence multiplies the run's storage by an
  order of magnitude for no analytical gain (§8).
- Do not write a sample as absent. A failed, throttled or overrun sample is present and marked.
- Do not interpolate, backfill, or compute a return series across a gap (§7).
- Do not compute volatility across a restart boundary or non-consecutive `seq` values.
- Do not publish a derived figure without its coverage ratio (§6, §9).
- Do not give the recorder a signer, Binance credentials, or any `src/execution/` import (§3).
- Do not let the recorder read the trading binary's configuration keys, or place a mainnet
  observation target in a variable the trading binary reads (§3).
- Do not site the archive on the State domain's partition (§3) — except on a single-volume host under [[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]], where the free-space floor is mandatory instead.
- Do not apply `config_contract.md` §5's Dual-LAN requirement to the recorder (§8a).
- Do not carry network verification between hosts, or treat the 2026-09-25 macOS measurements as applying to the current Windows host (§8b, as corrected by [[adr-036-single-volume-host-and-archive-free-space-floor|ADR-036]]).
- Do not treat the configured Devnet pool as a calibration target (§6a).
- Do not choose a fee-measurement route, ratify an EV placeholder, or authorize capital under this
  blueprint (§10).

These prohibitions are binding.
