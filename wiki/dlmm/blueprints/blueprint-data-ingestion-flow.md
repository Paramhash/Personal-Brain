---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/data_ingestion_flow.md
bot_commit: 93d497d
source_sha256: c01b94755fb32db938ce9ba1eef82e436b62eaf11470cd2e2b06db8edf69661b
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/data_ingestion_flow.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Data Ingestion Flow

**Domain owner:** Market Data
**Status:** authored and binding
This file fixes the ownership, transport rules, freshness semantics, and normalization boundaries for Deribit options summaries, Solana account streams, Binance hedge-state feeds, and snapshot publication into the rest of the system.

---

## 1. Scope

This blueprint governs:

- Deribit SOL options-summary intake
- Solana account-state stream intake for DLMM position and pool context
- Binance hedge-state feed intake
- normalization of venue-specific wire payloads into repository-owned snapshot records
- snapshot freshness, stale-data signaling, and disconnect handling

It does not govern gamma math, Dollar GEX aggregation, wall extraction, or zero-gamma interpolation. Those belong to `gex_intelligence.md`.

It does not authorize execution logic, RPC writes, order placement, or hedge resizing. This domain reads and normalizes only.

---

## 2. Ownership and outputs

The Market Data domain owns the transport lifecycle and the normalized snapshot boundary for:

- Deribit off-chain options summaries
- Solana on-chain account and position observations
- Binance hedge-state observations

Its responsibility ends at emitting timestamped, validated, normalized snapshots downstream.

Canonical market-data state variables are:

```text
spotOffchain_t
optionChainSnapshot_t
snapshotGeneratedAt_t
snapshotStale_t
instrumentCount_t
droppedInstrumentCount_t
```

Downstream modules may read these facts. They may not repair, interpolate, or silently restamp them.

---

## 3. Deribit transport rule

Deribit SOL option summaries must be collected through a persistent JSON-RPC WebSocket connection to:

```text
wss://www.deribit.com/ws/api/v2
```

The required request method is:

```text
public/get_book_summary_by_currency
```

with exactly these semantic parameters:

```text
currency = USDC
kind = option
```

Because the currency parameter selects the settlement bucket rather than the option
underlying, the transport contract must filter the returned records client-side and pass
forward only rows where `base_currency === SOL`. The SOL filter is part of the transport
contract and must run before the normalization layer.

Short-lived HTTPS polling is not the approved transport for this repository.

### 3a. Deribit ticker subscription — the second, push-based source

The request/response pattern above is the **discovery and reconciliation** source, and it
remains authoritative for the instrument set, `base_currency` filtering, `open_interest`, and
every wire field [[adr-012-deribit-linear-options-usdc-settlement|ADR-012]] fixed. A second source is permitted on the **same** connection for
venue-native option greeks:

```text
public/subscribe   channels: ticker.<instrument_name>.<interval>
```

The rules are binding:

- the ticker subscription is **additive**. It may not replace, gate, or reorder the
  `public/get_book_summary_by_currency` call, and a snapshot must remain assemblable when no
  ticker push has ever arrived
- channels must be **batched** across `public/subscribe` requests rather than sent one
  instrument at a time. Deribit's public rate limits are request-count based, so one request
  carrying many channels costs one request; ~580 individual calls is an avoidable breach
- only instruments that have already passed the §3 SOL filter may be subscribed. The filter
  runs first, as it does for normalization
- the push interval is a declared constant in the transport module, not a literal repeated at
  each call site
- a subscription push arrives as `{ method: 'subscription', params: { channel, data } }` and
  carries **no** `id`. It is a distinct frame shape, not a further case of the id-correlated
  response envelope, and must be handled on its own branch. An id-correlated reader must not
  consume it and it must not consume an id-correlated reply

The ticker source is a **preference input, never a gate**. Its absence for a given instrument
is not a drop reason, does not increment `droppedInstrumentCount_t`, and does not make the
snapshot stale. The consuming domain falls back to its own computation, per
`gex_intelligence.md` §3.

