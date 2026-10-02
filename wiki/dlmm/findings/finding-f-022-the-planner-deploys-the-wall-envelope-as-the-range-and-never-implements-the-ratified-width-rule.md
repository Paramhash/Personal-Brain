---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/F-022 - The planner deploys the wall envelope as the range and never implements the ratified width rule.md
bot_commit: 3f1eec9
source_sha256: e9c96eb8b02cde37bc72ac49fdece7c92fc2d02a9b1e6ef2951694d56575f8fd
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/F-022 - The planner deploys the wall envelope as the range and never implements the ratified width rule.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# F-022 — The planner deploys the wall envelope as the range, and never implements [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s width rule

**Status: CLOSED 2026-09-27 by TICKET O.**
**Raised:** 2026-09-27. Found by the independent review in
`todo/findings/IR_REVIEW_REQUEST_Wall_Stability_And_Bound_Derivation-findings.md` §6 and §8, and
confirmed here against the contract and the code.
**Type:** contract-versus-implementation gap. Not a coding error inside what is implemented — the
implemented behaviour is simply the *superseded* design.
**Severity:** high. It invalidates measurements taken through the planner, it explains F-021's second
finding entirely, and it is a prohibition breach: `range_planning.md` §5 forbids exactly what the code
does.

> **Bounded on 2026-09-27.** The actuator *does* implement §4's containment check:
> `dlmmDeploy.ts:202` evaluates `pool.activeBinId >= plan.lowerBinId && pool.activeBinId <= plan.upperBinId`
> and reports `ACTIVE_BIN_OUT_OF_RANGE` (`dlmmDeploy.ts:128`, `:284`), with committed cases.
> **No capital was ever at risk of an out-of-range deployment.** §2b step 3 is an earlier and
> cheaper failure, and defence in depth — not the only guard. The **invalidated measurements**
> are the serious half of this finding, not a capital-safety hole.
**Contracts:** `range_planning.md` **§2b ([[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]])**, §4, §5. Related: [[adr-030-deployment-sol-reserve|ADR-030]] (reserve),
`ev_policy.md` (σ and horizon inputs).
**Ticket:** DRAFT TICKET O (`todo/research/DRAFT_TICKET_O_Implement_The_ADR_034_Derived_Deploy_Width.md`), not yet staged.
**Related findings:** **F-021** (its Finding 2 is a *consequence* of this, not a separate gap);
**F-020** (its suggested containment check is already mandated by §2b step 3 — see "Corrections").

---

## What the contract requires

§2b, introduced by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]], changed what a wall *is*. Walls became an **envelope** the deployed range
may not leave; the deployed **width** is derived separately:

```text
sigmaHorizon       = sigma * sqrt(horizonSeconds)
targetHalfWidthPct = deployWidthSigmaMultiple * sigmaHorizon
targetHalfBins     = ceil( ln(1 + targetHalfWidthPct) / ln(1 + binStep / 10_000) )

width = clamp( 2 * targetHalfBins + 1, MIN_BINS_PER_POSITION, envelopeBins )
```

applied in a fixed five-step order: convert both walls to bins (the **envelope**); **reject** an
inverted envelope or one narrower than `MIN_BINS_PER_POSITION`; **reject if the reconciled active bin
lies outside the envelope**; compute `width` by the clamp; then place a window of exactly `width` bins
**centred on the active bin**, shifted inward only as far as needed to stay inside the envelope, with an
odd remainder going to the lower side first.

§5 states the prohibition directly: *"Do not deploy the full wall-to-wall interval as a range without
applying §2b's derived width."*

## What the code does

`planDeployRange` (`src/intelligence/range/rangePlanner.ts`) converts both walls and returns the
inward-rounded **wall-to-wall interval** as `lowerBinId`/`upperBinId`. Counted occurrences in that file:

| §2b concept | occurrences in `rangePlanner.ts` |
| --- | --- |
| `sigma` | 0 |
| `horizon` | 0 |
| `MIN_BINS_PER_POSITION` | 0 |
| `envelope` | 0 |
| `targetHalfBins` | 0 |
| `deployWidth` | 0 |
| `activeBin` | 0 |

So **none** of §2b is implemented: no σ input, no horizon, no floor, no clamp, no active-bin window, and
neither of the two mandated rejections. The function's signature cannot express them — it receives the
GEX walls, a `BinConversion` and a `RangePricingContext`, and is never given the active bin.

The implemented behaviour is the pre-ADR-034 design, and §5 now prohibits it.

## Measured consequence

From TICKET N's 6.7-hour live run (808 records, 30 s cadence, 2026-09-27):

- Returned width was **939 bins** with the call wall at 150 and **402** at 121. §2b line 152 tabulates
  "wall envelope ~940 bins" against a far narrower derived width — so **the run was measuring the
  envelope, reported as if it were the deployed range.**
- `plan_ok` was **true on all 808 ticks**, including **269 of 280** ticks in the 121 regime where the
  active bin lay outside the returned interval. §2b step 3 requires those to be **rejected**. The
  planner cannot reject them because it has no active bin to test.

**This supersedes F-021's Finding 2.** That finding described the containment gap as a missing guard
worth considering. It is not a gap in reasoning — it is step 3 of a ratified rule, unimplemented.

## Why this invalidates the churn measurements, and in which direction

Every churn figure produced so far assumed a position spread across the **whole envelope** — the
`simulatedBaseInventory` model divides by `(upper - lower)`, which was ~939 bins. §2b would deploy a
window of `width` bins centred on the active bin, materially narrower.

