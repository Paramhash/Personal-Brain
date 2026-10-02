---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/config_contract.md
bot_commit: e532796
source_sha256: 7feab5f8f884311cddc3ea7cb0cf124db94038f6398f916d597d8bc536ee9107
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/config_contract.md` at commit `e532796`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

<!-- markdownlint-disable MD012 -->

# Config Contract

**Domain owner:** Runtime configuration and dependency policy
**Status:** authored and binding
This file fixes how the repository handles package pinning, dependency conflicts, and runtime configuration ownership.

---

## 1. Scope

This blueprint governs:

- dependency version pinning in `package.json`
- use of npm `overrides` for nested dependency conflicts
- config ownership for runtime thresholds and environment-driven behavior
- package-level rules that preserve single class identities across Solana SDK boundaries

The canonical implementation file for immutable strategy thresholds is `src/config/strategy.config.ts`.

It does not define business logic thresholds themselves unless a later design ticket authors the config key surface.

---

## 2. Absolute pinning policy

All first-party dependency entries in `package.json` must be pinned to exact versions.

- no caret ranges: `^`
- no tilde ranges: `~`
- no tag-based references such as `latest`

The manifest is a runtime control surface. Silent minor or patch drift is treated as an architecture defect, not a convenience.

---

## 3. Nested dependency conflict policy

When a nested dependency conflict creates multiple runtime copies of a package that owns class identity or decoding semantics across the Solana SDK boundary, the repository must prefer one of two remedies:

1. align the root pin to the SDK's required version when that is safe and sufficient
2. add an npm `overrides` block that forces the nested package to exactly one version

This rule exists to prevent duplicate runtime identities for packages such as Anchor and Borsh, where two copies can break `instanceof`, coder compatibility, or account decoding.

If a conflict cannot be resolved cleanly with one of those remedies, stop and escalate via an ADR before adding more code.

---

## 4. Overrides rule

`package.json` must use npm `overrides` when nested dependency conflicts remain after root pin alignment and the conflicting package is part of a runtime identity surface.

Example class of use:

```json
{
  "overrides": {
    "@coral-xyz/borsh": "0.31.0"
  }
}
```

An override must always use an exact version string.

After adding or changing `overrides`:

1. delete `node_modules`
2. delete `package-lock.json`
3. rerun `npm install`
4. verify the resolved tree with `npm ls`

Lockfile surgery without a clean reinstall is not permitted.

---

## 5. Runtime config ownership

Runtime thresholds, cadences, and environment-derived behavior belong under the config domain once implementation begins. Until a formal config module is authored, feature code may inject threshold objects from the boundary layer, but it must not invent a parallel config ownership model.

### Strategy threshold surface

`src/config/strategy.config.ts` owns the immutable numeric defaults that are already ratified by findings and ADRs. The initial exported constants must be:

```ts
export const zeroGammaProximityPctThreshold = 0.0075;
export const hardZglCrossBufferPct = 0.0010;
export const threatPersistenceSnapshots = 2;
export const spotVelocityBpsPerSecond = 8;
export const redeployMinObservationMinutes = 20;
export const redeploySafeDistancePct = 0.0125;
export const redeployStableSnapshots = 12;
export const redeployRealizedVolCap1m = 0.0035;
export const deribitRefreshCadenceMs = 5000;
export const snapshotFreshnessBudgetMs = 7500;
export const deribitRequestTimeoutMs = 20000;
export const invalidRowTolerancePct = 0.05;
export const riskFreeRate = 0;
export const leverage = 5;
export const safetyBufferQuote = 50;
export const epsilonBase = 0.0625;
export const dlmmStrategyType = 'Curve';
export const swapSlippageBps = 50;
```

No placeholder values are permitted in that file.

#### [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] wall selection (UNRATIFIED levels)

Two constants are owned here and are **explicitly unratified**. They are not placeholders in the sense §5 forbids — the *rule* each serves is ratified and the values are the ones [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] records — but neither is a measurement, and both must be labelled wherever they surface.

```ts
export const callWallAccumulationFraction = 0.8;
export const missingWallAlarmTicks = 10;
```

`callWallAccumulationFraction` is the share of a side's eligible Dollar GEX magnitude that a wall must account for. **One value, applied symmetrically to the call and put accumulation rules** — there is deliberately no second put-side threshold, because two independently tunable levels would let the envelope become asymmetric for reasons nothing measures. The name is call-specific because [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] and `gex_intelligence.md` §6 name it so; a side-neutral rename is an open ADR-amendment question and not an implementer's change.

It must be **carried into `SolGexSignalPayload`** as `callWallAccumulationFraction_t`, so a stored or replayed frame identifies the policy value behind its walls. Frames produced under different values are not comparable, and the provenance field is what makes that visible.

`missingWallAlarmTicks` gates the **call-side** missing-wall alarm only; the put side escalates immediately (§6b). The unit is distinct source snapshots, not consumer reads.

Neither value may be duplicated in a feature module, and neither may be described as calibrated. The 24-frame capture behind [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] cannot discriminate `0.8` from the competing rules it was tested against, and nothing measures how long a missing wall persists.

#### [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]] wall buffer

```ts
export const wallBufferRoomFraction = 0.25;
export const wallProximityBasisMarginPct = 0.003;
```

`wallBufferRoomFraction` is `k` in [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]] §2a — the share of the room between spot and each wall given up on entry. **Ratified as policy and NOT calibrated**; those are different statuses, and nothing measures 0.25 as better than 0.20 or 0.30. [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]] §10 carries a measurable revisit trigger. It must be applied as a fraction of the available *room*, never as an absolute inset on the wall price, and the name `wallBufferFraction` must not be reintroduced — that was the rejected multiplicative parameter, whose ceiling `b_max = callDist / (1 + callDist)` blocks all deployment when walls tighten.

`wallProximityBasisMarginPct` is [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]]'s measurement-backed basis margin: the pool/spot basis was at most 0.2777% across 1336 recon records, so 0.3% covers all held evidence. **It is consumed by nothing today** — it belongs to an entry/exit inequality with no left-hand side until the deferred proximity threshold `t` is ratified. It is declared here because this file is the home of the ratified numeric surface, and it must not be surfaced beside the buffer as though the buffer applied it.

#### [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] pool cost factors (UNRATIFIED measurements)

```ts
export const poolSpotSigmaRatio = 0.88;
export const poolBurstFactor = 0.74;
```

**Status.** Both are owned here and are **explicitly unratified**, on the [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] pattern: the rule each serves is
ratified ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D1 and D5), and the values are the measurements [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] records. Neither is a calibration, and both
must be labelled wherever they surface.

**What they are.** Both are measured on the target Meteora pool against Deribit spot, at the research simulator's
30 s cadence (TICKET 028 Part 0):
- `poolSpotSigmaRatio` is the pool's σ over Deribit spot's: 0.882 overall, 0.82–0.91 per UTC day.
- `poolBurstFactor` is the pool's mean absolute 30 s move over a Gaussian's of the same variance: 0.739 overall,
  0.60–0.81 per day.

**How they are consumed.** They enter the EV gate only through `rangeCostRates` (`ev_policy.md` §3b). The gate,
[[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s model and the research simulator read these two constants and never restate them.

**Why there is no `PLACEHOLDER_` prefix.** [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] drafted them as `PLACEHOLDER_POOL_*`. This file permits no
placeholder values, so they carry the [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] form instead, and [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]]'s implementation note records the rename.

**What reopens them.** Either value leaving its measured range for a full [[adr-033-fee-yield-measurement-route|ADR-033]] sub-window reopens [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D1.

`zeroGammaProximityPctThreshold = 0.0075` is consumed by the Intelligence Engine (Q003) to classify the `ZERO_GAMMA_PROXIMITY` regime. It is not consumed directly by the Q004 Macro FSM, which reads the resulting `regimeLabel_t` and `distanceToZglPct_t` fields from the already-classified signal payload.

`deribitRefreshCadenceMs = 5000`, `snapshotFreshnessBudgetMs = 7500`, and
`deribitRequestTimeoutMs = 20000` are the mandatory Deribit transport defaults for the
Phase 6 Market Data module. The freshness budget deliberately allows one missed refresh cycle
before the snapshot must be treated as stale.

**The request ceiling is 20 s as of [[adr-026-devnet-tolerance-and-timeout-adjustments|ADR-026]].** [[adr-012-deribit-linear-options-usdc-settlement|ADR-012]] set it to 10 s on the reasoning that the
ceiling "accommodates the approximately 3,000-record JSON payload returned by the live USDC
options query". Measured, it does not: the 2026-09-19 08:52 soak recorded 20
`Deribit request timed out after 10000ms` failures against 7 successful refreshes, with the
ADR-013 ticker subscription already disabled and the venue answering an unsubscribed probe of the
same query in ~800 ms. The ceiling is therefore raised rather than the payload reduced.

Raising it does **not** relax the protections that depend on it, and must not be read as doing so.
The ceiling now exceeds both the cadence and the freshness budget by a wide margin, so a request
that runs its full 20 s overruns its own cadence and blows the freshness budget. That surfaces as
`tick_skipped` with `previous_tick_still_running` from the orchestrator's single-flight guard, and
as a latched `snapshotStale_t`. Both are the intended failure direction and neither is weakened by
the larger number: the guard prevents overlap regardless of how long a request takes, and the
latch is cleared only by a genuinely new snapshot. The three values remain mutually inconsistent
by design, and the cadence is still the one that should be revisited next.

### Dual-LAN bindings are verified at boot, not assumed

The two local addresses are required runtime configuration, and presence is not sufficient. A
configured address must additionally be **assigned to exactly one IPv4 interface**, and the two
keys must resolve to **different** interfaces. The composition root asserts both before any socket,
agent or logger is constructed, and refuses to start otherwise.

This is not a theoretical guard. On 2026-09-19 `INTELLIGENCE_LOCAL_ADDRESS` was set to an address
assigned to *two* interfaces at once — a wired NIC and Wi-Fi, on one L2 segment. Two MACs answered
ARP for it, the gateway's cache flapped between them, and the roughly 3,400-row Deribit book
summary was truncated whenever it flipped mid-transfer. The TLS handshake is small enough to
survive, so the socket always opened and the fault presented as a venue timeout. Three code changes
were made at the wrong layer before the cause was found. The same inspection also showed that both
keys had been pointing at addresses on the *same* interface, so the separation this section
mandates had never actually operated.

A silent violation of this requirement is therefore the expensive failure mode, and a boot refusal
is the cheap one. The check reports every fault in one pass, names the environment key and the
interface, and **never prints the address** — the rule that a diagnostic must not emit the host's
addressing applies to this message as it does to any other.

An interactive prompt is explicitly not the mechanism. The process is a headless daemon whose
stdout is a structured-JSON stream; blocking on stdin would hang an automated start and leave a bot
waiting at a terminal nobody is watching.

`invalidRowTolerancePct = 0.05` is the mandatory threshold at which dropped-row volume must
degrade the snapshot rather than merely report `droppedInstrumentCount_t` diagnostically.

`riskFreeRate = 0` is the mandatory default input to the deterministic Black-Scholes gamma
calculation unless a later ADR assigns a non-zero policy rate.

### Hedge risk surface

`leverage = 5`, `safetyBufferQuote = 50`, and `epsilonBase = 0.0625` are the mandatory
HedgeRiskConfig values consumed by the F-002 hedge feasibility and execution boundary.

`safetyBufferQuote` is the USDC-equivalent safety margin added after initial margin. The
hedge engine must calculate required collateral as target notional divided by `leverage`, plus
this buffer.

`epsilonBase = 0.0625` is exactly $1 / 16$ in binary floating-point representation. The
hedge tolerance comparison is the documented exact $\leq$ comparison from H12; using a
binary-exact threshold prevents representation error in the threshold itself from deciding an
edge case.

### Deployment execution surface

`dlmmStrategyType = 'Curve'` is the ratified liquidity shape for deployment. It satisfies
`liquidity_position_manager.md` §3 by selecting an allowed strategy and weights liquidity
toward the center of the approved range.

`swapSlippageBps = 50` is the maximum permitted Jupiter re-ratio slippage. The Jupiter adapter
must use this cap in its `/quote` request and must not silently widen it after a failed or
stale quote.

Mints, RPC endpoints, signer material, and venue credentials are environment configuration,
not immutable strategy constants. They must be supplied at the adapter boundary and never
committed to `strategy.config.ts` or emitted in logs.

### Runtime adapter network surface

The Phase 11 adapter boundary requires two runtime environment values for physical traffic
separation:

```text
intelligenceLocalAddress
executionLocalAddress
```

`intelligenceLocalAddress` is the local source address used by Intelligence-facing market-data
streams, including Deribit and Binance WebSocket clients. `executionLocalAddress` is the local
source address used by Execution-facing RPC and REST clients, including Solana RPC connections
and Jupiter requests.

These values are required runtime configuration. They must remain injected adapter parameters,
must never be committed to source, and must not be stored in `strategy.config.ts`. The adapter
layer must apply them when constructing network clients so Intelligence streams and Execution
RPC calls can be routed through separate physical NICs.

### Monitor key surface (TICKET P, TICKET U; `monitor.md`)

The read-only monitor resolves its own `MONITOR_*` keys in `src/monitor/monitorConfig.ts`
(`KNOWN_MONITOR_KEYS`); an unknown `MONITOR_*` key fails startup by name, never by value. No
`MONITOR_*` key may hold an endpoint or credential — the RPC endpoint still comes from the observer
boundary (`OBSERVER_SOLANA_RPC_URL`).

```text
MONITOR_HOST, MONITOR_PORT, MONITOR_CADENCE_MS, MONITOR_CONTESTED_MARGIN, MONITOR_REPLAY_ROOT
MONITOR_VENUE                        meteora-dlmm (default) | orca-whirlpool        — ADR-044
MONITOR_ORCA_POOL_ADDRESS            required for orca-whirlpool; public base58 address
MONITOR_ORCA_EXPECTED_BASE_MINT      required; must be the pool's token A (checked every read)
MONITOR_ORCA_EXPECTED_QUOTE_MINT     required; must be the pool's token B
MONITOR_ORCA_TICK_SPACING            required; must equal the pool's tick spacing
MONITOR_ORCA_BAND_PCT                optional, default 0.10, at most 0.5
MONITOR_ORCA_STATS_CADENCE_MS        optional, default 300000, at least 60000 (ADR-044 amendment)
MONITOR_RECORD_ROOT                  optional, either venue (ADR-045 Amendment 1); the monitor's own frame
                                     recording; never at or inside OBSERVER_ARCHIVE_ROOT, and never the
                                     same as or nested with MONITOR_REPLAY_ROOT
