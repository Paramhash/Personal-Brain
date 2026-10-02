---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-038
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/038-gex-walls-are-selected-on-the-correct-side-of-spot.md
bot_commit: 3f1eec9
source_sha256: bcc17c22e2b23bd49866d9506dd7af1bbf2162c36e206c24624231807e67d2ce
exported_at: '2026-10-02T12:50:26Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/038-gex-walls-are-selected-on-the-correct-side-of-spot.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] — A GEX Wall Is Selected **on Its Own Side of Spot**, by Gamma Accumulation Rather Than by Extremum

- **Date:** 2026-09-27
- **Status:** **Active. Ratified by the dispatcher 2026-09-27.** **ADR-037 is reserved for TICKET I's promotion boundary** (deferred, `todo/deferred.md`); this is 038 to avoid a collision.
- **Read the Decision field, not the draft history.** This ADR was drafted proposing a *constrained extremum*, and the evidence gathered to ratify it **overturned that rule** while confirming the diagnosis behind it. The Decision below states what was ratified. The superseded proposal is retained under "Alternatives rejected" with the evidence that killed it, because the reasoning is the useful part; it is **not** what to implement.
- **One quantity remains UNRATIFIED:** the 80% accumulation threshold. See "The unratified threshold".
- **Amends:** `gex_intelligence.md` §6. Consequential for `range_planning.md` §2 and §2b ([[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]), which consume the walls as an envelope.
- **Supersedes in part:** the framing of **F-021**, which asked for temporal wall stability. See "What this does to F-021".

- **Context:** `gex_intelligence.md` §6 defines the Call Wall as "the strike carrying the strongest positive call-side concentration under the module's declared wall-selection rule", and the Put Wall as the strongest negative put-side concentration. `extractCallWall` and `extractPutWall` implement exactly that: a scan over **every** strike for the extremum on each side, ties to the lower strike. `range_planning.md` §2 then uses the pair as an **envelope the deployed range may not leave**, which requires both to be bounds — the call wall above price, the put wall below it. **They are not.** Measured over 1336 recorded decisions on 2026-09-27 (`C:\observation\recon-sim-2026-09-27\`, pool price range 120.13–121.73): the pool price sat **above the call wall in 481 records (36.0%)** and **below the put wall in 0 (0.0%)**. Every one of those 481 is an `ACTIVE_BIN_OUT_OF_RANGE` rejection under §2b step 3 — the planner correctly refusing to propose a range price has already left — so for roughly a third of the observed period **the strategy could not deploy at all**. The distances explain the asymmetry and show it is structural rather than a property of this market: the call wall sat a median of **+0.20%** from the pool price (0.36% absolute) while the put wall sat a median of **14.98%** below it, a **42× asymmetry**; only two strikes ever won each side (call ∈ {121, 150}, put ∈ {103, 120}). **Option gamma is maximised at the money.** A wall defined as the peak-gamma strike on its side will therefore sit wherever spot is, and the call wall tracking spot to within a third of a percent is what that definition produces, not a failure to implement it. The selection is not noisy either: in a live frame the winning strike led by a **43.5% margin over 87 candidates** — it wins decisively, *because that is where spot is*. The put side escapes only by accident: put open interest clusters well below spot as downside protection, so the put-side gamma peak is displaced downward by a real positional fact, and that displacement is the only reason the put wall functions as a lower bound. A peak-gamma strike is a **pin or magnet level** — where dealer hedging tends to attract price — which is close to the opposite of a ceiling. Full evidence: **F-024**.

- **Decision (ratified):** **Each wall is selected from its own side of the reference price, by gamma accumulation.** The **Call Wall** is the lowest strike **strictly above** the reference price at which the running sum of call-side Dollar GEX over above-spot strikes, taken in ascending strike order, first reaches **80% of the above-spot call-side total**. The **Put Wall** is the mirror: the highest strike **strictly below** the reference price at which the running sum of put-side Dollar GEX over below-spot strikes, taken in *descending* strike order, first reaches 80% of the below-spot put-side total. **Two properties make this the ratified rule rather than the extremum.** It is *distributional*, so a single thin far strike cannot move it the way "the furthest strike carrying ≥10% of the maximum" can; and it returns **a strike that exists**, which a gamma-weighted centroid does not — `gex_intelligence.md` §3's determinism discipline prefers the former, and the centroid was the only rule observed to wander (15 distinct values across 24 frames where every strike-returning rule was constant). Ties remain resolved to the lower strike, deterministically, as §6 already requires. When no qualifying strike exists on a side, that wall is `null` and the planner rejects — §6's existing "`null` rather than guessed" rule is unchanged and becomes the honest report of "price is outside the observable chain on this side". **The reference price is the snapshot's `spotOffchain_t`**, not the pool's active-bin price: §6 is a market-data question answered from the option chain, and the walls must be defined before `range_planning.md` §2a scales them into pool units — using the pool price here would make the GEX signal depend on a Meteora pool, which `gex_intelligence.md` §10's data-flow boundary forbids. The change is confined to `extractCallWall` / `extractPutWall` and their §6 contract text; **the Dollar GEX formula (§4), the profile construction (§5), the gamma source precedence (§3a) and the Zero Gamma Level (§7) are untouched.** The peak-gamma strike does not stop being interesting — it stops being called a *wall*. Where a pin level is wanted it should be published under its own name (`callGammaPeak_t` / `putGammaPeak_t`) rather than reused as a bound.

- **Consequences:** **On the recorded data this change is decisive rather than marginal.** In all 1336 records the pool price was below 150, and 150 was the standing call-side runner-up, so a side-constrained selection would have chosen a strike above spot in **1336 of 1336 records (100%)** — the envelope would have bracketed spot in every one, and all 481 rejections would not have occurred. That figure was **inferred, not measured** — the recorded decisions store the selected wall, not the candidate surface — and it has since been **confirmed against the full candidate profile** in a 24-frame live capture: under the old global rule the call wall sat above spot in **0 of 24 frames**, and under every side-constrained rule in **24 of 24**, with 43 above-spot candidates available in every frame. The inference held. What the capture also showed is that a side-constrained *extremum* brackets spot without producing a usable bound, which is why the ratified rule is the accumulation rule and not the one this paragraph was drafted around; the widening described below refers to the ratified rule. Four further consequences. First, **the envelope widens substantially** — from a median 402 bins to roughly the 103–150 span — which moves [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s clamp firmly into the σ-binding regime and makes `deployWidthSigmaMultiple` the operative lever it was designed to be; ratifying that multiple via `observation_archive.md` §6 question 3 becomes worth doing, where under the current definition it was close to inert. Second, **a wider envelope touches more bin arrays**, so [[adr-030-deployment-sol-reserve|ADR-030]]'s already-breached `0.25 SOL` reserve moves further out of range: §2b computes 3 uninitialized arrays at `0.2577 SOL`, and this change makes the reserve question more urgent rather than less. Third, **a `null` wall becomes reachable in normal operation** — if price runs above the highest listed call strike there is no qualifying strike, where the old rule would always have found *something*. That is the correct report, but it means `MISSING_CALL_WALL` is now an expected operational state needing a stated response, not a data fault. Fourth, this is a **signal-definition change, so every historical wall series is computed under the old rule** and is not comparable across the change; any analysis spanning it must say so, exactly as the `configDigest` change was recorded.

- **Response to a missing wall (`MISSING_CALL_WALL` / `MISSING_PUT_WALL`), stated 2026-09-27:** ratifying this ADR required stating one, because the old global rule always found *something* and the new rule can decline. **First, discriminate the cause** — §6 requires the cause be published alongside the `null`, because the three causes are (1) an untrustworthy chain (`snapshotStale_t`), (2) an incomplete one (`regimeLabel_t = 'DEGRADED'` or `locallyDroppedInstrumentCount > 0`), and (3) a genuinely exhausted chain. **Cause 3 is remote:** the chain measured on 2026-09-27 spanned strikes 20–240 against spot 121.53, so exhausting it needs about **+97.5%** up or **−83.5%** down. A `null` wall in ordinary operation is therefore **most likely a data fault, not a market state**, and this ADR's earlier characterisation of it as a routine operational state was wrong. Then, **the same five rules apply to all three causes**, because the planner's job is identical whether the bound is unknown or absent:
  1. **Do not deploy and do not widen.** A range without an upper bound is not a range.
  2. **Never substitute a fallback bound.** Not the global extremum, not the highest listed strike, not a σ-derived window left open at the top. A fabricated bound is precisely the silent failure this ADR removed — it converts a visible refusal into an invisible bad plan, and F-024 is the record of how long that goes unnoticed.
  3. **Absence of a plan is not an exit signal.** An existing position must **not** be closed, withdrawn, or narrowed in response. The planner authorises openings and widenings; it has no withdrawal mandate, and letting a `null` wall trigger one would turn a stale option chain into a capital action.
  4. **The hedge continues, unchanged in mechanism.** Hedge sizing is a function of measured inventory and must never take a wall as an input, so a `null` wall may not suspend, resize, or unwind it. If cause 3 ever does occur, the position is at or through its upper bound and inventory has shifted hard — the moment hedging matters most is the moment this state appears.
  5. **Record it; do not merely log it.** Every tick with a `null` wall must produce a recorded decision carrying both the rejection and the discriminated cause, so the window can measure frequency and cause mix. This mirrors `observation_archive.md` §7 rule 2: a silently absent record is forbidden, and absence must be accounted for.

  **Escalation is gated on persistence for the call side and on occurrence for the put side.** A single-tick `null` is noise; a sustained one means the strategy is out of the market and someone must know. The call side alarms after `missingWallAlarmTicks` consecutive ticks — default `10`, **UNRATIFIED**, because no measurement of the duration distribution exists. The put side alarms **immediately**: mechanically it is the mirror, but a price below the entire listed chain is a crash rather than an extension, and the asymmetry in consequence outweighs the symmetry in derivation.

- **The unratified threshold:** the **80%** accumulation level is a policy choice, not a measurement, and is ratified **only** as a default. It must be declared in `strategy.config.ts` as `callWallAccumulationFraction` (default `0.8`), labelled **UNRATIFIED** in the same terms as `deployWidthSigmaMultiple`, and carried into any published signal so a reader can tell which threshold produced a wall. The 24-frame capture **cannot** distinguish 80% from the two competing rules' 10% and +2% parameters: all three selected strike 150 in all 24 frames. Anything that reads a wall must therefore treat the level as provisional. Ratifying the threshold needs data spanning a real price move, which the [[adr-033-fee-yield-measurement-route|ADR-033]] window will supply under this definition — see "Limits of this evidence".

- **What this does to F-021:** F-021 recorded the call wall oscillating 150 ↔ 121 and asked for hysteresis, dwell or a tie-margin rule. **That framing is superseded.** The oscillation is real, but it is between a **near-ATM pin (121)** and a **far-OTM strike (150)** — two different kinds of level — so a hysteresis rule would have stabilised the answer to the wrong question. Under this ADR the 121 candidate is simply ineligible whenever price is above it, which was **67.7%** of recorded ticks, and the oscillation largely disappears as a side effect rather than being suppressed. F-021's stability question is **not** closed by this: a genuine contest between two strikes on the correct side of spot remains possible, and whether that needs hysteresis is a separate decision that should be taken **after** this change, against data produced under the new definition. The monitor's `CONTESTED` diagnostic stays display-only and unratified in the meantime.

- **Alternatives rejected:** **The constrained extremum — this ADR's own original proposal** — select the strike above spot with the greatest call-side Dollar GEX. Rejected on the evidence gathered to ratify it: because gamma decays from the money, the nearest above-spot strike inherits most of it, so the rule selected **122 (+0.39% from spot) in all 24 frames** while only 18.9% of above-spot gamma lay within +1% of spot. It fixes bracketing (24/24) without producing a bound, and would convert a **visible 36% rejection rate into a silent 100% acceptance of plans placed almost entirely below current price**. A rejection stops capital; a lopsided plan does not. **Keep the global extremum and accept the rejections** — the status quo, and rejected because it means the strategy cannot deploy in roughly a third of observed conditions while the signal reports a healthy, decisive wall; the failure is silent at the signal layer and only visible as a planner rejection two domains downstream. **Add temporal hysteresis to the existing definition (F-021's proposal)** — rejected as treating the symptom: it would stabilise the choice between a pin and a resistance level without making either a bound, and a stabilised wrong bound is worse than an unstable one because it invites confidence. **Use a gamma-weighted centroid of above-spot strikes** — more robust to a single thin strike than an extremum, and rejected for now only because it changes the quantity from "a strike that exists" to "a computed level between strikes", which §3's determinism discipline and the bin conversion both prefer to avoid; worth revisiting if the constrained extremum proves noisy under replay. **Accept that GEX bounds only the downside and derive the upper bound elsewhere** — e.g. from volatility alone, or from liquidity structure. This is the most honest alternative and is **not** foreclosed: if replay shows the constrained call wall is unstable or frequently `null`, this becomes the leading option, and [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s σ-derived width already supplies a mechanism that needs no upper wall. It is rejected *for now* because it discards information the chain does contain, and the cheaper change has not yet been tried. **Define the wall as peak gamma but clamp it to be above spot** — rejected as the worst of both: it reports a strike that did not win its own selection, so the published number would be neither the gamma peak nor the extremum above spot, and no reader could tell which question it answered.

- **Ratification prerequisites, all three discharged 2026-09-27:** (1) **confirmation against a full strike profile** rather than the recorded two-strike set — discharged by the 24-frame capture, which both confirmed the bracketing inference and overturned this ADR's original rule; (2) a stated **missing-wall response** — discharged above, and it also corrected the premise, since a `null` wall is most often a data fault rather than the reachable market state this ADR assumed; (3) acknowledgement that **[[adr-030-deployment-sol-reserve|ADR-030]]'s reserve** moves further out of range — acknowledged, and it remains an open question routed to its own ADR as [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] requires. It is **not** resolved by this ratification and is not made less urgent by it.

---

## Replay result, 2026-09-27 — the inference holds, the *expected effect* does not

The ratification blocker above required confirming the bracketing inference against a full strike profile
rather than a two-strike candidate set. That was done against live profiles from TICKET P's monitor.
**Bracketing is confirmed. The consequence stated in this ADR is wrong, and is corrected here.**

### What the full surface shows

One representative frame, spot 121.52, 101 strikes:

- **43 call-side candidates above spot**, 58 put-side below. The constrained rule is **not fragile** — it
  has ample choice, and the two-strike worry is resolved. Bracketing held in every frame examined.
- But the constrained extremum selects **122 — only +0.39% above spot.** Strike 122 carries 636,560 of
  call-side Dollar GEX against 150's 560,568.

**Gamma decays from the money, so the nearest above-spot strike tends to carry the most of it.**
Constraining the search to "above spot" therefore moves the wall from *at* the money to *just* above it.
It removes the rejection without producing a bound: only **18.9%** of above-spot call gamma lies within
+1% of spot, yet that is where the extremum lands.

### Why that is arguably worse than the status quo

Under this ADR as drafted, the envelope would become roughly 103–122: about **412 bins below spot and 11
above**. §2b then centres a 203-bin window on the active bin and shifts it inward to stay inside, so the
deployed window ends up almost entirely below current price — the lopsided placement already observed
live (200 bins below, 2 above).

So the change would convert **a visible 36% rejection rate into a silent 100% acceptance of badly
placed plans.** A rejection is legible and stops capital; a lopsided plan is neither. **On this evidence
the ADR as drafted must not be ratified.**

### Four rules compared on the same surface

| rule | selected | distance from spot |
| --- | --- | --- |
| constrained extremum (**this ADR as drafted**) | 122 | **+0.39%** |
| gamma-weighted centroid of above-spot strikes | 135.3 | +11.3% |
| furthest above-spot strike carrying ≥10% of the above-spot max | **150** | **+23.4%** |
| extremum excluding strikes within +2% of spot | **150** | **+23.4%** |
| strike below which 80% of above-spot gamma accumulates | **150** | **+23.4%** |

**Three independent rules converge on 150, and only the constrained extremum disagrees.** 150 is a clear
secondary peak — the round-number strike where open interest clusters — and is what a reader would call
resistance. 122 is the at-the-money pin bleeding into the above-spot set.

### Revised decision, and what is still open

The **side constraint is necessary but not sufficient**. It is retained: a wall below spot cannot bound a
range from above, and that part of the diagnosis stands. What must change is the *selection among the
remaining candidates* — an extremum picks the ATM shoulder, and the rule needs to find the **dominant
cluster** instead.

The three convergent rules above are the candidates, and choosing between them is **not** something this
ADR should settle on one frame. The gamma-weighted centroid has the property §3's determinism discipline
dislikes — it returns a level between strikes rather than a strike that exists — while the other two
return a real strike and differ mainly in how they express "material". A short capture across changing
spot is running to test whether the convergence on 150 is stable or an artefact of one moment; **that
result is the remaining ratification blocker**, and it replaces the one this section discharged.

### Process note

This is the ratification blocker doing its job. The ADR was drafted from a two-strike inference, clearly
labelled as inferred, with replay named as a precondition — and replay overturned the expected effect
while confirming the mechanism. The 100%-bracketing figure was correct and would have been deeply
misleading on its own.

---

## Capture result, 2026-09-27 — 24 frames, and the status quo fails every one

The remaining blocker was whether the three rules' convergence on 150 was stable or a momentary artefact.
Captured from the live monitor at 25 s intervals over ten minutes; 101 strikes in every frame; spot
121.4676-121.6494. **The capture ran to completion at 24 frames and every figure below is the final one** --
the interim analysis at 14 frames gave identical results, which is itself weak evidence of stability.

### Rule stability

| rule | selected across 14 frames | distance above spot (min / median / max) |
| --- | --- | --- |
| constrained extremum (**this ADR as drafted**) | **122**, every frame | +0.29 / **+0.39** / +0.44% |
| gamma-weighted centroid | 135.05–135.37, 15 distinct values | +11.01 / +11.30 / +11.45% |
| furthest strike ≥10% of max | **150**, every frame | +23.31 / **+23.43** / +23.49% |
| extremum beyond +2% of spot | **150**, every frame | +23.31 / +23.43 / +23.49% |
| 80% cumulative above-spot gamma | **150**, every frame | +23.31 / +23.43 / +23.49% |

**The three rules agreed in 24 of 24 frames.** The convergence on 150 is not an artefact of one moment.

### Bracketing

| rule | call wall above spot |
| --- | --- |
| every side-constrained rule above | **24 / 24** |
| **global extremum — the current code** | **0 / 24** |

**The status quo bracketed spot in none of the 24 frames.** That is a sharper statement of the problem
than the historical 36%: in the conditions observed here the current definition fails continuously, and
the 36% figure was an average over a period that included regimes where it happened to work.

### Two further observations

**The constrained rule is not fragile: 43 above-spot candidates in every frame**, never fewer. The
two-strike worry that prompted this blocker is fully resolved.

**The three strike-returning rules are perfectly stable; the centroid is not.** 150 was selected
identically every time, while the centroid moved across 15 distinct values — because it is a continuous
function of the gamma surface rather than a snap to an existing strike. That is precisely the property
`gex_intelligence.md` §3's determinism discipline prefers to avoid, and it is now an observation rather
than a theoretical objection.

**The put wall was 103 in every frame** and is unaffected by any of this, as expected: it already sat on
the correct side by accident of where put open interest clusters.

### Revised decision, for ratification

**Retain the side constraint; replace the extremum with a dominant-cluster rule.** The side constraint is
confirmed necessary — the global extremum bracketed spot 0/24 — and confirmed insufficient, since the
constrained extremum lands +0.39% from spot and would produce the lopsided plans described above.

Of the three convergent rules, **"the strike below which 80% of above-spot call gamma accumulates"** is
the one to take forward, for two reasons rather than by preference: it is a *distributional* measure, so a
single thin far strike cannot move it the way "furthest strike ≥10% of max" can; and it returns a real
strike, which the centroid does not. The other two are recorded as equally supported by this evidence.

**None of the three is parameter-free.** Each carries a magic number — 10%, +2%, 80% — and this capture
cannot distinguish them because all three gave the same answer in every frame. **That threshold is the
remaining unratified quantity**, and it should be labelled `UNRATIFIED` in the same terms as
`deployWidthSigmaMultiple` rather than chosen silently.

### Limits of this evidence

Spot moved **0.150%** across the capture, so this establishes **rule stability at near-constant spot**, not
behaviour across a real move. It can and did falsify a candidate rule; it cannot confirm that 150 remains
the dominant cluster when price moves several percent, or how any rule behaves when the dominant cluster is
crossed. That needs data spanning a genuine move — which the [[adr-033-fee-yield-measurement-route|ADR-033]] window will produce, but only under
whichever definition is ratified first. **That circularity is unavoidable and should be stated in the
ratification rather than resolved by waiting.**

---

## Measured correction, 2026-09-27 — this ADR understated the failure it fixed

TICKET N's read-out analysis recomputed the bracketing failure on the same 1336 records, and found that
**this ADR quoted the figure for the wrong price**.

| Reference price | Above call wall | Bracketed by walls |
| --- | --- | --- |
| `pool_price_quote_per_base` — what the Context section quotes | 481 (36.0%) | 855 (64.0%) |
| **`spotOffchain_t` — what this ADR's Decision ratifies** | **646 (48.4%)** | 690 (51.6%) |

The 36.0% figure is arithmetically correct and the text says "pool price", so nothing stated here was
false. But §6 as amended fixes the reference price at `spotOffchain_t`, and against that price the old
global definition failed **48.4%** of the time — **12.4 percentage points worse** than recorded. The
diagnosis and the decision are unaffected; the case for them is stronger than the numbers in the Context
section suggest, and anyone citing 36.0% as "the rate the old rule failed at" is citing the wrong price.

Also measured on the same records, and relevant to the cost this ADR records: under the superseded
planner the call wall changed **9 times in 11.13 hours (0.81/h)**, flipping the deployed envelope between
402 and 939 bins. That oscillation — not hedging — accounted for **95.2%** of the apparent hedge churn in
those runs. See `todo/research/TICKET_N_READOUTS_And_Constant_Sensitivity.md` and **F-021**.

## Correction, 2026-09-27 — the put wall is NOT unchanged by this decision

This ADR states that "the put wall selected 103 in every frame" and that it "is **unchanged** by this
decision". **Both are wrong, and the error was mine: 103 is the put-side _extremum_, not the accumulation
strike.** Running the shipped `extractPutWall` over the same 24-frame capture gives **95**.

The arithmetic, on the first captured frame: 58 eligible below-spot put strikes carrying 3,152,777 of total
magnitude. Accumulating downward from spot reaches only **47.3%** by strike 110; the 80% threshold is first
crossed at **95**, at 91.3% cumulative. Strike 103 is the single largest contributor — which is exactly why
the extremum rule chose it — but one strike is not 80% of the side.

**Consequences.** The put side is affected by this decision after all, and the ADR's framing that it
"escapes only by accident" understated the change: the lower bound moves **6.5% further from spot**, and the
envelope widens from the 103–150 span this ADR quotes to **95–150**. In bins at the pool's 4 bps step that is
**1142, not 940**.

**This propagates to [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]].** Its cost table's bottom row is labelled "full [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] envelope" and was
computed at 940 bins. At the true 1142 bins it becomes **17 positions and 17 bin arrays, 0.9770 SOL
recoverable and 1.2145 sunk, 2.1915 SOL total — 8.77x the superseded 0.25 SOL reserve**, not 7.22x. The
direction of every [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] conclusion is unchanged and its 203-bin σ row is untouched; the worst case is
worse than recorded. Corrected there as well.
