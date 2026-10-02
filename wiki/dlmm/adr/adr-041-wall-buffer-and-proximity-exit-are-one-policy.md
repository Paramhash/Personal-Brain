---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-041
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/041-wall-buffer-and-proximity-exit-are-one-policy.md
bot_commit: 3f1eec9
source_sha256: ea7dd3ac0c260e3e4fde22f7436efec3540bf0dc23d5456d9a0a627e965bf84a
exported_at: '2026-10-02T12:50:26Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/041-wall-buffer-and-proximity-exit-are-one-policy.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]] — The Wall Buffer and the Wall-Proximity Exit Are One Policy, and Only the Buffer Half Can Be Ratified Today

- **Date:** 2026-09-27
- **Status:** **Active. Ratified by the dispatcher 2026-09-27.** Drafted under TICKET S, which reserved ratification as a separate dispatcher act; this is that act.
- **Ratification is partial by design, and the split is the decision.** In force: the structure, the equations, the failure behaviour, the recording obligations, **`m = 0.3%`**, **`k = 0.25`**, and the **relative parameterisation of §2a** — not the multiplicative form TICKET S's scope text used. **Not in force: `t`.** The proximity threshold is deferred, so the wall-proximity exit is **not authorised and must not be built**.
- **What this unblocks, and what it does not.** `DRAFT_TICKET_R_Implement_The_Ratified_Wall_Buffer.md` is cleared **for the buffer only**. Its withdrawal-trigger half remains blocked on `t`, so R's scope needs trimming before staging rather than being read as fully unblocked.
- **`k = 0.25` is ratified as policy and is NOT calibrated.** Those are different statuses and conflating them is the failure this line exists to prevent. It is the value in force, chosen deliberately, and no measurement supports it over 0.20 or 0.30. It must never be described as calibrated or optimised, and §10's revisit trigger applies to it.
- **Ratifying this ADR enabled no runtime behaviour by itself.** No constant was added to `strategy.config.ts` and no code changed; implementation is TICKET R's, within the limits above.
- **Depends on:** [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] and its implementation (TICKET Q, verified in source and changelog on 2026-09-27); [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] and its derived window (TICKET O); [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] and [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] for the cost of a cycle; the `callWallDistancePct_t` / `putWallDistancePct_t` measurement fields.
- **Nothing in this ADR is calibrated.** The held post-ADR-038 evidence is 24 frames over 9.5 minutes with near-constant spot. It cannot distinguish a proximity threshold anywhere between 2% and 20%. Every number below is either a measurement of something else, or a policy choice labelled as one.

---

## 1. The decision, stated once

A wall buffer and a wall-proximity exit are **one policy evaluated at two moments**: the buffer refuses to *open* a position near a wall, and the trigger *closes* one that drifts near a wall. Ratifying them separately allows a position to be opened inside the band that immediately closes it.

**Ratified:** the structure, the equations, the failure behaviour, the parameter *relationship*, and the recording obligations.

**Deferred:** the proximity threshold `t`. The exit behaviour is **absent, not disabled** — there is no trigger to switch on, and that is deliberate: a present-but-disabled exit is a flag someone can flip, which is the argument `observation_archive.md` §3 rule 1 already makes about the signer.

**Chosen as a labelled policy default:** the buffer parameter `k`, because its failure mode is refusal — which costs no capital — where the trigger's failure mode spends it.

---

## 2. Ratified parameterisation: a fraction of the **room**, not of the wall price

TICKET S's scope states the buffer multiplicatively, and that form is recorded here because the entry/exit inequality was derived from it:

```text
bufferedPutWall  = putWall  * (1 + b)
bufferedCallWall = callWall * (1 - b)
```

At the buffered boundary the implied minimum distances are **not** `b`, and the **put side binds**:

| `b` | put-side `b/(1+b)` | call-side `b/(1-b)` | binding |
| --- | --- | --- | --- |
| 0.05 | 0.04762 | 0.05263 | put |
| 0.10 | 0.09091 | 0.11111 | put |
| 0.15 | 0.13043 | 0.17647 | put |

