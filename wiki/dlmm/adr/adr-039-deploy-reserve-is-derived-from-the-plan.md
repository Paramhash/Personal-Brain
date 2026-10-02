---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-039
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/039-deploy-reserve-is-derived-from-the-plan.md
bot_commit: aebf1c0
source_sha256: ccd4130e4fa3daf03b366da0c873da0f9d3f9e68cb481e1d23420cf40bae25de
exported_at: '2026-10-02T12:50:26Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/039-deploy-reserve-is-derived-from-the-plan.md` at commit `aebf1c0`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] — The Deployment Reserve Is Derived From the Plan, Because a Fixed Constant Cannot Cover a Cost That Scales With Range Width

- **Date:** 2026-09-27
- **Status:** **Active. Ratified by the dispatcher 2026-09-27.** It changes when a deployment is refused for funding, which is a capital-affecting guard.
- **Ratified with prerequisite 1 taken on its second branch:** the minimum viable wallet is **explicitly left open**, not decided. Guidance sufficient to close it later is recorded under "What wallet this implies". Nothing in this ADR depends on the answer.
- **Supersedes:** **[[adr-030-deployment-sol-reserve|ADR-030]] Decision 2** (the reserve is a fixed `0.25 SOL` constant). [[adr-030-deployment-sol-reserve|ADR-030]]'s Decision 1 (policy: never spend the whole base balance) and Decision 3 (reject `INSUFFICIENT_SOL_RESERVE` before construction) are **retained unchanged** — this ADR changes only how the reserve is *computed*.
- **Amends:** `liquidity_position_manager.md` §3a.
- **Driver:** [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] §2b and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] both widen the deployed range, and neither re-derived the reserve. Flagged as an open cost by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]], and recorded again as an unresolved cost when [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] was ratified on 2026-09-27.

## Context: the reserve was correct for a world that no longer exists

[[adr-030-deployment-sol-reserve|ADR-030]] sized `0.25 SOL` against a **single** position of at most 69 bins touching at most two uninitialized bin arrays. That was the whole deployment shape on 2026-09-19. Two later decisions changed the shape without revisiting the constant:

- **[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] §2b** replaced "deploy the wall envelope" with a σ-derived window, making the deployed width a function of measured volatility rather than a fixed 20–69 bins.
- **[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]** widened the envelope that clamps it — from a median 402 bins under the old wall definition to roughly the 103–150 price span, which at the pool's 4 bps bin step is **940 bins**.

Two costs scale with that width, and the reserve accounts for neither.

**First, width creates positions, not just bins.** `transactionLimits.MAX_BINS_PER_POSITION = 69`, and `executeDlmmDeploy` calls `chunkBinRange` to split any wider plan into multiple chunks — **each of which creates its own position account, with its own rent.** The reserve is a single flat quantity subtracted once, and the guard runs *before* chunking, so it cannot know how many position accounts the plan will create. [[adr-030-deployment-sol-reserve|ADR-030]]'s arithmetic contains exactly one position's rent because on 2026-09-19 there was only ever one.

**Second, width crosses bin arrays.** A bin array holds `MAX_BIN_ARRAY_SIZE = 70` bins, and every array the range touches that does not yet exist must be rent-funded.

## Measurement

The cost model is taken from the Meteora SDK's own published constants rather than inferred, and the Solana rent formula `(128 + data_len) × 3480 × 2` reproduces `BIN_ARRAY_FEE` exactly — which is what licenses using that formula for the account sizes the SDK does not publish a fee for.

| SDK constant | SOL | Covers |
| --- | --- | --- |
| `POSITION_FEE` | 0.05740608 | one position account |
| `BIN_ARRAY_FEE` | 0.07143744 | one uninitialized bin array |
| `TOKEN_ACCOUNT_FEE` | 0.00203928 | the idempotent ATA |
| `BIN_ARRAY_BITMAP_FEE` | 0.01180416 | bitmap extension, beyond ±512 array indices |

Cost at the pool's live active bin (−5280, 4 bps), under the 69-bin chunking the code actually performs. "Worst" assumes every touched array is uninitialized; "best" assumes all already exist. **Both columns are rent plus base fees only — they exclude `DEPLOY_RESERVE_MARGIN_BASE`**, which adds a flat 0.01 SOL to the reserve actually charged (so the 203-bin worst case is 0.4599 as rent, 0.4699 as reserve).

