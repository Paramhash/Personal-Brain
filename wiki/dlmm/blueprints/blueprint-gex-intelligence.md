---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/gex_intelligence.md
bot_commit: 3f1eec9
source_sha256: f9925337af13d9d8df6bb95e5962864557936186733d243fb12684c8c0112287
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/gex_intelligence.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# GEX Intelligence

**Domain owner:** Intelligence
**Status:** authored and binding
This file fixes the deterministic analytics boundary for SOL gamma math, signed Dollar GEX aggregation, wall extraction, zero-gamma interpolation, and regime classification inputs emitted to the decision layer.

---

## 1. Scope

This blueprint governs:

- Black-Scholes gamma computation for normalized SOL option snapshots
- signed Dollar GEX per 1% move
- local and cumulative net GEX profile construction by strike
- Call Wall and Put Wall extraction
- deterministic Zero Gamma Level extraction
- consumption of intelligence thresholds from `src/config/strategy.config.ts`
- publication of `SolGexSignalPayload` into the shared protocol boundary

It does not govern transport lifecycle or venue connectivity. Those belong to `data_ingestion_flow.md`.

It does not govern macro-state transitions. Those belong to `state_machine.md` and its implementing reducers.

---

## 2. Required output contract

This domain emits the intelligence payload consumed by the macro decision layer:

```text
SolGexSignalPayload
```

The output remains a computed signal. It is not permission to execute, hedge, or mutate state directly.

The intelligence layer owns the derivation of:

```text
callWallStrike_t
putWallStrike_t
zeroGammaLevel_t
totalNetDollarGex1Pct_t
distanceToZglQuote_t
distanceToZglPct_t
regimeLabel_t
```

It reads normalized snapshots from Market Data and writes computed facts downstream.

---

## 3. Deterministic gamma rule

### 3a. Gamma source precedence

Gamma may come from either of two sources, in this fixed order:

1. **the venue-native gamma** carried on the normalized record, when it is finite and strictly
   greater than zero
2. **the local closed-form computation** below, in every other case

The precedence is binding and the fallback is unconditional. A record with no native gamma,
a null one, a non-finite one, or one at or below zero is **not** excluded on that basis — it
falls to the local computation exactly as though the native source did not exist. Absence of a
native value is a market and transport condition, never a drop reason, and never a degradation
signal.

Both sources are subject to the whole of this section without exception: both are unsigned,
neither may have an option-side sign applied to it, and the sign-application point in §4 is
unmoved. The venue computes the same closed form from the same inputs; preferring its value
removes the obligation to reproduce its risk-free-rate assumption, its time-to-expiry rounding,
and its IV normalization in order to agree with it. It does not introduce a second convention.

Determinism is preserved in the sense this blueprint requires: one normalized snapshot produces
one profile. The native value is a field **on** the snapshot, fixed at the moment the snapshot
was assembled, not a value re-read at computation time — so a given snapshot yields the same
profile on every replay. Custody and freshness of the native value belong upstream, to
`data_ingestion_flow.md` §3a and §4a; this domain reads what the snapshot carries and does not
reach for the transport itself (§10).

### 3b. The local computation

Black-Scholes gamma must be computed deterministically from normalized option records using:

- spot
- strike
- time to expiry in years
- implied volatility in decimal form
- the chosen risk-free rate input

Gamma is non-negative for both calls and puts under Black-Scholes. Option-side sign must therefore not be injected during gamma calculation.

If an instrument cannot support a valid gamma computation because a required input is malformed, expired, non-finite, or otherwise unusable, the record must be excluded explicitly from the GEX aggregation and reflected in the upstream or local drop diagnostics rather than coerced.

---

## 4. Canonical Dollar GEX formula

Dollar GEX per 1% move must be calculated exactly as:

$$
\text{gamma} \times \text{open\_interest} \times 10 \times \text{spot}^2 \times 0.01 \times k
$$

where:

- $k = +1$ for calls
- $k = -1$ for puts

The multiplier `10` is the Deribit SOL contract multiplier fixed by F-003.