Verified to five decimal places against a direct computation. So the entry/exit condition in this form is `b/(1+b) > t + m`, which is materially stricter than the intuitive `t <= b` — at `b = 0.10` it caps `t` at 9.09%.

**The multiplicative form is recorded but is NOT the ratified one**, for a reason that is structural rather than aesthetic. Its ceiling is surface-dependent:

```text
b_max = callDistancePct / (1 + callDistancePct)
```

Verified: a measured call distance of 0.2343 gives `b_max = 0.18982` against a directly measured 0.18983. Consequently:

| Observed call distance | `b_max` before spot leaves the buffered envelope |
| --- | --- |
| 5% | 4.76% |
| 10% | 9.09% |
| **23.4% (measured)** | **18.96%** |
| 40% | 28.57% |

**A `b` ratified as an absolute fraction therefore blocks every deployment whenever the walls tighten.** At `b = 0.15`, any surface whose call wall sits inside ~17.6% admits no position at all — and the pre-ADR-038 series had the call wall inside 1% of spot for 48.4% of records. [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] makes that regime unreachable today, but nothing measures whether the accumulation wall *stays* 23% out; that is F-021, still open.

### 2a. The ratified form

Parameterise by the fraction `k` of the available room surrendered on each side:

```text
bufferedCallWall = spotOffchain_t + (callWallStrike_t - spotOffchain_t) * (1 - k)
bufferedPutWall  = spotOffchain_t - (spotOffchain_t - putWallStrike_t) * (1 - k)
```

**Two properties make this the ratified form.**

**Inversion and spot-exclusion become structurally impossible for every `k` in `[0, 1)`.** Under [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] a non-null call wall is strictly above spot and a non-null put wall strictly below, so `bufferedCallWall > spotOffchain_t > bufferedPutWall` holds by construction. Verified across `k` from 0.10 to 0.99: spot remained inside at every value, where the multiplicative form excluded spot at every `b >= 0.25` on the same surface. **Two of the four refusal paths the scope asks to specify simply cease to exist**, and cannot be reintroduced by a badly chosen parameter.

**It self-scales.** The buffer is defined relative to the room actually available, so it tightens and loosens with the wall spread instead of blocking deployment when the spread narrows.

**The code identifier is `wallBufferRoomFraction`**, declared in `src/config/strategy.config.ts` when TICKET R implements it. Named here so the ADR is the single authority: the identifier must not be `wallBufferFraction`, which was TICKET S's name for the **absolute** multiplicative inset that §2b records as not in force. Two names for two different rules is how the wrong one gets implemented.

The minimum distances at the buffered boundary are, exactly:

```text
minCallDistance = k * d_call / (1 + d_call * (1 - k))
minPutDistance  = k * d_put  / (1 - d_put  * (1 - k))
```

where `d_call` and `d_put` are the observed distances. Verified at `k = 0.25` on the measured surface: 0.04982 and 0.06525 against directly computed values. Note the asymmetry **reverses** — here the **call side binds**, where the multiplicative form binds on the put side. The entry/exit condition in this form is therefore:

```text
k * d_call / (1 + d_call * (1 - k)) > t + m
```

which self-scales on both sides: as the walls tighten, the standoff and the threshold ceiling shrink together.

### 2b. The multiplicative form is retained for the record only

It is **not** in force. Kept because TICKET S's scope text and the earlier reviews are written in its terms, so a reader arriving from either needs the conversion — and because its ceiling is the evidence that decided the parameterisation.

Recorded so that it cannot be reintroduced casually: were it ever adopted, it would additionally require ratifying the behaviour when `b` exceeds `b_max`, which must be an **explicit refusal** through the existing taxonomy — inverted bounds or `ENVELOPE_BELOW_MIN_BINS` — and **never a silent clamp of `b`**. A clamped buffer becomes a different policy in exactly the regime the buffer exists to protect against, and does so without saying it has. The ratified form needs no such rule, because it cannot reach that state.

---

## 3. The basis margin `m`, and why rounding is not part of it