| Plan width | Positions | Position rent | Arrays | Array rent | Worst | Best | vs 0.25 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 20 bins (`MIN_BINS_PER_POSITION`) | 1 | 0.0574 | 1 | 0.0714 | **0.1308** | 0.0594 | 0.52× — ok |
| 69 bins ([[adr-030-deployment-sol-reserve|ADR-030]]'s world) | 1 | 0.0574 | 2 | 0.1429 | **0.2023** | 0.0594 | 0.81× — ok |
| 203 bins (σ-derived, `deployWidthSigmaMultiple = 1`) | 3 | 0.1721 | 4 | 0.2857 | **0.4599** | 0.1741 | **1.84× — BREACH** |
| 1142 bins (full [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] envelope) | 17 | 0.9750 | 17 | 1.2144 | **2.1915** | 0.9770 | **8.77× — BREACH** |

Three things follow.

**The breach is real and already live.** The σ-derived window is the width §2b produces today, and its worst case needs 1.84× the reserve.

**The 940-bin row is the true worst case but not the expected one.** §2b clamps the deployed width to the envelope, so reaching 940 bins requires σ to grow roughly 4.6×. It is a volatility-spike bound, not a daily one.

**The reserve still holds whenever the touched arrays already exist**, which on an established pool is common. That makes the failure intermittent and conditional on pool state — the worst possible shape for a funding bug, because it passes in testing and fails on the first range extension into virgin arrays.

**[[adr-030-deployment-sol-reserve|ADR-030]]'s own worst case was also understated, independently of any of this.** It computed 186,273,160 lamports from a measured 43,398,280 treated as position-plus-ATA rent. But the ATA is 2,039,280, leaving 41,359,000 for the position account — **below the SDK's `POSITION_FEE` of 57,406,080.** Recomputed from SDK constants, [[adr-030-deployment-sol-reserve|ADR-030]]'s own scenario costs 202,269,560 lamports (0.2023 SOL), so the claimed "roughly 34% margin" was closer to 24%. The conclusion survives — 0.25 did cover one position — but the margin was never what the record said.

## Most of the reserve is a recoverable deposit, and that changes the affordability claim

The reserve is a single quantity the wallet must hold at deploy time, so the arithmetic above is unaffected by this section. But its *terms* have different economic lives, and conflating them overstates the cost.

- **Position-account rent is recoverable.** Closing a position returns its rent to the owner. It is withheld working capital, not an expense.
- **ATA rent is recoverable** on the same basis.
- **Bin-array rent is permanently sunk.** Bin arrays are program-owned shared state that the depositor never closes, so whoever first initializes an array pays for it and no one gets it back.
- **Base and priority fees are sunk**, and small.

| Plan width | Recoverable | Sunk (worst) | Total | Sunk share |
| --- | --- | --- | --- | --- |
| 20 bins | 0.0594 | 0.0814 | 0.1408 | 57.8% |
| 69 bins | 0.0594 | 0.1529 | 0.2123 | 72.0% |
| 203 bins | 0.1741 | 0.2958 | 0.4699 | 62.9% |
| 1142 bins | 0.9770 | 1.2245 | 2.2015 | 55.6% |

**This softens the affordability conclusion and sharpens the cost one.** Roughly 37–44% of the reserve is a deposit that comes back on close, so the strategy is less capital-starved than the headline withholding figure suggests. But the sunk share is **the majority of the reserve at every width**, and it is sunk in a specific way that matters: **bin-array rent is paid once per array, ever.** It is therefore a one-time cost of *establishing* a price range, amortized across every future deployment into it — not a recurring per-deployment toll. The 7.22× figure is the cost of first entry into virgin territory, and re-deploying into the same range later costs only the recoverable terms.

That amortization is real but it must not be used to wave the cost away, for two reasons. Widening a range is exactly the act that touches virgin arrays, so **the cost lands precisely when [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] are doing their job**. And a range abandoned after one deployment never amortizes anything.

## The EV gate does not know about any of this

**`evCalculator` has no rent term.** Its only Solana cost input is `gasFees`, backed by `PLACEHOLDER_DEPLOY_LAMPORTS = 200_000` (0.0002 SOL) — transaction fees only, and flat regardless of chunk count. The sunk bin-array rent is **1,429× that placeholder at 203 bins and 5,001× at 940 bins.**

So the gate that decides whether a deployment is worth making is blind to the largest sunk cost of making it, and blind in a direction that **makes wider ranges look cheaper than they are** — which is the direction [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] both push. This ADR does not fix it: the reserve is a funding guard, and a funding guard that refuses unaffordable deployments is not a substitute for an EV term that prices affordable ones correctly. Recorded as **F-026**.

## Decision

**The reserve is computed from the plan, as pure arithmetic over published constants, with no RPC.**

```text
reserve = Σ_chunks rent(positionSize(chunkBins))          // one term per position account
        + arraysTouched(lowerBinId, upperBinId) × BIN_ARRAY_FEE
        + TOKEN_ACCOUNT_FEE
        + chunkCount × baseTransactionFee
        + DEPLOY_RESERVE_MARGIN_BASE                       // priority fees and compute budget
```

where `positionSize(n) = POSITION_MIN_SIZE` for `n ≤ DEFAULT_BIN_PER_POSITION`, else `POSITION_MIN_SIZE + (n − DEFAULT_BIN_PER_POSITION) × POSITION_BIN_DATA_SIZE`, and `arraysTouched` is `floor(upper/70) − floor(lower/70) + 1` **using floor division, not truncation** — the pool's bin ids are negative, and truncating toward zero undercounts.

Four constraints on that formula:

1. **Assume every touched bin array is uninitialized.** This is the only term that genuinely needs chain state, and assuming the worst keeps the whole computation pure. It over-reserves on an established pool — up to 0.2857 SOL on the 203-bin case — and that cost is accepted deliberately, because [[adr-030-deployment-sol-reserve|ADR-030]] Decision 3 requires rejecting an underfunded wallet *before* touching the network, and a reserve that needs an RPC round trip to be correct cannot do that.
2. **Chunk before reserving.** The guard currently runs ahead of `chunkBinRange`; it must now run after it, because the chunk count is an input to the cost. This does **not** weaken [[adr-030-deployment-sol-reserve|ADR-030]] Decision 3: `chunkBinRange` is pure arithmetic over the plan, so the guard still precedes every pool read, `buildChunkTransaction`, simulation, and signature. The ordering that mattered is preserved; only the ordering within the pure prefix changes.
3. **`DEPLOY_SOL_RESERVE_BASE` becomes a floor, not the value.** The operator override is retained on the [[adr-026-devnet-tolerance-and-timeout-adjustments|ADR-026]] precedent with the same fail-closed parsing, but it now raises a derived reserve and cannot lower it. An operator able to set the reserve *below* the arithmetic can reintroduce the 2026-09-19 failure by configuration, and this guard exists precisely to make that unreachable.
4. **`DEPLOY_RESERVE_MARGIN_BASE` is UNRATIFIED.** Priority fees are market-dependent and nothing here measures them. Default `0.01 SOL`, labelled on the same terms as `deployWidthSigmaMultiple` and `callWallAccumulationFraction`. The rent terms are exact; this one is a guess and must be visible as one.

## Consequences

**The deployable-capital consequence is the important one, and it is strategic rather than technical.** The reserve stops being a fixed toll and becomes a function of range width, so **a wider plan is a more expensive plan**. At the σ-derived 203 bins the worst-case reserve is 0.4599 SOL; on the 1.266 SOL wallet from [[adr-030-deployment-sol-reserve|ADR-030]]'s soak that withholds **36% of the base side**, against the roughly 20% [[adr-030-deployment-sol-reserve|ADR-030]] recorded. At the 940-bin envelope bound the reserve alone exceeds that wallet entirely. **[[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]'s widened envelope and [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s σ width may therefore have made the strategy unaffordable at the wallet sizes previously assumed**, and this ADR is what makes that visible instead of letting it surface as a simulation failure. Choosing the minimum viable wallet is a separate question this ADR deliberately does not answer.

**More deployments will be refused, and the refusals are correct.** A wide plan on a thin wallet now fails closed with `INSUFFICIENT_SOL_RESERVE` at preflight. That is the same named rejection as today, so nothing downstream must learn a new reason — but its frequency will rise, and it must not be read as a fault.

**The reserve is no longer a single auditable number.** [[adr-030-deployment-sol-reserve|ADR-030]]'s constant could be checked by reading one line; a derived reserve is only as good as its arithmetic, and it sits on the path to signing. It therefore requires unit tests pinning each row of the measurement table above, including the negative-bin-id floor division, which is the one term where a plausible implementation is silently wrong in exactly the direction that under-funds.

**Width remains uncoupled from wallet balance, deliberately.** It is tempting to cap the planned width by what the wallet can afford. That would make `range_planning.md` depend on reconciled wallet state, crossing the `intelligence -> decision` arrow that §5 fixes, so the planner continues to plan on market inputs alone and execution continues to refuse what cannot be funded.

## What wallet this implies

Prerequisite 1 is left open, so this is guidance rather than a decision. Wallet size needed for the derived reserve to stay within a given share of the base balance:

| Plan width | Reserve | ≤40% | ≤25% | ≤10% |
| --- | --- | --- | --- | --- |
| 203 bins (today's σ width) | 0.4699 | 1.17 SOL | 1.88 SOL | 4.70 SOL |
| 940 bins (envelope bound) | 1.8151 | 4.54 SOL | 7.26 SOL | 18.15 SOL |

The 1.266 SOL wallet [[adr-030-deployment-sol-reserve|ADR-030]] was soaked against sits just past the ≤40% column for today's width and nowhere near it for the envelope bound. **Whoever closes this question should decide the share, not the wallet** — the share is a policy statement that survives future width changes, whereas a wallet figure silently expires the next time σ or the envelope moves.

## Alternatives rejected

- **Raise the constant to cover the worst case.** It would have to be about 1.81 SOL to cover a 940-bin envelope, withholding roughly 10× what the common case needs and destroying deployable capital in every ordinary deployment. It also preserves the actual defect — a constant cannot track a cost that scales with width, so the next width change breaks it again, silently.
- **Keep 0.25 SOL and cap the deployed width at 69 bins.** This funds the reserve by discarding [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]], both adopted on evidence. It trades a funding bug for a strategy regression.
- **Query rent exemption per account at dispatch.** [[adr-030-deployment-sol-reserve|ADR-030]] rejected this for needing live RPC inside the sizing path, and that objection still stands. Worth recording that it does **not** apply to this ADR: the rent amounts are computable from published constants, and the only chain-dependent term is handled by assuming the worst.
- **Read which bin arrays exist, to avoid over-reserving.** Genuinely more accurate, and it would recover up to 0.2857 SOL on the 203-bin case. Rejected *for now* because it costs an RPC round trip before the guard and makes the guard's correctness depend on a fetch that can fail. Revisit if over-reservation is shown to be the binding constraint on deployable size — but it must degrade to the conservative figure on any fetch failure, never to a cheaper one.
- **Catch the insufficient-lamports error and retry smaller.** Rejected by [[adr-030-deployment-sol-reserve|ADR-030]] and still rejected: the guardrails forbid catching it, and it would convert a funding fault into silent size drift.

## Ratification prerequisites

1. **A decision on the minimum viable wallet, or an explicit acceptance that the question stays open** — **discharged on the second branch, 2026-09-27.** The question is open by decision, not by omission. "What wallet this implies" records the arithmetic needed to close it, and the recommendation that the answer be expressed as a *share* rather than a SOL figure.
2. **Nothing else.** The rent terms are derived from published constants and verified against [[adr-030-deployment-sol-reserve|ADR-030]]'s own `BIN_ARRAY_FEE` figure, so unlike [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] this ADR needed no new measurement before ratification.

## Correction, 2026-09-27 — the envelope row was computed on the wrong put wall

The bottom row of both tables was computed over a **103–150** envelope, taken from [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]'s own text. That
text was wrong: 103 is the put-side *extremum*, and the ratified accumulation rule selects **95** on the same
capture. The true full envelope is **95–150 — 1142 bins, not 940** — and the rows above have been corrected
to 17 positions, 17 bin arrays, and **2.1915 SOL worst case (8.77× the superseded reserve)**.

Three things this does not change. The **203-bin σ row is untouched**, and it is the row that matters today —
the breach that is live is still 1.84×. The **decision** is unaffected, and in fact strengthened: a fixed
constant tracks a width-scaled cost even less well than recorded. And the **direction** of every consequence
below is the same, with the worst case simply worse than stated.

It does sharpen one argument. "Raise the constant to cover the worst case" was rejected partly because it
would need to be about 1.81 SOL; the real figure is **2.19 SOL**, and the fact that this number moved by 21%
on a corrected input is itself evidence for deriving the reserve rather than pinning it.

## Annotation, 2026-09-27 — the envelope row is superseded once [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]]'s buffer is in force

TICKET R implements [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]]'s buffered envelope, and the envelope is the ceiling in [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]'s clamp and
therefore in this ADR's cost model. Lowering the ceiling lowers the worst case. At the ratified
`wallBufferRoomFraction = 0.25`, on the 2026-09-27 surface:

| | Envelope | Positions | Arrays | Recoverable | Sunk | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Raw [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] envelope — the row above | 1142 bins | 17 | 17 | 0.9770 | 1.2145 | **2.1915 SOL** |
| **Buffered (`k = 0.25`) — operative once R lands** | ~852 bins | 13 | 13 | 0.7476 | 0.9288 | **1.6763 SOL** |

**The worst case falls about 23.5%, and nothing else changes.** The deployed window stays at 207 bins because
σ still binds, so no position, reserve or EV term moves at today's volatility — this is purely a reduction in
the *ceiling* the reserve must be able to cover.

**This annotation does not change this ADR's reserve policy.** The reserve is still derived from the plan, the
formula is unchanged, and the **203-bin σ row — the breach that is actually live at 1.84x — is untouched.**
What changes is only which row is the worst case: the buffered envelope replaces the raw one as the widest
plan the planner can now produce.

Recorded here because this table has already been corrected once for using a stale envelope (the 940-bin row
computed from [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]'s misstated put wall), and a second stale worst case would be the same mistake twice.

## Implementation, 2026-09-27 — at dispatcher instruction

Implemented and verified the same day. **Suite 930/930 across 31 suites** (923 + 7 new), `tsc --noEmit` clean.
**No build was run**: `dist/` backs the running archive recorder and `dist-recon/` backs TICKET T, so this change
reaches a running binary only at the next deliberate build.

- `config/deployRentModel.ts` — `deployReserveLamports(range, maxBinsPerPosition, marginLamports)`: [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]]'s
  `deployRentBreakdown` total plus the margin. It reuses the rent model, so the reserve and the EV rent term cannot
  disagree about positions or arrays.
- `config/strategy.config.ts` — `DEPLOY_RESERVE_MARGIN_BASE = 0.01` (UNRATIFIED). `DEPLOY_SOL_RESERVE_BASE` is now
  resolved by `resolveDeploySolReserveFloorBase` as a **floor**, `null` when absent. `DEPLOY_SOL_RESERVE_DEFAULT`
  (0.25) is removed: a default floor of 0.25 would have kept the superseded constant in force for every plan cheaper
  than it (the 20- and 69-bin rows), which is the thing this ADR replaces.
- `execution/solana/dlmmDeploy.ts` — `executeDlmmDeploy` chunks first (constraint 2), then applies
  `deployReserveXAmount = max(derived, floor)`, still before any pool read. The request carries `baseDecimals` and
  converts lamports to base units rounding **up**, instead of assuming a base unit is a lamport. An unpriceable plan
  is refused as `INSUFFICIENT_SOL_RESERVE`.
- `execution/adapters/liveAdapters.ts` — passes the floor and the base decimals.
- `liquidity_position_manager.md` §3a amended as this ADR requires.

**Tests pin every row of the measurement table** against the printed values, not against the module's own
arithmetic: 20 / 69 / 203 / 1142 bins reproduce 0.1308 / 0.2023 / 0.4599 / 2.1915 SOL + 0.01 margin at the live
active bin. Also pinned: the 203-bin breach (> 1.8× the old 0.25), negative-bin floor division (−5270..−5250 costs
exactly one more `BIN_ARRAY_FEE` than −5290..−5271; truncation would count one array), the floor raising and never
lowering, decimals conversion rounding up, and an unpriceable plan refused before anything is built.
