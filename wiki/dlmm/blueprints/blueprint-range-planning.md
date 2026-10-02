---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/range_planning.md
bot_commit: ab766fb
source_sha256: daad6bbcc1da9a65b7ab41f9866f7248e3c58b796a3738c919e2c42c6c8a40a5
exported_at: '2026-10-02T12:50:28Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/range_planning.md` at commit `ab766fb`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# Range Planning

**Domain owner:** Intelligence
**Status:** authored and binding
This file fixes the deterministic intelligence boundary that converts GEX walls and zero-gamma context into deployable DLMM bin ranges.

---

## 1. Scope

This blueprint governs:

- deriving deploy bounds from `putWallStrike_t`, `callWallStrike_t`, and zero-gamma context
- converting validated quote bounds into deterministic DLMM bin identifiers
- emitting a range plan consumed by the DLMM deployment actuator

It does not fetch market data, submit Solana transactions, choose a liquidity strategy, or
advance either FSM.

---

## 2. Wall-anchored deploy bounds

Deploy bounds must be strictly anchored between the GEX walls:

```text
lower bound >= putWallStrike_t
upper bound <= callWallStrike_t
```

**Amended 2026-09-26 by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]].** These were equalities until the wall interval was measured
against a fine-binned pool, where wall-to-wall spans roughly 940 bins and places 99.89% of deployed
capital in bins earning nothing. The walls are now an **envelope** the deployed range may not leave,
and the width *inside* that envelope is derived in §2b. Nothing here permits a bound outside a wall;
the change is one-directional, from "equal to" to "no wider than".

The lower bound must be strictly less than the upper bound. A missing wall, a non-finite wall,
or inverted/equal bounds is not a range to repair heuristically; the planner must reject it so
the downstream actuator cannot deploy outside the approved wall interval.

`zeroGammaLevel_t` is contextual intelligence. It may inform diagnostics and deterministic
plan metadata, but it must not expand, contract, or move either wall-anchored bound unless a
later ADR changes this rule.

### 2a. Walls arrive in USD and must be converted to pool quote units ([[adr-023-range-planner-devnet-scaling-and-containment|ADR-023]])

`gex_intelligence.md` derives `callWallStrike_t` and `putWallStrike_t` from Deribit SOL option
strikes, which are **USD per SOL**. §3a's conversion expects a price in the **pool's quote token
per whole base token**. Those are the same number only when the pool quotes in USD, and nothing
guarantees that — the configured Devnet pool quotes in a token worth roughly 1/6,937,302 SOL.
The planner must therefore convert before converting again:

```text
poolWall = wallUsd * (poolActiveBinPriceQuotePerBase / spotOffchain_t)
```

- `poolActiveBinPriceQuotePerBase` is the pool's own active-bin price, by the **same** formula
  `ev_policy.md` §5a fixes for the EV gate. There is one active-bin price in this repository and
  this is it; a second formula here would be a second answer to one question
- `spotOffchain_t` is the USD spot the walls are denominated in, carried on the same GEX
  snapshot the walls came from, so the ratio is taken between two prices of the same instant
- the scaled walls then pass through §3a's decimal-aware bin conversion unchanged

**This is a change of numeraire, not a change of bound.** §2's anchoring rule is untouched: the
lower bound is still the Put Wall and the upper still the Call Wall, expressed in the units the
pool actually prices in. Scaling by a strictly positive factor preserves ordering, so it can
neither invert the bounds nor widen them past a wall.

Both scaling inputs must be finite and strictly positive. A missing or unusable pool price or
off-chain spot is a **named rejection**, never an unscaled wall and never a substitute price
from another venue — an unscaled wall is a bound in the wrong currency, which is the defect this
section exists to remove.

### 2b. The deployed width is derived, and the walls only bound it ([[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]])