**A narrower window traverses its full base-to-quote range faster**, so for the same price path the
simulated inventory swings proportionally harder: roughly as `envelopeBins / width` to first order. The
honest expectation is therefore that **real hedge churn is higher than measured, not lower** — the
opposite of the reassuring direction. The provisional 1.58%-of-position fee estimate from the quiet
regime should be treated as a floor scaled by a factor nobody has computed yet.

No churn number should be quoted until the planner produces a §2b window.

## Corrections this forces to earlier findings

- **F-020** recommended raising a containment check "against `range_planning.md` rather than
  implementing it unilaterally". That was wrong in its premise: the check is already ratified as §2b
  step 3. The work is implementation, not an ADR.
- **F-021** described the wall-anchored 939-bin range as evidence about bound width. It is evidence
  about the *envelope*. Its §6 question — "is anchoring bounds on walls the right design at all" — is
  answered by the contract: walls are an envelope and were never meant to be the range.

## What is genuinely open, and not blocked by this

Two dependencies §2b itself flags, neither of which prevents implementing the rule:

1. **`deployWidthSigmaMultiple` is UNRATIFIED**, default 1. §2b is explicit that the conservative
   directions conflict — a small multiple concentrates liquidity and raises fee yield per unit, a large
   one keeps price in range longer — and that **±1σ is not a 68% chance of staying in range**, because
   that figure describes the terminal distribution, not the probability a path never leaves the band.
   The ratifier is `observation_archive.md` §6 question 3, which needs only the `active_bin_id` series —
   **which the running 21-day window is collecting.** Implement with the default and label it.
2. **[[adr-030-deployment-sol-reserve|ADR-030]]'s `0.25 SOL` reserve is not width-aware.** §2b computes that even 3 uninitialized bin
   arrays cost `0.0434 + 3 × 0.0714 = 0.2577 SOL`, above the ratified reserve, so *even the tightest
   defensible width breaches it*. [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] routes this to its own ADR. It gates **deployment**, not the
   planner change.

## What an implementation ticket must carry

§2b names three requirements, and they should be lifted verbatim rather than reinvented:

- **A negative `activeBinId` case.** The target pool's active bin was `-5311` at verification and
  `-5280` in this run; every soak in the repository ran at `+1110`. The planner carries no sign bug
  today, but no committed test outside the observation suite exercises a negative active bin through
  width selection, containment and chunking. A Devnet fixture at `+1110` cannot catch a sign error on
  the only pool that matters.
- **A case for each of §2b's two rejections**, plus one where the floor binds and one where σ binds, so
  every branch of the clamp is covered rather than only the fine-pool path.
- **The tie rule pinned by test** — an odd remainder to the lower side first — since a window placed
  near a wall is where a non-deterministic remainder shows up first.

Add to those, from this finding:

- **A case asserting the returned interval is not the envelope** when σ implies something narrower —
  the defect this finding records would have been caught by a single such assertion.
- **`src/recon/decisionHarness.ts` must be updated in step**, or TICKET N's churn read-outs continue to
  measure the envelope. It needs the active bin (it already has it), σ, and the horizon.

## Note on the review that found it

The independent reviewer read §2b; the prior analysis had read §2, §3 and §5 and stopped. Two findings
(F-020, F-021) were filed with a conclusion the contract had already settled, which is the specific
failure mode of reading an implementation and a contract section rather than the contract in full.

---

## Closure — 2026-09-27, TICKET O

Closed citing tests, not reasoning.

**The fix.** `planDeployRange` implements §2b's five steps in order: derive the envelope, reject an
envelope below `minBinsPerPosition`, reject an active bin outside it, clamp the σ-derived width between
the floor and the envelope, and place a window of exactly that width centred on the active bin with the
odd remainder to the lower side. σ and the horizon are passed in rather than imported, because
`src/intelligence/` sits upstream of `src/decision/` under §5's flow. `MIN_BINS_PER_POSITION` moved to
`config/strategy.config.ts` so the floor has one home without inverting that arrow.

**The cases that close it** — `src/intelligence/range/__tests__/rangePlanner.test.ts`:

| Case | What it pins |
| --- | --- |
| R30 | §2b's own worked figure: `targetHalfBins` = 101, width = 203 |
| **R31** | **The returned interval is the window, not the envelope** — the assertion whose absence let this ship |
| R32 | The window is centred on the active bin |
| R33 | An even width puts the odd remainder on the lower side (§2b's tie rule) |
| R34 / R35 / R36 | The floor binds / σ binds / the envelope binds — every branch of the clamp |
| R37 | A too-narrow envelope is rejected, not widened (§5) |
| R38 | An active bin outside the envelope is rejected — F-021's 121-regime in miniature |
| R39 | Equality with either envelope bound is containment (§4), at both edges |
| R40 | A **negative** active bin works through width, containment and placement |
| R41 | Unusable width inputs are rejected rather than producing a width |

**Suite: 672/672 across 20 suites, typecheck clean** (was 660).

**Verified live**, against the real pool with the soak still running: the planner returned a **203-bin
window inside a 402-bin envelope**, with the active bin contained and both recorded per tick.

**The predicted direction holds.** One bin of drift now moves a 100 SOL simulated position by
`100/202 = 0.495` SOL, against `100/938 = 0.1066` before — **4.64×**, matching the predicted
`envelopeBins / width` of 4.63. So earlier churn figures understated inventory sensitivity by about that
factor, in the direction this finding warned about. **Aggregate churn over a full run has not been
re-measured**, and no fee estimate should be quoted until it is.

**Still open, and deliberately not in this ticket:** ratifying `deployWidthSigmaMultiple` (its ratifier is
`observation_archive.md` §6 question 3, which the running window is collecting), making [[adr-030-deployment-sol-reserve|ADR-030]]'s reserve
width-aware, and F-021's wall stability. A bistable call wall still produces two legal plans that
disagree.
