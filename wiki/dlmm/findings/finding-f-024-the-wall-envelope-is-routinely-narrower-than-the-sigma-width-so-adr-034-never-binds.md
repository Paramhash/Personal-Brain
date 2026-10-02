---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/F-024 - The wall envelope is routinely narrower than the sigma width, so ADR-034 never binds.md
bot_commit: 3f1eec9
source_sha256: a884af9e1cce1d5cb1224630dfe1304ae04ea4f9ab6810e44994bad448d796cd
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/F-024 - The wall envelope is routinely narrower than the sigma width, so ADR-034 never binds.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# F-024 — The wall envelope is routinely narrower than the σ-derived width, so [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s rule never binds

**Raised:** 2026-09-27, from the first live frame produced by TICKET P's monitor.
**Type:** strategy finding. Not a defect — every component behaved exactly as specified. The specification
produces a result nobody appears to have anticipated.
**Severity:** high for [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s usefulness and for [[adr-030-deployment-sol-reserve|ADR-030]]'s reserve. No capital was at risk.
**ADR:** **[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]** (PROPOSED) `docs/decisions/038-gex-walls-are-selected-on-the-correct-side-of-spot.md` — constrains each wall to its own side of spot.
**Contracts:** `range_planning.md` §2b ([[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]), `liquidity_position_manager.md` §3
(`MIN_BINS_PER_POSITION`), [[adr-030-deployment-sol-reserve|ADR-030]] (reserve). Related: **F-021**, **F-022**.

---

## The observation

One live frame, 2026-09-27, against the real SOL/USDC pool and a 398-instrument Deribit chain:

```text
spot      120.63        pool price 120.4673
put wall  120           call wall  121
envelope  bins [-5305, -5285]  =  21 bins  =  0.80% wide
window    bins [-5305, -5285]  =  21 bins   <- identical to the envelope
binding constraint: ENVELOPE        sigma-implied width: 203 bins
```

**The walls were one strike apart.** The σ-derived width wanted **203 bins**; the envelope permitted
**21**. So §2b's clamp saturated at `envelopeBins` and the deployed window *is* the wall-to-wall interval —
the very thing §5 prohibits deploying, arrived at legitimately because the clamp's ceiling is the envelope.

## Why this matters

**1. [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s width rule is inoperative in this regime.** The whole point of §2b was that walls bound the
width while volatility sets it. With a 0.80% envelope against a 8.4% σ-implied width, volatility never gets
a say: the answer is always "as wide as the walls allow". The `deployWidthSigmaMultiple` that
`observation_archive.md` §6 question 3 is meant to ratify has **no effect at all** while this holds —
ratifying it would be ratifying a number the code cannot use.

**2. The position sits one bin above the legal floor.** `MIN_BINS_PER_POSITION` is 20 and the envelope gave
21. One strike closer together and §2b step 2 rejects with `ENVELOPE_BELOW_MIN_BINS`. This is not
hypothetical: the final tick of the 2026-09-27 recon run measured a 20-bin envelope — exactly the floor.
**The strategy is operating at the boundary of producing no plan at all.**

**3. [[adr-030-deployment-sol-reserve|ADR-030]]'s reserve problem gets worse, not better.** §2b already recorded that even a 203-bin window
touches 3 uninitialized bin arrays costing `0.2577 SOL`, above the ratified `0.25 SOL`. A 21-bin window
touches fewer arrays, which helps — but a 21-bin position is also a far more fragile one, needing
repositioning on the smallest move. The reserve question and the width question are coupled in a way
neither ADR states.

**4. It explains F-021 differently than F-021 does.** F-021 recorded the call wall oscillating 150 ↔ 121 and
treated it as a stability problem. This frame shows walls at 120/121 with **87 qualifying call candidates**
and a 31.9% leader margin — not contested by any threshold. So the walls are not always in a near-tie; they
are sometimes *tightly clustered around spot*, which is a different condition with a different consequence.
F-021's hysteresis question remains open, but it is not the whole story.

## What was verified, and what was not

**Verified:** the numbers above are one live frame from the monitor, computed by the production
`buildGexProfile`, `planDeployRange` and view model. Every component did what its contract says. The
envelope-binding path is exercised by `rangePlanner`'s R36 and the view model's P07.

**Not verified:** how *often* this regime holds. One frame is an existence proof, not a distribution. The
2026-09-27 recon run's final tick corroborates it (20-bin envelope), and its earlier ticks showed 939-bin
envelopes — so the envelope evidently ranges over nearly two orders of magnitude. **That range is the
finding that matters, and measuring it is the next step.**

## Suggested next steps

1. **Measure the envelope-width distribution** over the recon run's 1336 records and, better, over the
   [[adr-033-fee-yield-measurement-route|ADR-033]] window once it runs. `envelope_bin_span` is recorded per tick; the question is what fraction of
   ticks have an envelope narrower than the σ-implied width, and what fraction fall below the 20-bin floor.
2. **Decide what a sub-floor envelope means operationally.** §2b rejects, correctly. But a strategy that
   cannot plan whenever its walls converge needs a stated response — hold the existing position, stay out,
   or use a different bound — and that is an ADR, not an implementation choice.
3. **Do not ratify `deployWidthSigmaMultiple` until step 1 is done.** If the envelope binds in most ticks,
   the multiple is close to irrelevant and ratifying it would create false confidence in a lever that does
   not move.
4. Re-read §2b's worked example. Its "narrowing 940 bins to 203" frames the envelope as the wide bound and
   σ as the narrowing force. This frame is the exact inverse, and the contract does not discuss that case.

---

## Extension, 2026-09-27 — the planner produced nothing at all, for every frame observed

The original finding said [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s width rule is *inoperative* in this regime. Continuous observation
through TICKET P's monitor shows something stronger: in the regime that held for the whole observation
period, **the planner produced no plan at all**.

### Measured

Every frame the monitor published was `BLOCKED` with `ACTIVE_BIN_OUT_OF_RANGE`. A representative one:

```text
spot        121.3871      pool price 121.1922
put wall    103           call wall  121
envelope    null          window     null
status      BLOCKED       rejection  ACTIVE_BIN_OUT_OF_RANGE
```

**The cause is legible in one line: the pool price is 121.19 and the call wall is 121.** Price sits
*above* the upper wall, so the envelope cannot contain the active bin and §2b step 3 rejects — correctly.

This is the condition derived while building the collector and recorded in `collector.test.ts` C08:
because the pool price is itself derived from the active bin, §2a's wall scaling moves the envelope by the
same factor, and `binId = activeBin + ln(wall / spot) / ln(1 + binStep/10_000)`. The envelope tracks the
active bin exactly, so step 3 can **only** fire when the walls fail to bracket spot. That is no longer a
theoretical corner: it is the observed state of the market.

### A number from the first report was wrong, and is withdrawn

The first screenshot showed a rejection counter of **4072 out of 4072 frames**, and that figure was
reported as evidence of scale. **It is an artefact of F-025** — a backpressure defect that re-sent the same
frame thousands of times, and the browser counted each copy. The server had published 7 frames.

After fixing F-025 the counts agree: 3 frames published, 3 rejections, one per frame. **The rate was
wrong; the state was not.** Every frame observed, before and after the fix, rejected for the same reason.

What is *not* established is duration: the monitor has run for minutes, not days. "Every frame observed"
is an accurate statement about a short window, and nothing here measures how long the regime persists.

### Why this sharpens the finding rather than replacing it

The original observation was a 21-bin envelope against a 203-bin σ width — the walls too *tight* to use.
This is the adjacent failure: the walls have drifted so that spot is outside them altogether. Both come
from the same root, which is that **the walls are clustered on top of spot and move with it**, and the
combination means:

1. When the walls bracket spot narrowly, [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s σ rule cannot bind — the envelope always wins.
2. When they fail to bracket spot at all, there is no plan — the strategy is simply out.

Between those two, the interval in which the σ-derived width is the operative constraint may be small.
**That interval is the strategy's entire operating range**, and nothing has measured it.

### Revised next steps

Steps 1–4 of the original stand. Add, before them:

0. **Measure how often the walls bracket spot at all.** This is cheaper and more fundamental than the
   envelope-width distribution: it is one boolean per recorded tick
   (`put_wall_strike <= spot <= call_wall_strike`), computable over the existing 1336 TICKET N records
   immediately and over the [[adr-033-fee-yield-measurement-route|ADR-033]] window as it accrues. If that fraction is low, the width question is
   premature and the wall-derivation question — F-021's, and §6's — is the only one that matters.

---

## Step 0 answered, 2026-09-27 — measured over all 1336 TICKET N records

The extension above called for measuring how often the walls bracket spot at all, and said it was cheap.
It was: one boolean per record over the retained run.

| | records | share |
| --- | --- | --- |
| walls **bracket** spot (`put ≤ price ≤ call`) | 855 | **64.0%** |
| price **above** the call wall → `ACTIVE_BIN_OUT_OF_RANGE` | 481 | **36.0%** |
| price below the put wall | 0 | 0.0% |

Envelope span across the same records: **min 19, median 402, max 939 bins**, with **17 records (1.3%)** at
or below the 20-bin floor.

### What this settles

**The strategy could not have deployed in roughly a third of the observed period.** 36% of ticks put price
outside the call wall, where §2b step 3 rejects and there is no plan. That is not a rare corner; it is a
routine state of this market.

**The failure is one-sided.** Price was never below the put wall — not once in 1336 records. Every
out-of-range tick was price running *above* the call wall. That asymmetry is a fact about how the call wall
is selected, and it points at `gex_intelligence.md` §6 rather than at [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]: a call wall that sits at or
just below spot is not functioning as an upper bound.

**The envelope is usually wide, not narrow.** A median of 402 bins against a σ-implied 203 means σ *does*
bind in the typical case, and the 21-bin frame that prompted this finding was closer to the 1.3% tail than
to normal. The original headline — "the envelope is routinely narrower than the σ width" — **is wrong as
stated, and is corrected here**: it is routinely *wider*. The real problem is not envelope width but
envelope *placement*, and the two were conflated because a single frame happened to show both.

### Consequences for the revised next steps

- Step 1 (envelope-width distribution) is now partly answered and is **lower priority** than it looked.
- Step 3 stands but for a different reason: σ binds in the median case, so `deployWidthSigmaMultiple` is
  *not* irrelevant. Ratifying it matters, and `observation_archive.md` §6 question 3 remains the right
  instrument.
- **A new step, ahead of the others: the one-sided call-wall failure is the finding to pursue.** Why does
  the call wall sit below spot 36% of the time while the put wall never does? That is a §6 wall-extraction
  question and it shares a root with F-021.

---

## Why the failure is one-sided, 2026-09-27 — the call wall is a pin, not a ceiling

The step-0 measurement left an unexplained asymmetry: price above the call wall 36% of the time, below the
put wall 0%. Measuring the *distance* from each wall to the pool price over the same 1336 records explains
it, and the explanation is structural rather than a property of this particular market.

| | min | median | max |
| --- | --- | --- | --- |
| call wall **above** pool price | −0.56% | **+0.20%** | +24.86% |
| put wall **below** pool price | +0.35% | **+14.98%** | +15.38% |

Median absolute distance: **call wall 0.36% from spot, put wall 14.98% from spot — a 42× asymmetry.**

Only two strikes ever won each side: call wall ∈ {121, 150}, put wall ∈ {103, 120}.

### The mechanism

**Option gamma is maximised at the money.** A "wall" defined as *the strike carrying peak dollar gamma on
its side* will therefore sit wherever spot is, not above or below it. The call wall tracking spot to within
a third of a percent is not a coincidence or a data problem — it is what that definition produces.

The current frame shows the selection is not noisy either: 121 wins by a **43.5% margin over 87 candidates**.
It is a decisive winner. It wins *because that is where spot is*.

The put side escapes this only because put open interest clusters well below spot as downside protection,
so the put-side gamma peak is displaced downward by a real positional fact. That displacement is what makes
the put wall usable as a lower bound, and its absence is what makes the call wall unusable as an upper one.

### What this means for the design

A peak-gamma strike is a **pin or magnet level** — where dealer hedging tends to attract price. That is
close to the opposite of a ceiling. `range_planning.md` §2 uses the two walls as an *envelope the deployed
range may not leave*, which requires both to be bounds. One of them is not.

So the observed behaviour is not a planner defect and not a market anomaly:

- `planDeployRange` correctly refuses a range price has already left.
- The GEX engine correctly reports the strike with the most call gamma.
- **The design step that does not hold is treating that strike as an upper bound.**

### Consequence for the open questions

This subsumes rather than replaces F-021. That finding recorded the call wall oscillating 150 ↔ 121 and
asked for hysteresis. The oscillation is real, but it is between a **near-ATM pin (121)** and a **far-OTM
strike (150)** — those are two different kinds of level, and a hysteresis rule that merely stabilises the
choice between them would stabilise an answer to the wrong question.

**The question for `gex_intelligence.md` §6 is therefore not "how do we stop the call wall flipping" but
"what should bound the upper side of a range at all."** Candidates worth assessing — none is this
finding's to choose:

- the highest strike above spot carrying material call gamma, rather than the maximum;
- a gamma-weighted centroid of above-spot strikes;
- an explicit call-side *resistance* definition distinct from the peak-gamma pin;
- accepting that GEX bounds only the downside and deriving the upper bound another way.

Until that is settled, the [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] width work rests on an envelope whose upper edge is not a bound, and the
36% rejection rate is the visible consequence rather than the problem itself.

---

## 2026-09-27 — step 0 answered, and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] ratified

Revised step 0 ("measure how often the walls bracket spot at all") is **answered**, and the answer is the
worst available one: across a 24-frame live capture the call wall sat above spot in **0 of 24 frames**
under the shipped rule. Combined with the 36.0% above-call-wall rate over the 1336 recorded decisions,
the bracketing failure is confirmed as structural rather than an artefact of the recorded two-strike set.

**[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] is ratified**, redefining a wall as a side-constrained, distributionally-selected strike. That
addresses the root this finding identified — walls clustered on top of spot and moving with it — so the
finding's diagnosis is settled. Its *measurement* questions are not: the original steps 1–4 asked for the
envelope-width distribution and the interval in which the σ rule is the operative constraint, and the
ratified definition **changes both** (median envelope 402 bins → roughly the 103–150 span, which moves
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s clamp into the σ-binding regime for the first time). Those steps must be re-run under the new
definition, against the [[adr-033-fee-yield-measurement-route|ADR-033]] window, once [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] is implemented — no historical series is comparable
across the change.