The practical pattern is:

1. maintain one long-lived WebSocket session
2. send JSON-RPC request frames on that connection at the chosen refresh cadence
3. correlate responses by request id
4. treat disconnects, malformed responses, and stale snapshots as first-class events

The ingestion module may reconnect after a disconnect, but it must not backfill the gap by pretending the last good snapshot is current.

---

### 3b. Binance transport rule — two independent streams

Binance hedge state is **not** one feed. The venue publishes the two halves this repository
needs on two different connections, with two different authentication models, and no single
Binance stream carries both. The transport contract is therefore two streams, not one:

**1. Public market data.**

```text
<ws base>/ws        subscribe: <symbol>@markPrice
```

The socket must send an explicit `SUBSCRIBE` frame after it opens:

```text
{ "method": "SUBSCRIBE", "params": ["<symbol>@markPrice"], "id": <n> }
```

A bare `/ws` connection with neither a stream name in the path nor a `SUBSCRIBE` frame is a
valid, open and permanently silent socket. It is not an error state, it raises no event, and
`isConnected()` reports `true` throughout — which makes the omission invisible to every health
check. The subscribe frame is part of the transport contract for exactly that reason.

This stream carries the symbol, the mark price, the last funding rate, and the next funding
time. It carries **no** account or position data.

**2. Authenticated user data.**

```text
POST /fapi/v1/listenKey   ->  listenKey
<ws base>/ws/<listenKey>  ->  ACCOUNT_UPDATE frames
```

This stream carries account balances and position amounts. It is reachable only with a
REST-created `listenKey`, which has a bounded lifetime and must be kept alive on a timer at the
venue's documented interval. An expired or invalidated key ends the stream; the venue may also
announce it in-band as a `listenKeyExpired` event.

The rules are binding:

- the two streams have **independent** validation boundaries, connection and reconnect
  lifecycles, latched freshness budgets, stale reasons, and diagnostics
- neither stream's frame may satisfy the other's freshness. A fresh mark price does not make an
  account reading current, and a fresh account update does not make a mark price current
- the `listenKey` lifecycle is owned by the transport: created before the authenticated socket
  opens, kept alive on its documented interval, recreated on expiry, and closed — with its
  timer — on disconnect
- credentials, listen keys, and signed URLs are adapter-boundary material. They are never
  logged, never returned to a downstream consumer, and never read by a policy module
- the `SUBSCRIBE` acknowledgement (`{"result":null,"id":n}`) is a control frame, not a data
  frame. It must not be normalized and must not increment the dropped-frame counter

---

## 4. Freshness and stale-snapshot semantics

Every published snapshot must carry a repository-owned timestamp indicating when the snapshot was generated from validated source data.

The canonical freshness fields are:

```text
snapshotGeneratedAt_t
snapshotStale_t
```

The rules are binding:

- each snapshot must be timestamped when the normalized snapshot is assembled
- a disconnected socket must force `snapshotStale_t = true`
- a socket that remains connected but has exceeded its freshness budget must force `snapshotStale_t = true`
- stale data must never be silently interpolated, extrapolated, or republished with a fresh timestamp
- the last known snapshot may remain readable for diagnostics, but its stale flag must remain true until a fresh snapshot replaces it

If the ingestion layer cannot prove freshness, it must emit staleness.

### 4a. Freshness of a per-instrument push source

A push source keyed by instrument carries its own freshness, one key at a time. The
snapshot-level rules above are unchanged; these govern the per-instrument values layered on
top of them:

- each stored per-instrument value carries its **own** received-at timestamp, and is fresh
  only while that timestamp is inside the freshness budget
- one instrument's push may never stand in for another's. There is no chain-wide received-at
  for a per-instrument source
- an instrument that has **never** received a push is *not* stale. It has no value, which is a
  different fact from a value that can no longer be trusted, and it resolves to the consumer's
  fallback rather than to a staleness signal
- a per-instrument value that has aged out resolves the same way as one that never arrived:
  the reader yields nothing and the consumer falls back