**Wall spacing is an options-structure quantity; bin width is a pool-geometry quantity. Nothing
makes them commensurate.** On an 80 bps pool the Put and Call walls happened to enclose 47 bins, a
deployable position. On the 4 bps mainnet SOL/USDC pool the same 37.6% encloses roughly **940 bins**,
which is 14 bin arrays, 14 chunked transactions, and — because fees accrue only in the active bin —
**939 of 940 bins earning nothing at any instant**. A range that wide is not a concentrated liquidity
position; `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER = 1.8` encodes a concentration *benefit* that
such a position does not have.

The planner therefore owns a **deploy width**, distinct from the wall envelope.

#### 2b-0. Three intervals, not two ([[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]])

Since [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]] the planner derives **three** nested intervals, and conflating any two of them loses the reason a plan was refused:

| Interval | Meaning | Source |
| --- | --- | --- |
| **Raw wall envelope** | where the market says the bounds are | [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] walls, scaled by §2a |
| **Buffered envelope** | where *policy* permits deploying | [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]] §2a, applied to the raw walls |
| **Deployed window** | what is actually deployed | §2b's σ-derived width, clamped by the **buffered** envelope |

The buffered envelope is derived by surrendering a fraction `k` of the room between spot and each wall:

```text
bufferedCallWall = spotOffchain_t + (callWallStrike_t - spotOffchain_t) * (1 - k)
bufferedPutWall  = spotOffchain_t - (spotOffchain_t - putWallStrike_t) * (1 - k)
```

`k` is `wallBufferRoomFraction`, **ratified policy and explicitly not calibrated** ([[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]] §5). `k = 0` reproduces the pre-ADR-041 behaviour exactly, which is what keeps a historical plan re-derivable from its record.

**Four rules bind.**

**The buffer applies to the USD walls, before §2a's scaling — and the order is a legibility choice, not a correctness one.** The two commute: the `spot` in the buffer cancels against the `spot` in `scale = poolPriceQuotePerBase / spotOffchain_t`, so both orders yield `poolPrice × (1 + d × (1 − k))`. USD-first is chosen so `lowerBoundQuote` / `upperBoundQuote` keep exactly the meaning they had before [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]].

**The buffered envelope is the operative ceiling.** §2b step 4's clamp and step 5's placement both read it, not the raw envelope. A window clamped to the buffered count but *placed* against the raw bounds would have the right width and could still shift outward past the buffered limit — correct by one measure and escaped by the other.

**Raw walls and the raw envelope are never overwritten.** They are retained so a buffer-induced refusal stays distinguishable from a genuine wall breach, which is why the buffer has its own rejection reasons: `BUFFERED_ENVELOPE_BELOW_MIN_BINS` and `BUFFERED_ENVELOPE_DEGENERATE`, separate from the raw `ENVELOPE_BELOW_MIN_BINS` and `DEGENERATE_BIN_RANGE`. "Policy declined the room" and "the walls were too tight" are different facts with different owners.

**An invalid `k` is rejected, never clamped** — `INVALID_BUFFER_FRACTION` for anything outside a finite `[0, 1)`. A silently clamped buffer becomes a different policy in exactly the regime the buffer exists to protect against, and does so without saying it has.

**One consequence worth stating, because it contradicts the natural reading.** The buffer is a **deployment entry gate**, not a width control. Measured on the 2026-09-27 surface, σ remains the binding constraint until `k ≈ 0.185` while spot leaves the buffered envelope at `k ≈ 0.190` — a 0.005-wide interval in which the buffer governs the width. For any ordinary `k` the deployed window is **unchanged** and the buffer's only effect is to refuse deployments too close to a wall. It does lower the worst-case envelope, which is why [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]'s reserve ceiling falls with it.

**Step 3's containment check guards an invariant, not a reachable failure.** Because the buffered bounds are strictly on either side of spot for every `k < 1`, and the pool price derives from the active bin, containment holds by construction. The check stays — it is the only thing that would catch a future change to the scaling or rounding breaking that derivation — and is asserted as a property over `k` rather than by a fixture that forces it.

#### The rule

```text
sigmaHorizon      = sigma * sqrt(horizonSeconds)
targetHalfWidthPct = deployWidthSigmaMultiple * sigmaHorizon
targetHalfBins     = ceil( ln(1 + targetHalfWidthPct) / ln(1 + binStep / 10_000) )

width  = clamp( 2 * targetHalfBins + 1, MIN_BINS_PER_POSITION, envelopeBins )
```

