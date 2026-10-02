---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/F-021 - The call wall oscillates between strikes and the planner accepts uncontaining bounds.md
bot_commit: 3f1eec9
source_sha256: dccea9ea79a9a9b52968b6a7f2214101ac3881ac1537c9d59ea4f0bb27d27d19
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/F-021 - The call wall oscillates between strikes and the planner accepts uncontaining bounds.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# F-021 — The call wall oscillates between strikes, and the planner accepts bounds that do not contain spot

**Raised:** 2026-09-27, from TICKET N's 6.7-hour live decision run
(`C:\observation\recon-sim-2026-09-27`, 808 records at 30 s).
**Type:** two findings with one cause. The first is a **strategy-design** problem, not a code defect.
The second is a **missing guard**, and is the empirical case for the check F-020 proposed.
**Severity:** blocks deploying against wall-anchored bounds as currently derived. No capital was at risk;
this was observe-only.
**Contracts:** `gex_intelligence.md` §6 (wall extraction) and §8, `range_planning.md` §2 and §5.
**Related:** **F-020** (the containment check it suggested — this is the evidence for it).
**Superseded in part by F-022**, which found the underlying cause: `planDeployRange` never implements
`range_planning.md` §2b ([[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]), so it returns the wall **envelope** as the range and cannot perform the
containment rejection §2b step 3 already requires. **Read F-022 before acting on Finding 2 or on any
width or churn number below.**

---

## Finding 1 — the call wall is bistable

Over 6.7 hours the **call wall alternated between 150 and 121**, nine transitions, while **spot moved only
1.41%** (120.32–122.01) and the **put wall never moved** from 103.

Regime run-lengths, in order:

```text
wall 150  452 ticks (226.0 min)
wall 121   44 ticks ( 22.0 min)
wall 150    1 tick  (  0.5 min)   <-- single-tick flip
wall 121    1 tick  (  0.5 min)   <-- and straight back
wall 150   11 ticks (  5.5 min)
wall 121   58 ticks ( 29.0 min)
wall 150   62 ticks ( 31.0 min)
wall 121   88 ticks ( 44.0 min)
wall 150    3 ticks (  1.5 min)
wall 121  268 ticks (134.0 min)
```

At 05:30:38 → 05:31:08 → 05:31:38 the wall went 121 → 150 → 121 on **consecutive 30-second ticks**.

**The two strikes are in a near-tie.** Mean `totalNetDollarGex1Pct` was 3.09M in the 150 regime and 3.26M
in the 121 regime — a ~5% difference in aggregate gamma. §6 selects the wall by extremum, so two strikes
within noise of each other trade places as open interest ticks over. Nothing is computed wrongly; the
selection rule simply has no hysteresis.

### Why it matters

The bound is what liquidity is deployed against. A bound that can move 19% (150 → 121) and back inside
one minute has two bad readings and no good one:

- **Reposition on each flip** — nine withdraw-and-redeploy cycles in under 7 hours. Ruinous in gas and
  swap friction, and `range_planning.md` §5's approved-bounds discipline would be re-approving constantly.
- **Ignore flips** — then the plan in force is routinely the one the current signal disagrees with, and
  there is no rule saying which reading is authoritative.

**The effect on the width is large, not marginal.** 150 gives a 939-bin range; 121 gives 402. The
narrower range excludes current spot entirely (below).

### What would settle it

Not prescribing — this belongs to `gex_intelligence.md` §6. The obvious candidates:

- **Hysteresis or a minimum dwell time** on wall selection: a challenger must beat the incumbent by a
  margin, or hold the lead for N snapshots, before the wall moves.
- **A tie-margin rule**: when the top two strikes are within X% of each other, hold the incumbent.
- **Publishing wall stability as a signal** so the FSM can decline to act on a contested wall, in the
  spirit of §9's staleness latch — the signal reports its own unreliability rather than hiding it.

Whichever is chosen, it is a decision about the *signal*, and should be recorded as an ADR against §6
rather than patched at the planner.

---

## Finding 2 — `planDeployRange` returns `ok` for a range that excludes current price

> **Reframed 2026-09-27 by F-022.** This is not a missing guard to be considered; it is **step 3 of a
> ratified rule (§2b, [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]) that was never implemented**, along with the rest of §2b. The finding below
> stands as evidence, but its framing as a new proposal was wrong.

| Call wall | Ticks | Width | **Active bin inside the planned range** | Sim position base inventory |
| --- | --- | --- | --- | --- |
| 150 | 529 | 939 bins | **529 / 529** | 55.0–58.7 SOL |
| 121 | 280 | 402 bins | **11 / 280** | **0.0 SOL** |

**`plan_ok` was `true` on all 808 ticks.** In the 121 regime, spot (~121.7) sits at or above the upper
bound, so the proposed range contains no current price at all — and the planner reports success, because
every §2 check it performs passes: both walls present, finite, positive, correctly ordered, bin step valid.

**This is exactly the guard F-020 recommended**, now with evidence rather than reasoning. F-020 noted that
the planner "is not given the active bin — it takes a price, not a position", so it cannot ask the one
question that would have caught both that unit bug and this one: *does the range I am proposing contain
the pool's current price?*

**35% of ticks in this sample would have produced a deployment with price outside its own bounds.** A
position deployed there is entirely one asset at the moment of deployment and earns no fees until price
re-enters — the opposite of the intent.

---

## What this run does **not** establish

**The headline churn figure from this run is an artefact — do not quote it.** Total simulated hedge churn
was 543 SOL over 6.7 h, which extrapolates to 407× turnover and 16.3% of position value in taker fees.
**279.9 SOL of that — over half — came from the nine wall flips**, because
`simulatedBaseInventory` treats a bounds change as an instantaneous inventory jump: 56 SOL → 0 → 56 with
each flip.

In the real system a bounds change is a **reposition** governed by the operational FSM, not a hedge
resize. The sim has no reposition model, so it books the whole inventory swing as hedge churn.

The defensible figure is the stable-regime one: **263 SOL over 529 ticks (~4.4 h) in the 150 regime**,
and even that includes flip-adjacent ticks. A clean churn number needs the flip boundaries excluded, and
that analysis has not been done.

**A prior estimate from the same run's first 2.5 hours was 7.8%/h → 39× → 1.58% in fees**, measured
before any wall flip occurred.

> **Do not treat that as the quiet-regime estimate either — F-022.** It was computed against a position
> spread across the ~939-bin **envelope**. A §2b window is materially narrower and traverses its full
> base-to-quote range faster, so real churn scales up roughly as `envelopeBins / width`. The 1.58% is a
> **floor multiplied by an uncomputed factor**, not an estimate.

---

## What this run does establish

- The zero-gamma level is **stable**: 104.68–105.98 across 807 ticks, with **zero jumps above 1%**. An
  earlier 26-minute sample suggested instability; over 6.7 hours it is the *walls* that are unstable and
  the ZGL that is steady. This is the reverse of the initial reading and supports `range_planning.md` §2
  anchoring bounds on walls only in so far as the walls can be stabilised.
- Bound **width** is a clean function of the wall pair — 939 bins at 150, 402 at 121 — so width is a
  faithful indicator of which regime is in force. **But per F-022 these are envelope widths, not deployed
  widths**: §2b derives the deployed width from volatility and centres it on the active bin, so every
  width figure here describes the envelope only.
- The pipeline itself is sound: **808/808 plans produced, zero rejections, zero stale snapshots, zero tick
  failures** over 6.7 hours against live Deribit and Solana.

## Suggested next steps

1. **Raise the §6 wall-stability question as an ADR.** It is a signal-design decision and the most
   consequential thing in *this* finding. It remains genuinely unsettled: §6 defines extraction and tie
   handling but says nothing about temporal stability.
2. **Implement `range_planning.md` §2b in full — see F-022.** Not "add a containment check": the check is
   step 3 of a rule whose other four steps are also missing.
3. **Give the sim a reposition model, or stop reporting churn across bounds changes.** Splitting
   `sim_hedge_delta_base` into within-bounds drift and bounds-change jumps would make the number
   trustworthy; currently the two are summed.
4. Re-run once walls are stabilised, to get the churn figure the strategy actually has to beat.

---

## 2026-09-27 — re-based by [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] (ratified), not closed

[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] is ratified, which changes what this finding is asking. The 150↔121 oscillation was not a
stability defect to damp: 121 was a **pin** and 150 a **resistance level**, so hysteresis would have
stabilised a choice between two different kinds of level. Under the ratified rule 121 is ineligible
whenever price is above it, and the ratified accumulation rule selected **150 in all 24 frames** of the
live capture.

That is **not** evidence of stability. Those 24 frames span a 0.150% price move, so they test nothing
about behaviour across a real move — the only condition under which wall stability matters. **This finding
stays open**, re-based to the ratified definition: the question is now whether the 80%-accumulation wall
is stable across a price move large enough to reshape the above-spot gamma distribution, which the
[[adr-033-fee-yield-measurement-route|ADR-033]] window is the first dataset able to answer. Step 4 below is unchanged in intent; steps 1–3 stand.

---

## 2026-09-27 — step 3 answered, and it changes what this finding is about

Step 3 asked for `sim_hedge_delta_base` to be split into within-bounds drift and bounds-change jumps,
"currently the two are summed". Measured over the 1336-record sim run (11.13 h, 100 SOL position):

| Component | Turnover | Rate | % position/yr @ 4 bps |
| --- | --- | --- | --- |
| **Within-bounds drift** (range unchanged, 487 ticks) | 32.05 SOL | 2.88 SOL/h | **10%** |
| **Bounds-change jumps** (range moved, 848 ticks) | 639.70 SOL | 57.49 SOL/h | 201% |
| Summed, as recorded | 671.75 SOL | 60.37 SOL/h | 212% |

**95.2% of the apparent hedge churn was this finding's oscillation, not hedging.** The planner moved the
range on **63.5% of tick transitions**, and the call wall changed 9 times in 11.13 h (0.81/h), flipping
the envelope between 402 and 939 bins. Each flip re-marked simulated inventory across a new range and the
harness summed that into the hedge delta.

Two consequences. **The churn figure the strategy has to beat is ≈10%/yr, not 212%** — step 4's "re-run
once walls are stabilised" would have found roughly the former, and quoting the latter would have
condemned the strategy for a defect in wall selection. **And a tolerance band cannot fix this**: widening
`epsilonBase` 80× (0.0625 → 5.0 SOL) cut the rebalance count 96% but turnover only 12%. This finding's
subject was never hedge tuning; it is that an unstable wall definition manufactures phantom trading cost.

Full numbers: `todo/research/TICKET_N_READOUTS_And_Constant_Sensitivity.md`, read-out 3.

**Still open**, and unchanged by this: whether the [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] accumulation wall is stable across a real price
move. These runs span 1.2–1.4%, which is not a test of that.