The planner scales USD walls into pool units (`rangePlanner.ts:401-403`) while the distances are measured against off-chain spot, so the two differ by the pool/spot basis. Measured:

| Dataset | n | Median | Largest magnitude |
| --- | --- | --- | --- |
| 24-frame [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] capture | 24 | −0.1740% | **0.2218%** |
| 1336 recon records | 1336 | −0.1729% | **0.2777%** |

Consistently negative and small — the pool priced about 0.17% below spot at the median — and never beyond **0.28%**. **Ratified: `m = 0.3%`**, which covers all held evidence with a small margin. This is a measurement-backed choice, unlike `t`.

**Inward rounding contributes favourably and must not be counted into `m`.** `rangePlanner.ts:414-415` rounds the lower bound up and the upper bound down, so the envelope **shrinks**; a narrower envelope makes the active-bin containment test *stricter*, and any accepted position sits further inside the buffered envelope than the unrounded algebra implies. The term is bounded by one bin — 0.04% at the pool's 4 bps step — and it is a margin, not a leak. Double-counting it would overstate the required standoff.

The post-conversion check still stands: the implementation must verify on the **same snapshot**, after scaling and rounding, that no position accepted for deployment is already trigger-eligible. The algebra is the reason to expect that check to pass, not a substitute for it.

---

## 4. Ratified: `t` is deferred, and the exit is absent

**The threshold cannot be chosen from anything held.** Measured with the shipped extractors over the capture:

| Side | Min | Median | Max |
| --- | --- | --- | --- |
| `callWallDistancePct_t` | 23.31% | 23.43% | 23.49% |
| `putWallDistancePct_t` | 21.79% | 21.83% | 21.91% |

| Threshold | 2% | 5% | **10%** | 15% | 20% | 25% |
| --- | --- | --- | --- | --- | --- | --- |
| Frames triggering | 0/24 | 0/24 | **0/24** | 0/24 | 0/24 | 24/24 |

Every value from 2% to 20% fires on nothing; 25% fires on everything. **10% is not merely uncalibrated — on all post-Q evidence it is inert.** The pre-Q figure, where 10% fired on 60.4% of 1336 ticks, was measured against the superseded global-extremum walls and is not evidence about this rule: the distribution did not shift, it changed shape, because the side constraint removed the near mode entirely.

**The 9.5-minute capture is not a sample of a larger post-Q dataset; it is the entire one.** No other retained data carries a candidate strike surface, so [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] walls cannot be recomputed from the 1336-record series at all.