applied in this fixed order, so the same inputs always yield the same plan:

1. Convert both walls to bin ids per §2a and §3a, inward-rounded (lower ceil, upper floor). That
   interval is the **envelope**.
2. **Reject** if the envelope is inverted, or if `envelopeBins < MIN_BINS_PER_POSITION`. A wall
   interval too narrow to hold a legal position is not a range to widen — widening would leave a
   wall, which §5 forbids.
3. **Reject** if the reconciled active bin lies outside the envelope. §4's containment check already
   catches this at the actuator; catching it here as well means an unplaceable range never reaches
   the execution boundary.
4. Compute `width` by the clamp above.
5. Place a window of exactly `width` bins containing the active bin, centred on it, shifted inward
   only as far as required to stay inside the envelope. **Tie rule:** an odd remainder goes to the
   lower side first. This is what keeps the placement deterministic when the active bin sits near a
   wall.

`sigma` is the same volatility input `ev_policy.md` consumes, and `horizonSeconds` is the same deployment horizon.
Since [[adr-047-provisional-sigma-estimator|ADR-047]] (TICKET Z Part B), `sigma` is the [[adr-047-provisional-sigma-estimator|ADR-047]] chain: trailing 24 h σ of 300 s spot returns, then trailing
6 h, then the labelled placeholder while the root's in-memory history warms up. `SIGMA_SOURCE=placeholder` is the kill
switch back to the pre-ADR-047 input (`realizedVol1m_t` when a port supplies it, else the placeholder). The root
computes σ once per tick (`PlanningSigma`), and the gate's plan, the logged plan and the deploy dispatch's re-plan all
read it. The macro FSM's `realizedVol1m_t` is a separate input and is not fed from it. The width
is recomputed per plan from the then-current inputs; it is never frozen into a constant.

#### Why a volatility-derived width rather than a fixed cap

A **bin cap** is not an economic statement. Sixty-nine bins is 2.76% of price at 4 bps and 55% at
80 bps, so a bin-count rule would mean something different on every pool — and it would import a
transaction-shaped limit into a question about where price goes. A **fixed percentage** is
pool-independent but introduces a bare constant with no derivation behind it, which is the failure
mode this repository keeps paying for.

A volatility-derived width is different in one decisive respect: **it is wrong in a self-correcting
direction.** If volatility is higher than assumed the range widens, which is what a wider price
excursion requires. A fixed cap is wrong in an unknown direction. And because `sigma` is already
measured by the observation archive, the width becomes correct when `sigma` is ratified, with no
further planning decision.

#### `deployWidthSigmaMultiple` is UNRATIFIED

Introduced by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] and labelled in the same terms as the EV placeholders, because it is a policy
choice and not a measurement. **Default 1.**

Two things the ratifier must know. First, the conservative directions conflict: a *small* multiple
concentrates liquidity and raises fee yield per unit, while a *large* one keeps price inside the
range for longer. There is no direction that is safe on both counts, which is why this cannot be
settled by choosing carefully. Second, **a ±1σ band is not a 68% chance of staying in range.** That
figure describes the *terminal* distribution; the probability that a path never leaves the band
during the horizon is materially lower. So a multiple of 1 will show a lower in-range fraction than
its label suggests, and the honest expectation is that ratification moves it above 1.

`observation_archive.md` §6 question 3 — the fraction of wall-clock time the active bin remained
inside a range of width *W*, across a range of *W* — measures exactly the path property this
multiple encodes. That question is the ratifier, and it needs no bin window, only the `active_bin_id`
series.

#### What the rule does to the two geometries this repository has measured

| | 4 bps mainnet target | 80 bps Devnet |
| --- | --- | --- |
| wall envelope | ~940 bins | 47 bins (soak15) |
| σ-derived width at multiple 1 | **203 bins** | 13 bins |
| which constraint binds | **σ** | the **20-bin floor** |
| deployed width | **203 bins** | **20 bins** |
| bin arrays touched | 3 (was 14) | 1 |
| chunked transactions | 3 (was 14) | 1 |