MONITOR_RECORD_MIN_FREE_BYTES        optional, default 53687091200 (50 GiB), at least 10 GiB
MONITOR_HURDLE_CAPITAL_BASE          optional, either venue; SOL-equivalent capital the Hurdle panel
                                     models (ADR-046), default 50; display only
```

`MONITOR_ORCA_*` keys are refused when the venue is Meteora DLMM (`MONITOR_RECORD_*` are accepted for both since
[[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]] Amendment 1), and
`MONITOR_REPLAY_ROOT` is refused when it is Orca ([[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] §5) — the Orca monitor replays its own
recordings from `MONITOR_RECORD_ROOT` instead ([[adr-045-orca-monitor-records-its-own-frames-for-replay|ADR-045]]).

### Fee-growth sampler key surface (TICKET 027, [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]])

Read by `src/feegrowth/feeGrowthConfig.ts`. The RPC endpoint and pool come from `observer.env` through `resolveObserverConfig`, not from these keys. An unknown `FEEGROWTH_*` key fails by name, and values are never shown.

```text
FEEGROWTH_ROOT             default C:\observation\dlmm-fee-growth; never at or inside OBSERVER_ARCHIVE_ROOT
FEEGROWTH_CADENCE_MS       default 300000, at least 60000
FEEGROWTH_RANGE_PCT        default 0.10 (ADR-050 D2), above 0 and at most 0.5
FEEGROWTH_MIN_FREE_BYTES   default 53687091200 (50 GiB), at least 10 GiB
FEEGROWTH_PORT             default 7763; loopback health only
```

### Notifier key surface (TICKET X, [[adr-048-health-alarms-to-the-operators-discord|ADR-048]])

Read from `C:\observation\notifier.env` by `src/monitor/notify/notifierConfig.ts`; an unknown `NOTIFIER_*` key fails
by name, and no error shows a value.

```text
NOTIFIER_DISCORD_WEBHOOK_URL   required; a credential — https://discord.com/api/webhooks/… only; never logged
NOTIFIER_CADENCE_MS            default 60000, at least 15000
NOTIFIER_HEARTBEAT_UTC_HOUR    default 0 (the daily heartbeat hour, UTC)
NOTIFIER_DISK_ALERT_FREE_GIB   default 75
NOTIFIER_ARCHIVE_ROOT          default C:\observation\archive (metadata only)
NOTIFIER_RECON_ROOT            default C:\observation\recon-evidence-T2-2026-09-28
NOTIFIER_ORCA_RECORD_ROOT      default C:\observation\monitor-orca-frames
NOTIFIER_DLMM_RECORD_ROOT      default C:\observation\monitor-dlmm-frames (TICKET Z; metadata only)
NOTIFIER_FEEGROWTH_ROOT        default C:\observation\dlmm-fee-growth (TICKET 027; metadata only)
NOTIFIER_HEALTH_LOG            default C:\observation\logs\health.log
# TICKET Y (ADR-049): market events and the daily summary
NOTIFIER_MARKET_ENABLED              default true; true | false
NOTIFIER_DISCORD_MARKET_WEBHOOK_URL  optional; a credential, same shape rule; unset = the alarm webhook
NOTIFIER_SUMMARY_UTC_TIME            default 00:05; HH:MM, UTC
NOTIFIER_MARKET_MAX_PER_HOUR         default 6; integer 1–60; the excess is folded into one message
```

### Operator-overridable strategy defaults ([[adr-026-devnet-tolerance-and-timeout-adjustments|ADR-026]])

A ratified constant may be given an **operator override** without ceasing to be ratified. The
ratified value remains in `strategy.config.ts` as an exported default, and the override is parsed
**in that same file**, at import, so the exported constant every consumer already reads carries
the resolved value and no consumer contract changes.

This is a deliberate, bounded exception to the rule above that runtime environment "must not be
stored in `strategy.config.ts`". The distinction it rests on: that rule exists to keep mints,
endpoints, credentials and signer material — values that are secret, deployment-specific, or
required — out of source and off the strategy surface. An override for a ratified *strategy
threshold* is none of those. It has a committed default that is correct for production, it is
absent in production, and it is the same kind of number as the constant it replaces. Resolving it
anywhere else would split one value across two files and leave consumers reading whichever half
their import happened to reach.

```text
REBALANCE_TOLERANCE_BASE   ->  reRatioReserveToleranceBase   (default 0.05 whole base tokens)
SIGMA_SOURCE               ->  sigmaSource                   (default trailing; trailing | placeholder)
```

`SIGMA_SOURCE` ([[adr-047-provisional-sigma-estimator|ADR-047]], TICKET Z Part B) chooses the σ the range planner and the EV gate use: `trailing` is the [[adr-047-provisional-sigma-estimator|ADR-047]]
chain, and `placeholder` is the kill switch to the pre-ADR-047 behaviour. The root and both monitors read it. A value
other than those two fails at import, by name.

`reRatioReserveToleranceBase` is the band inside which `liquidity_position_manager.md` §2a
returns an exact-zero re-ratio. Devnet pool drift can move the wallet just past a hardcoded
`0.05`, which sends [[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]]'s calculator to Jupiter for a route the configured Devnet quote token
cannot be traded on — turning a harmless drift into `TOKEN_NOT_TRADABLE` instead of [[adr-024-rebalance-bypass-and-telemetry-fixes|ADR-024]]'s
bypass. The override exists so a Devnet operator can widen the band explicitly, in configuration,
rather than by editing a ratified constant.

The rules are binding:

- the **default is unchanged** and is what production uses when the variable is absent. An empty
  or whitespace-only value counts as absent, because that is what an unset key in a `.env` file
  usually produces
- an override must be **validated and fail closed**: a malformed, non-numeric, non-finite, zero or
  negative value is a boot failure that names the key, never a silently substituted default. An
  operator who meant to widen the band and mistyped must not get production's `0.05` instead
- the parser must take its environment as a **parameter**, so the malformed cases are assertable
  offline against an injected object rather than by mutating the real environment. The exported
  constant applies it once to `process.env`
- a widened band is a **Devnet convenience, not an economic policy**. It suppresses small
  re-ratios; it does not make the resulting inventory correct

This pattern applies only where an ADR grants it explicitly. It is not a general licence to make
ratified constants environment-tunable, and it does not extend to mints, endpoints, credentials or
signer material, which remain adapter-boundary configuration under the rule above.

### EV gating rule

The canonical EV hurdle is binding across config and decision domains:

```text
net_ev >= 1.5 * (swap_slippage + gas_fees)
```

Feature modules may consume this rule, but they may not redefine the multiplier or the shape of the inequality ad hoc.

[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] added `projected_hedge_drag_quote` inside `net_ev` (`ev_policy.md` §3b, §4). The inequality is textually
unchanged. Its two new EV placeholders live with the other EV placeholders in `src/decision/ev/evCalculator.ts`,
labelled UNRATIFIED:
- `PLACEHOLDER_HEDGE_TAKER_FEE_FRACTION = 0.0005`;
- `PLACEHOLDER_HEDGE_CHECK_INTERVAL_SECONDS = 30`.

`hurdleRate.ts` re-exports both.

---

## 6. Prohibitions

- Do not use version ranges in `package.json`.
- Do not accept duplicate runtime copies of Anchor, Borsh, or equivalent coder/class identity packages once detected.
- Do not patch `package-lock.json` manually to simulate deduplication.
- Do not add `overrides` without a verification step that proves the tree collapsed.

These prohibitions are binding.