The sign convention is binding. Calls contribute positive signed Dollar GEX; puts contribute negative signed Dollar GEX. The sign is applied during Dollar GEX conversion, not in the gamma function itself.

---

## 5. Profile construction rule

The GEX engine must produce two related strike profiles over strikes sorted in deterministic ascending order:

```text
local_net_gex_by_strike
cumulative_net_gex_by_strike
```

Definitions:

- `local_net_gex_by_strike` is the sum of signed Dollar GEX of all options at that strike
- `cumulative_net_gex_by_strike` is the running sum of `local_net_gex_by_strike` across sorted strikes

These are separate analytic objects and must not be conflated.

---

## 6. Wall extraction

Call Wall and Put Wall must be extracted deterministically from the aggregated strike surface.

A wall is **a bound, not a pin**. `range_planning.md` §2 consumes the pair as an envelope the deployed range may not leave, which requires the call wall to sit above the reference price and the put wall below it. A wall selected as the peak-gamma strike on its side does **not** satisfy that, because option gamma is maximised at the money: such a strike tracks spot and is a magnet level, close to the opposite of a ceiling. The selection is therefore constrained by side **and** taken distributionally rather than at the extremum. See **[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]**.

The reference price is the snapshot's `spotOffchain_t`. It must **not** be a pool-derived price — that would make this module depend on a Meteora pool, which §10 forbids.

The repository meaning is:

- Call Wall: the **lowest** strike **strictly above** the reference price at which the running sum of call-side Dollar GEX **magnitude** over above-spot strikes, taken in **ascending** strike order, first reaches `callWallAccumulationFraction` of the above-spot call-side total magnitude
- Put Wall: the **highest** strike **strictly below** the reference price at which the running sum of put-side Dollar GEX **magnitude** over below-spot strikes, taken in **descending** strike order, first reaches the same fraction of the below-spot put-side total magnitude

**Accumulate magnitudes, not signed values.** This is a clarification of [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]'s wording, not a change to its meaning, and it exists to close a sign trap. Put-side Dollar GEX is negative, so both the running sum and the side total are negative, and a naive `runningSum >= fraction * total` is satisfied by the **first** strike visited — an implementation that reads as a threshold test but behaves as "take the nearest strike", which is the failure this whole section replaces. Working in magnitudes makes one comparison correct for both sides.

**The threshold comparison is inclusive (`>=`).** A fraction of 1 therefore selects the outermost eligible strike rather than returning `null`.

**Determinism comes from the strike ordering, not from the tie rule.** The lower-strike tie rule below resolved ties in *concentration*, which is what the superseded extremum rule compared. The accumulation scan is ordered by strike — a total order over a profile holding one row per strike — so no two candidates can contend for the same position, and input row order cannot change the result. The tie rule is retained because ties in concentration still arise when **ranking** candidates for display.

`callWallAccumulationFraction` is declared in `strategy.config.ts`, defaults to `0.8`, and is **UNRATIFIED** on the same terms as `deployWidthSigmaMultiple`: it is a policy choice that no measurement has yet discriminated from its alternatives, and any published wall must carry the fraction that produced it.

**The qualifying set must be non-empty before the fraction is applied.** A side's candidates are the strikes on that side of the reference price carrying **strictly positive** call-side (respectively strictly negative put-side) Dollar GEX. If that set is empty the side's total is zero, and a fraction of zero is reached by the first strike examined — which would return a spurious wall sitting on top of spot, the exact failure this section exists to prevent. An empty qualifying set is `null`, never a strike.

If no valid strike qualifies for one side, that wall output must be `null` rather than guessed — and consumers must treat it as a refusal to deploy, never as an error to suppress or a value to substitute.

**A `null` wall is ambiguous, and the ambiguity must be resolved at this boundary rather than by the consumer.** It has three causes with different meanings, and they are separable from fields the snapshot already carries:

1. **Untrustworthy chain** — `snapshotStale_t = true`. A data fault. It says nothing about the market.
2. **Incomplete chain** — `snapshotStale_t = false` but `regimeLabel_t = 'DEGRADED'` or `locallyDroppedInstrumentCount > 0`. The snapshot is current but built on too little of the chain, per §9.
3. **Exhausted chain** — fresh and complete, and still no qualifying strike. The genuine market state: price has left the observable chain on that side.