Both cases are deployable and neither is wall-to-wall. On the coarse pool the floor binds, which is
worth stating plainly: there, the **transaction minimum** sets the width, not economics. On the fine
pool σ binds and the walls never come into play, since the Put and Call walls sit 347 and 538 bins
from the active bin against a σ half-width of 101.

#### The width rule is necessary and not sufficient

Narrowing 940 bins to 203 reduces the bin arrays touched from 14 to 3, but **3 uninitialized arrays
still cost `0.0434 + 3 × 0.0714 = 0.2577 SOL`, above [[adr-030-deployment-sol-reserve|ADR-030]]'s ratified `0.25 SOL` reserve.** Even
the tightest defensible width breaches it. [[adr-030-deployment-sol-reserve|ADR-030]]'s constant was sized against at most two
uninitialized arrays, so it must become width-aware; that is a reserve decision and [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] routes it
to its own ADR rather than settling it here.

#### What the implementation ticket must carry

This is a design amendment; the code change is a separate ticket. Three requirements travel with it:

- **A negative `activeBinId` case.** The target pool's active bin was `-5311` at verification, where
  every soak in this repository ran at `+1110`. The planner carries no sign bug today — its only
  non-negative guard is `isUsableDecimals`, which validates decimals and is correct — but no
  committed test outside the observation suite exercises a negative active bin through width
  selection, containment and chunking. A Devnet fixture at `+1110` cannot catch a sign error on the
  only pool that matters.
- **A case for each of §2b's two rejections**, and one where the floor binds and one where σ binds,
  so the clamp's branches are all covered rather than only the fine-pool path.
- **The tie rule pinned by test**, since a window placed near a wall is where a non-deterministic
  remainder would show up first.

#### Where the reserve evidence comes from, and where it does not

The array-count and rent figures in this section are **account-size arithmetic**, the method [[adr-030-deployment-sol-reserve|ADR-030]]
itself used: a `BinArray` is 10,136 bytes with a rent-exempt minimum of 71,437,440 lamports, and the
`0.0434 SOL` base was measured at the 2026-09-19 13:14 soak on a 22-bin range whose arrays already
existed.

They are **not** taken from the observation archive, and cannot be. The recorder ships with
`cost_observations` wired end to end but its venue reader returns empty — decoding another
participant's deployment transaction into a trustworthy `bin_count` was out of its ticket's scope,
and `observation_archive.md` §5c declares an empty stream legitimate. The archive's useful evidence
for *this* decision is the `active_bin_id` series and nothing else; a width-aware reserve must be
settled by the arithmetic above or by a deliberate Devnet experiment that crosses uninitialized
arrays, as the 13:14 soak did by accident.

#### The planner owns width; the executor owns chunking

These are separate concerns and must not be conflated. The planner emits **one aggregate range** of
the derived width. `MAX_BINS_PER_POSITION = 69` is a per-transaction limit that `chunkBinRange`
applies afterwards, and it is **not** a width rule — `chunkBinRange` handles 940 bins correctly, in
14 legal chunks. The defect was never in chunking.

---

## 3. Deterministic bin conversion

The planner must map the two validated wall bounds to DLMM bin identifiers through one
deterministic conversion rule supplied by the execution boundary's pool metadata.

The resulting plan must include lower and upper quote bounds, lower and upper bin ids, and the
zero-gamma context used for the plan. The same walls and pool metadata must always yield the
same bin range. Rounding, clamping, and tie behavior must be explicit and unit-tested.

### 3a. The unit contract — walls are per-token, bins are per-base-unit ([[adr-022-range-planner-numeraire-alignment|ADR-022]])

The conversion spans two different units, and until [[adr-022-range-planner-numeraire-alignment|ADR-022]] it silently assumed they were one.

A **GEX wall** is a price in **quote tokens per whole base token** — the unit a human quotes a
strike in. Meteora's **bin geometry** is a ratio of **base units**: bin `i` sits at
`(1 + binStep / 10_000) ^ i` lamports-to-quote-base-units. Those two agree only when the pool's
two mints carry the same number of decimals. The binding conversion is therefore:

```text
binId = log(price * 10^(quoteDecimals - baseDecimals)) /
        log(1 + binStep / 10_000)
```

- `price` is a wall in quote tokens per whole base token
- `baseDecimals` and `quoteDecimals` are **required pool metadata**, carried on the reconciled
  `SolanaPoolStateSnapshot`. They are not defaulted, not inferred, and not read from the
  environment at this boundary — the snapshot already holds the pool's own values
- **equal decimals preserve the prior formula exactly**: the factor is `10^0 = 1`, so every
  existing bin id is unchanged
- unusable metadata is rejected deterministically. It is never approximated, and 9/6 is never
  assumed

Inward rounding is unchanged and remains **lower ceil, upper floor** (§5 forbids widening past a
wall, and inward rounding can only narrow the deployed interval).

**This is the exact inverse of the active-bin price `ev_policy.md` §5a fixes** for the EV gate:

```text
quotePerWholeBase = (1 + binStep / 10_000) ^ activeBinId * 10^(baseDecimals - quoteDecimals)
```

The two must stay inverses of each other. A pool priced one way and planned the other places
liquidity at prices no wall approved, and the offset is not subtle — on the Devnet pool
(`binStep = 80`, 9 base decimals, 6 quote decimals) the missing factor displaces every bin id by
`3 * ln(10) / ln(1.008)`, about **867 bins**. See [[adr-022-range-planner-numeraire-alignment|ADR-022]] and [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]].

---

## 4. Boundary output

Range Planning emits a pure deployment plan. It does not return a transaction and does not
hold a DLMM client. The deployment actuator consumes the plan and confirms that the selected
bins remain valid against freshly reconciled Solana pool state before submitting a transaction.

**Active-bin containment is part of that confirmation ([[adr-023-range-planner-devnet-scaling-and-containment|ADR-023]]).** Before constructing,
simulating, signing or sending any transaction, the actuator must verify that the reconciled
active bin lies inside the planned range, inclusive of both bounds:

```text
plan.lowerBinId <= pool.activeBinId <= plan.upperBinId
```

A plan that does not contain the active bin describes liquidity that is entirely out of range
at the moment of deployment: it earns no fees, and it is the observable signature of a planner
fed prices in the wrong unit. The check is cheap, it is the last thing standing between a
mis-scaled plan and committed capital, and a failure must be reported as its **own** reason —
distinct from a bin-step mismatch, an unavailable pool read, or an oversized transaction —
because those send an operator somewhere else entirely.

Equality with either bound is containment. The active bin sitting on the edge of the range is a
deployable position, not a boundary error.

---

## 5. Data-flow and prohibitions

```text
marketdata -> state -> intelligence -> decision -> risk -> execution
```

- Do not deploy a range without both valid wall anchors.
- Do not widen bounds beyond the Put and Call walls.
- Do not use zero gamma as a substitute for a missing wall.
- Do not open an RPC client or submit a transaction from this module.
- Do not rely on non-deterministic bin rounding or input iteration order.
- Do not convert a USD wall to a bin id without first scaling it into pool quote units (§2a).
- Do not substitute a perpetual mark price, or any venue price other than the pool's own
  active-bin price, for the scaling numerator.
- Do not deploy, simulate, or build a transaction for a plan that does not contain the
  reconciled active bin (§4).
- Do not deploy the full wall-to-wall interval as a range without applying §2b's derived width. On a
  fine-binned pool that interval is not a concentrated position.
- Do not widen a range to reach `MIN_BINS_PER_POSITION` by leaving a wall. If the envelope cannot
  hold a legal position, reject (§2b step 2).
- Do not use `MAX_BINS_PER_POSITION` as a width policy. It is a per-transaction limit applied by the
  chunker after planning (§2b).
- Do not treat `deployWidthSigmaMultiple` as ratified, or substitute a bare percentage or bin count
  for the volatility derivation (§2b).

These prohibitions are binding.