**The cost asymmetry decides the recommendation.** The cost of a *false* trigger is measured: each cycle is a full close and reopen, committing per [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]/[[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] —

| Deployed width | Recoverable | Permanently sunk (virgin arrays) |
| --- | --- | --- |
| 203 bins (σ-derived, in force today) | 0.1741 SOL | **0.2958 SOL** |
| 1142 bins (full [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] envelope) | 0.9770 SOL | **1.2145 SOL** |

and a wall-proximity exit moves the range by construction, so it is exactly the cycle that touches virgin arrays. The cost of a *missed* trigger — what actually happens when price leaves a deployed range — is **entirely unmeasured, because no capital has ever deployed.**

**Choosing a number when one failure mode is quantified and the other is not would be picking the risk we can see over the one we cannot.** **`t` is therefore deferred, the exit behaviour remains absent rather than present-and-disabled, and TICKET R stays blocked on `t` alone.**

Deferral is bounded, not open-ended: if the buffer is ratified, the inequality in §2a already caps `t` above, so the eventual decision is a choice within a stated interval rather than a free parameter.

---

## 5. Ratified: `k = 0.25`, as a labelled policy default and not a calibration

**Chosen, not measured.** On the observed surface `k = 0.25` gives a minimum standoff of **4.98%** on the call side and 6.53% on the put side while leaving 75% of the available room deployable, and it cannot invert or exclude spot at any wall spread.

Why a value can be chosen here when `t` cannot: **the buffer's failure mode is refusal.** Too large a `k` forgoes yield; too small a `k` permits a deployment nearer a wall than intended. Neither spends capital, and the first is recoverable by changing the number. The trigger's failure mode spends 0.2958–1.2145 SOL per occurrence.

It is explicitly **not** an optimum, and no measurement supports 0.25 over 0.20 or 0.30.

---

## 6. Trigger semantics, for whenever `t` is ratified

Specified now so the deferred decision is a number rather than a design.

- **Either side is sufficient.** A position is exposed if it is near *either* bound.
- **Equality triggers** — `distance <= t` — for deterministic boundary behaviour.
- **Only while a reconciled active position exists.** Guarded on the position fact, as the EV branch already is (`macroStateMachine.ts:397`).
- **Persistence over distinct fresh snapshots**, counted in the wall rule's **own state**. It must **not** reuse `consecutiveThreatSnapshots` (`:313-317`), which increments on `threatQualified` — hardcoded to `regimeLabel_t === 'ZERO_GAMMA_PROXIMITY'` (`:310`). Redefining that predicate as a disjunction corrupts the counter: with `threatPersistenceSnapshots = 2`, one ZGL-proximity snapshot followed by one wall-proximity snapshot satisfies persistence **though neither condition persisted**. Copy the qualify-dwell-act pattern; do not share the counter.
- **Precedence is ratified for attribution, not exclusivity.** One intent per entry is already structural: the reducer assigns a single `nextState` and emits `intent` only on entry to `DEFENSIVE_WITHDRAWAL` (`:578-581`), so simultaneous conditions resolve to exactly one `WITHDRAW` and one operational job. TICKET R must not build mutual exclusion that exists. What precedence determines is the `reason` string — the only record of *why* a position closed, and the field an operator reads first. A wall exit misattributed to `ev_gate_failed_while_deployed` sends a future diagnosis in the wrong direction. Proposed order: degraded input, negative GEX, hard ZGL cross, **wall proximity**, ZGL threat, EV failure.
- **It requests the existing full-withdraw path.** No wing-only mutation; that needs its own actuator design.

### 6a. The distance must be read, never re-derived

**Binding implementation constraint.** The trigger consumes `callWallDistancePct_t` / `putWallDistancePct_t`, or `wallDistancePct` directly. It **may not** inline the subtraction.

JavaScript coerces `null` to `0`, so on a missing call wall the inline expression `(callWallStrike_t - spotOffchain_t) / spotOffchain_t` evaluates to **`-1`** — not `NaN` — and `-1 <= t` is **`true`** for every positive `t`. A trigger written inline would read a missing call wall as "price is 100% past the wall" and **fire a withdrawal**, which is precisely what [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] §6b forbids. The put side coerces to `+1` and reads as maximally safe. One absent input, two opposite wrong answers, neither raising an error. Pinned by test `P63` in `gexProfile.test.ts`, recorded in `gex_intelligence.md` §6a1.

---

## 7. Re-arm

A re-arm rule separate from `t` is required, and **it cannot be calibrated either**. The post-Q wall-switch frequency is not merely unmeasured but **not yet measurable**: zero flips were observed across the 24 frames, but with 23 transitions over 9.5 minutes the rule of three supports only **<= 18.95 flips/h** at ~95% confidence, and the superseded rule's measured **0.81 flips/h** sits comfortably inside that bound. This window would not have detected the old oscillation either.

Proposed structure, with the numbers deferred alongside `t`: re-arm requires **both** distances to clear a separate, wider clearance threshold for a stated count of distinct fresh snapshots after a completed redeployment. The state must survive the withdraw-to-redeploy handoff and be reconstructible from recorded decisions.

**The EV gate is the economic backstop and the re-arm rule should not duplicate it.** [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] puts sunk rent inside `net_ev`, so an uneconomic redeploy is refused on its own terms. Two consequences worth recording: the re-arm rule need not encode cost policy, and a permissive re-arm does not merely cost fees — each virgin-array cycle consumes sunk capital that never returns, so it can leave the strategy unable to redeploy at all.

---

## 8. Missing walls — [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] §6b is preserved without exception

- A missing wall blocks a new deployment or widening, and is recorded with its discriminated cause.
- A missing wall is **never** an exit signal. It may not close, withdraw, narrow or otherwise mutate an existing position, and may not suspend, resize or unwind the hedge.
- A missing wall yields a `null` distance, which is an absent measurement — never zero, never maximum danger, and never satisfying a `<=` comparison.
- Missing-wall escalation stays observability-only. `missingWallAlarmTicks` may not be repurposed as a proximity threshold.

This is already enforced rather than asserted: every alarm carries the fixed guidance `BLOCKS_NEW_DEPLOYMENT_ONLY_NOT_AN_EXIT_SIGNAL`, and a test asserts the alarm object exposes no action, intent or side-effect field. Neither this ADR nor TICKET R may weaken that.

---

## 9. What must be recorded, so the deferred values can eventually be chosen

Already published by TICKET Q and the diagnostics increment: `callWallDistancePct_t`, `putWallDistancePct_t`, `callWallAccumulationFraction_t`, both missing-wall causes, and their recon-record equivalents.

Still required before `t` can be ratified:

1. **The distance distribution across a real price move** — the [[adr-033-fee-yield-measurement-route|ADR-033]] window is the first dataset able to supply it.
2. **The post-Q wall-switch frequency**, which needs a window long enough to distinguish it from the ≤18.95/h bound this capture supports.
3. **Whether the accumulation wall stays ~23% from spot**, or tightens. F-021's open question, and the one that decides whether an absolute `b` is viable at all.

## 10. Revisit trigger

This ADR expires as a basis for action when any of the following becomes true, and must be revisited rather than silently inherited:

- **30 consecutive days** of post-ADR-038 distance data exist at ≥95% coverage; or
- the observed **call-wall distance falls below 10%** on any day's median, which would put `b_max` near the proposed standoff and make the buffer the binding deployment constraint; or
- the measured **wall-switch frequency exceeds 0.5/h**, which would make re-arm the dominant design concern rather than the threshold; or
- **capital is authorised**, at which point the unmeasured cost of a missed trigger stops being hypothetical.

A policy default with no stated expiry is how an UNRATIFIED value quietly becomes the design.

---

## 11. Consequences, and what ratification would and would not do

**Ratification enabled no behaviour by itself.** It authorised a shape, one measured margin (`m = 0.3%`), and one labelled default (`k = 0.25`). No constant entered `strategy.config.ts` and no code changed. TICKET R is cleared for the buffer and stays blocked on `t`.

**The buffer alone is a coherent, useful increment.** With the exit deferred, `k` gives a "do not deploy right next to a wall" rule whose worst outcome is a refused deployment. The entry/exit consistency check becomes vacuous while no trigger exists, and must be added with the trigger, not before.

**It does not resolve F-021.** Wall stability across a real move remains unmeasured, and both parameters depend on it.

**Recorded cost of the recommendation.** Choosing the relative parameterisation means the buffer is no longer expressible as a single inset on a wall price, so anyone comparing it to the multiplicative literature — or to TICKET S's own scope text — must convert. That is a real readability cost, accepted because the multiplicative form can silently block all deployment and this one cannot.

## 12. Alternatives rejected

- **Ratify 10% now as a policy default.** It fires on 0/24 frames of all post-Q evidence, so it would ship a trigger that does nothing while appearing to be a safety control — the worst of both, because it invites reliance on protection that is not there.
- **Defer both parameters.** Defensible, and rejected only because `k`'s failure mode is refusal. Deferring it forgoes a free safety improvement while waiting for data that only bears on `t`.
- **Infer `t` from the pre-Q 60.4% rate.** That rate describes the superseded wall rule. Using it would calibrate against a definition [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] removed.
- **Set `t = b` (or `t <= b`).** The derived condition is `b/(1+b) > t + m`, which is strictly tighter. `t = b` admits positions eligible for withdrawal on the tick they open.
- **Treat the buffer as a width control.** Measured: σ remains binding until `b ≈ 0.1848` while spot exits at `b ≈ 0.1898`, a 0.005-wide interval. The buffer is an entry gate; presenting it as a knob that continuously tightens the deployed window would misdescribe it.