- a still-open socket carrying a stalled push feed must not suppress `snapshotStale_t`, and
  equally must not force it. The snapshot's own freshness is decided by §4 against the
  request/response source, which is the source the snapshot is assembled from
- a disconnect invalidates the stored per-instrument values. Venue subscriptions do not
  survive the socket, so a reconnect inside the freshness budget must not resurrect values it
  is no longer receiving — that is §3's backfill prohibition applied per key

---

### 4b. Freshness of a composite snapshot assembled from two sources

A snapshot assembled by merging two independently-fed source states carries the freshness of
the **worse** half.

**Two freshness classes.** §4's age check assumes a source that is *supposed* to push on a
clock, and silence from such a source is evidence it has failed. That assumption does not hold
for every feed, and applying it where it does not hold produces a false staleness that is
indistinguishable from a real one. Each source therefore declares its class:

**Clocked.** The source pushes on a cadence of its own, unconditionally — the public
`<symbol>@markPrice` stream is one. Freshness is the §4 rule unchanged: the stored received-at
timestamp, checked against the configured `snapshotFreshnessBudgetMs`. Silence past the budget
latches stale, because for this class silence *is* the failure.

**Latched-Until-Contradicted.** The source publishes state transitions rather than a heartbeat —
Binance `ACCOUNT_UPDATE` is one. **Event silence is normal and must not age out a valid source
state**: an account that has not traded for an hour is not an account whose state is unknown, it
is an account that has not changed. A source in this class has **no age check at all**. It is
fresh while, and only while:

- its websocket is open, **and**
- its authenticating credential — for Binance, its listen key — is valid, **and**
- its keepalive loop is succeeding

and it latches stale on any of: socket closure, credential expiry or invalidation, keepalive
failure, malformed source state, or an explicit transport failure. The latch is cleared only by
a **new valid event on a newly established authenticated session** — restoring the session alone
proves nothing about the state, which is §3's backfill prohibition applied to a credential.

A source in this class trades one failure mode for another, deliberately. A clocked source
detects a silently wedged feed by its silence; this one cannot, and relies on its liveness
signals instead. That is the correct trade only because those signals exist and are checked —
a latched-until-contradicted source with no keepalive would be a source that can never be
known to be wrong.

These govern the composite:

- each source state carries its own received-at timestamp, its own latch, and its own stale
  reason, resolved independently against the rule for **its own class**
- the composite may be emitted as **fresh only when every source is present, validated and
  fresh by its own class's rule**. If any source is missing, stale, disconnected, or — for an authenticated source —
  backed by an expired key, the composite is marked `snapshotStale_t = true` and must not be
  treated as current hedge state
- the composite's `snapshotGeneratedAt_t` is the **oldest** contributing source timestamp, not
  the newest. A composite is no more current than its stalest half, and stamping it with the
  newer half would republish the older one under a fresh timestamp, which §4 forbids
- a latched-until-contradicted source may take its **first** value from an authoritative
  out-of-band read rather than from an event, published on a session that is live at that moment.
  This is a seed, not a backfill: `ACCOUNT_UPDATE` fires only on a fill, a transfer or a funding
  payment, so an idle account never delivers a first frame and the composite would otherwise
  never exist at all. The seed is permitted **once, on the first successful read** — a repeat
  after a stale event would be a session restoring a value it cannot vouch for, which the rule
  below forbids. A failed seed leaves no value and may be retried
- a composite has no value at all until every source has delivered at least one valid frame.
  That is an absence, not staleness — the same distinction §4a draws for a per-instrument key
- reconnecting one source does not clear that source's latch, and never touches the other's.
  Only a genuinely new valid frame on a source clears that source's latch (§3's backfill
  prohibition, applied per source)
- the composite's stale reason must identify **which** source is responsible. "Stale" without
  a source is not actionable when the two halves fail for unrelated causes

---

### 4c. Reconnection is required, bounded, and never a source of freshness ([[adr-027-socket-stability-and-boot-validation|ADR-027]])