The third is **remote, not routine**. Measured 2026-09-27, the listed chain spanned strikes 20–240 against spot 121.53, with 43 qualifying above-spot and 58 below: exhausting it upward requires roughly **+97.5%**, downward roughly **−83.5%**. A `null` wall in ordinary operation is therefore far more likely to be cause 1 or 2 than cause 3, which is why the cause must be published alongside the `null` and never inferred from it. See **[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]**, "Response to a missing wall".

The peak-gamma strike remains a meaningful quantity and does not stop being published — it stops being called a wall. Where a pin level is wanted, publish it under its own name (`callGammaPeak_t` / `putGammaPeak_t`) and never reuse it as a bound.

### 6a. Published provenance and the missing-wall cause

Two facts must travel with the walls, because neither can be reconstructed from them later.

**The accumulation fraction that produced them.** `callWallAccumulationFraction_t` on `SolGexSignalPayload` carries the value actually used. The level is UNRATIFIED, so frames taken under different values are not comparable, and without the field that incomparability is invisible to anything replaying the record.

**Why an absent wall is absent.** `callWallMissingCause_t` and `putWallMissingCause_t` carry one of three values, and are `null` exactly when the wall is present:

| Cause | Meaning |
| --- | --- |
| `SOURCE_STALE` | The snapshot is not trustworthy. A data fault; says nothing about the market. |
| `PROFILE_DEGRADED` | The snapshot is current but built on too little of the chain (§9). |
| `NO_ELIGIBLE_STRIKE` | Fresh and complete, and still no qualifying strike on that side — price has left the observable chain. |

**Precedence is fixed in that order**, most-general first. A stale snapshot may also be degraded and may also have no eligible strike; reporting the innermost cause would state a conclusion about the market derived from data already known to be untrustworthy.

`PROFILE_DEGRADED` is decided by the **drop-tolerance** test, not by `regimeLabel_t`. The label is also `DEGRADED` for a stale snapshot and for non-finite totals, so keying off it would let a staleness fault be reported as an under-built profile and defeat the precedence rule.

**A consumer must never infer the cause from the `null`.** Measured 2026-09-27 the listed chain spanned strikes 20–240 against spot 121.53, so exhausting it needs roughly +97.5% up or −83.5% down: in ordinary operation a `null` wall is far more likely to be cause 1 or 2 than cause 3.

### 6a1. Wall distance is published as a diagnostic, and is not a threshold

`callWallDistancePct_t` and `putWallDistancePct_t` carry spot's distance to each wall as a fraction of spot. They exist so the [[adr-033-fee-yield-measurement-route|ADR-033]] window can record the **post-ADR-038 distribution**, which is the evidence a wall-proximity policy needs and does not have: every distance measured before 2026-09-27 was taken against the superseded global-extremum walls, whose distances were bimodal near 0% and 23%, while the ratified rule produced 21–23% on both sides across all 24 captured frames. A threshold chosen from the old distribution would be calibrated against a rule that no longer exists.

**Nothing in the repository compares these to a threshold, and nothing may.** There is no proximity constant, no armed or triggered state, and no withdrawal behaviour keyed to them. A trigger requires an ADR that does not exist; adding a comparison would be taking that decision by accident. The monitor may display them and must not label, colour, or warn on them.

**Sign convention.** Positive means the wall is on its own side of spot and further away; negative means price has passed it. A negative value is unreachable for a wall selected under this section, because eligibility is strict — it occurs only for historical walls chosen under the superseded rule, where 48.4% of records had price above the call wall.

**`null` means absent, never zero, and this must be explicit rather than arithmetic.** A missing wall or an unusable spot yields `null`. This is not a stylistic preference: JavaScript coerces `null` to `0`, so an inline `(callWall - spot) / spot` on a missing wall evaluates to **`-1`**, and `-1 <= anyThreshold` is **true** — a proximity rule written that way would read a missing call wall as "price is 100% past the wall" and force the exit §6b forbids. The put side coerces to `+1` and reads as maximally safe. One absent input, two opposite wrong answers, neither an error. Consumers must therefore treat `null` as "not measured" and must never substitute a number for it.