§3 says a transport "may reconnect after a disconnect, but it must not backfill the gap". That
settled what a reconnect may not do and left open whether one has to happen at all. Both
transports read it as optional and were connect-once: the socket dropped, the source latched
stale, and nothing ever called `connect()` again. The process stayed up, so nothing looked
broken — which is why the 2026-09-19 Step 6 run spent its whole life emitting
`socket is not connected` against a venue that was answering probes in under a second.

A persistent transport **must** attempt to re-establish a dropped connection, and the attempt
must be:

- **single-flight per source.** A drop announces itself more than once — typically `error` then
  `close` — and every notification asks for a reconnect. All but the first are no-ops while an
  attempt is pending or in flight; otherwise each one opens a socket the client cannot reference
- **bounded.** Delay grows with consecutive failures and is capped. An unbounded exponential
  eventually schedules the next attempt further away than any operator would wait, which is
  connect-once reached slowly
- **time-limited per attempt.** A socket that neither opens nor errors must be abandoned and
  closed, or it holds the source's only slot indefinitely
- **cancellable.** An explicit `disconnect()` cancels anything pending or in flight, and cancels
  *before* closing the socket — the `close` it triggers reaches the same handler that schedules
  reconnection, and a scheduler cancelled afterwards reads a shutdown as an outage
- **resource-safe on every path.** No orphaned socket, listener, timer, or credential survives a
  failed attempt

**Reconnecting restores the transport and nothing else.** §4's latch is untouched by it: the
source stays stale until a genuinely new valid frame or snapshot arrives on the new session. For
a source with its own credential, the credential is released and re-minted rather than reused —
a stream may have dropped *because* the credential expired, and reconnecting with it reconnects
to a refusal.

**Independent sources reconnect independently** (§4b). One source coming back says nothing about
the other, and must not clear the other's latch, restart its session, or freshen the composite.

---

## 5. Validation and normalization boundary

Wire payloads from Deribit, Solana, and Binance are not repository contracts. They must be validated and normalized before any downstream module consumes them.

The ingestion layer must keep these representations distinct:

- raw wire payloads
- validated venue-specific records
- normalized repository snapshot records

No analytics module may run business math directly against unvalidated wire payloads.

Normalization responsibilities include:

- parse instrument identifiers into structured fields such as strike, expiry, and option side
- preserve source spot and implied-volatility fields exactly enough for deterministic downstream math
- count and surface dropped records rather than silently suppressing them
- sort or prepare snapshot collections into deterministic downstream order where needed

Missing or null `bid_price` and `ask_price` values are expected market conditions for valid
far-out-of-the-money or otherwise illiquid instruments. They are fully optional at the wire
boundary and must not trigger validation failure or increment `droppedInstrumentCount_t`.

An `open_interest` of exactly zero is likewise an expected market condition — an unheld
option, not a malformed one — and must not trigger validation failure or increment
`droppedInstrumentCount_t` ([[adr-014-zero-open-interest-degradation|ADR-014]]). Only a non-finite or negative `open_interest` remains a
drop reason.

A zero-open-interest row is **excluded before the counter**, at the same pipeline point the
§3 SOL filter uses to exclude foreign base currencies — not retained with `openInterest: 0`,
and not special-cased inside the drop-and-count loop. It therefore reaches neither
`droppedInstrumentCount_t` nor `instrumentCount_t` nor the normalized snapshot: by the time
normalization runs it was never a candidate row. [[adr-014-zero-open-interest-degradation|ADR-014]] records retention as an explicitly
rejected alternative, on the grounds that a zero-weight row inside `instrumentCount_t` buys no
analytical benefit — its contribution to any signed Dollar GEX sum is zero either way — and
blurs what `instrumentCount_t` means. The consequence [[adr-014-zero-open-interest-degradation|ADR-014]] accepts is that
`instrumentCount_t` counts the subset carrying open interest rather than the venue's full
listed chain.

The normalization boundary owns `droppedInstrumentCount_t`. A malformed or unsupported row is dropped explicitly and counted.

---

## 6. Venue-specific responsibilities

### Deribit

Deribit ingestion owns:

- WebSocket lifecycle
- request scheduling
- response-id correlation
- subscription lifecycle and un-correlated push-frame handling (§3a)
- SOL option-summary validation
- venue-native per-instrument greek custody and their per-instrument freshness (§4a)
- normalized option-chain snapshot publication
- stale/disconnect diagnostics

Custody is not interpretation. This domain stores what the venue sent, unmodified, and exposes
it. It does not sign it, scale it, substitute for it, or decide what it means — those belong to
`gex_intelligence.md`.

### Solana

Solana market-data intake owns:

- read-only account and pool observation
- normalized DLMM state snapshots for downstream consumers
- freshness semantics identical to the Deribit rules above

This blueprint does not authorize Solana writes. Those remain exclusive to `execution_router.md`.

### Binance

Binance market-data intake owns:

- read-only hedge-state observations
- the public `<symbol>@markPrice` subscription and its lifecycle (§3b)
- the authenticated user-data stream and the whole `listenKey` lifecycle — creation, keepalive,
  expiry handling, reconnect, and teardown (§3b)
- independent validation, normalization, latching and diagnostics for each of those two
  sources (§3b, §4b)
- assembly of the composite `BinanceHedgeStateSnapshot` from both source states, fresh only
  when both are fresh (§4b)
- normalized account, position, and mark-state snapshots needed for hedge feasibility and reconciliation
- freshness semantics identical to the Deribit rules above

The venue wire types for both streams stay local to the Binance module. Only the normalized
composite crosses the domain boundary, and the derived
`executed_short_notional_t = abs(position) * mark price` invariant is computed at assembly
rather than read from any venue field.

This blueprint does not authorize order placement or hedge resizing. The `listenKey` REST calls
are an ingestion concern and are not order placement; they create, refresh and release a
read-only subscription credential and nothing else.

---

## 7. Data-flow boundary

This domain writes only downstream into normalized state and intelligence inputs:

```text
marketdata -> state -> intelligence
```

It may not:

- call execution modules
- place trades or submit transactions
- classify GEX regimes
- compute Dollar GEX or zero-gamma levels

Those responsibilities belong further down the arrow.

---

## 8. Prohibitions

- Do not replace the persistent Deribit WebSocket with ad hoc request-per-process polling.
- Do not silently reuse the last good snapshot as if it were current after a disconnect or freshness breach.
- Do not run gamma or regime math inside the ingestion transport module.
- Do not hide malformed instruments by dropping them without incrementing `droppedInstrumentCount_t`.
- Do not let Market Data modules issue Solana or Binance writes.
- Do not send one `public/subscribe` request per instrument where batching is available.
- Do not let a per-instrument push source gate, delay, or invalidate the snapshot assembled
  from the request/response source.
- Do not apply an option-side sign, or any other analytic transform, to a venue-native greek
  inside this domain. It is stored exactly as received.
- Do not open a Binance stream socket without an explicit `SUBSCRIBE` frame or a stream name in
  the path. A silent socket that reports healthy is worse than a closed one.
- Do not expect account or position fields on the public mark-price stream, or mark-price and
  funding fields on the authenticated user-data stream. Neither venue frame carries the other's
  fields, and a schema that demands both rejects every real frame.
- Do not let one Binance source's freshness clear, extend, or stand in for the other's.
- Do not apply a clocked age check to a latched-until-contradicted source. Event silence is not
  a fault, and treating it as one makes a healthy idle account indistinguishable from a dead
  feed.
- Do not treat a latched-until-contradicted source as fresh on the strength of a restored
  session alone. A reconnect is not an event.
- Do not emit a composite hedge snapshot as fresh while either contributing source is stale,
  missing, disconnected, or backed by an expired listen key.
- Do not log, return, or hand downstream a listen key, an API credential, or a signed URL.

These prohibitions are binding.