### 6b. Response to a missing wall

A `null` wall **blocks a new deployment or a widening** — the planner already refuses with `MISSING_CALL_WALL` / `MISSING_PUT_WALL` — and is **never an exit signal**. It may not close, withdraw, or narrow an existing position, and it may not suspend, resize, or unwind the hedge, whose sizing takes no wall as an input. A fallback bound may never be substituted: not the global extremum, not the outermost listed strike, not a window left open at one end. [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] holds the full reasoning.

Escalation is **asymmetric**. The call side alarms after `missingWallAlarmTicks` consecutive **distinct** snapshots; the put side alarms immediately, because a price below the entire listed chain is a crash rather than an extension. The streak counts distinct source snapshots rather than consumer reads, since consumers poll faster than the source produces frames and counting reads would let one absent wall reach the threshold within a single frame.

The alarm is **observability only** and carries no action. It must not emit an execution intent, and `MISSING_CALL_WALL` / `MISSING_PUT_WALL` must not be mapped to a defensive-withdrawal transition.

Tie handling must be deterministic. Equal candidates must resolve by a fixed rule chosen in code and unit-tested, not by iteration accident.

---

## 7. Zero Gamma Level extraction

Zero Gamma Level must be extracted from the cumulative net GEX profile, not from the local strike profile.

The rule is binding:

- sort strikes ascending
- compute cumulative net GEX across that ordered surface
- find the adjacent strikes where cumulative net GEX crosses zero
- linearly interpolate the exact crossover within that interval

The interpolation domain is therefore the cumulative profile sign crossover, not the local per-strike sign pattern.

If the cumulative profile never crosses zero, `zeroGammaLevel_t` must be `null`.

If the cumulative value is exactly zero at a sampled strike, that strike itself is the Zero Gamma Level.

---

## 8. Threshold consumption and regime classification

This domain consumes:

```text
zeroGammaProximityPctThreshold = 0.0075
```

from `src/config/strategy.config.ts` to classify the `ZERO_GAMMA_PROXIMITY` regime.

`config_contract.md` makes this ownership explicit: the threshold belongs to Q003 intelligence classification, not directly to the Q004 Macro FSM.

The Intelligence Engine therefore owns the classification step that converts geometric proximity to a `regimeLabel_t` carried in `SolGexSignalPayload`.

The macro reducer consumes the already-classified payload and must not redefine this threshold locally.

---

## 9. Staleness handling

If the upstream snapshot is stale, disconnected, or otherwise not fresh enough to support trustworthy analytics, this domain must preserve that fact in its output by setting:

```text
snapshotStale_t = true
```

The intelligence layer may emit a degraded signal under stale conditions, but it must not hide staleness or fabricate freshness by recomputing on old inputs as though they were current.

---

## 10. Data-flow boundary

This domain writes only downstream:

```text
marketdata -> state -> intelligence -> decision
```

It may not:

- open or manage WebSocket transports
- submit transactions or orders
- advance the FSM directly
- read or write another module's private persistence layer outside the declared boundaries

The GEX engine computes and publishes facts. It does not execute.

---

## 11. Prohibitions

- Do not apply option-side sign inside the gamma function, to either gamma source.
- Do not exclude an instrument because it lacks a venue-native gamma; fall back to the local
  computation instead.
- Do not scale, re-sign, or otherwise adjust a venue-native gamma to reconcile it with the
  local computation. If the two disagree, the precedence in §3a settles it.
- Do not alter the Dollar GEX formula or contract multiplier ad hoc.
- Do not derive Zero Gamma Level from the local strike profile.
- Do not classify `ZERO_GAMMA_PROXIMITY` with a hard-coded duplicate threshold outside `strategy.config.ts`.
- Do not suppress `snapshotStale_t` when upstream freshness is not proven.

These prohibitions are binding.
