---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-040
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/040-sunk-deployment-rent-is-an-ev-term.md
bot_commit: 3f1eec9
source_sha256: 89b5d567841b04b5a8477572f5693827f5a56e61b503270994f4235a8fe041fa
exported_at: '2026-10-02T12:50:26Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/040-sunk-deployment-rent-is-an-ev-term.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] — Sunk Deployment Rent Is an EV Term, Subtracted Inside `net_ev` Rather Than Added to the Friction Budget

- **Date:** 2026-09-27
- **Status:** Active. Implemented and verified the same day; 847/847 tests pass and `tsc --noEmit` is clean.
- **Amends:** `ev_policy.md` §3 (new canonical field, new §3a) and §4 (a note on why the inequality is unchanged).
- **Consequential for:** [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]], whose rent arithmetic this reuses, and [[adr-030-deployment-sol-reserve|ADR-030]], whose reserve [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] superseded.
- **Driver:** **F-026**, raised while grounding [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]'s reserve arithmetic. Not found by any failure — no capital has deployed, so nothing had the chance to fail.

## Context

`evCalculator` had **no rent term**. Its only Solana cost input was `gasFees`, backed by a flat
`PLACEHOLDER_DEPLOY_LAMPORTS = 200_000` (0.0002 SOL) covering transaction fees. [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] established
that a deployment also pays rent scaling with range width, and that the **bin-array** portion is
permanently sunk — bin arrays are program-owned shared state the depositor never closes, so whoever
first initialises one pays for it and nobody gets it back.

Measured at the pool's live active bin (−5280, 4 bps), worst case where every touched array must be
created, sunk bin-array rent is **1,429×** the old placeholder at the σ-derived 203-bin width and
**5,001×** at the 940-bin [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] envelope bound. The gate authorising capital was blind to the
largest sunk cost of moving it, by three orders of magnitude.

**The direction of the error is what made it dangerous.** Rent grows with range width, so omitting it
made wider ranges look cheaper than they are — and widening is exactly what [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] §2b and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]
both do. A gate biased toward the change being made cannot catch the case where that change costs
more than it earns.

## Decision

**1. `deploy_rent_sunk` joins the `ev_policy.md` §3 canonical payload**, priced in the pool's quote
asset by §5a's active-bin converter — the same converter `gas_fees` uses, because rent is a SOL cost
and the comparison is in the pool's quote asset.

**2. Only the sunk portion is charged.** `deployRentModel` splits the cost by economic life, and this
term reads `sunkLamports` — bin-array rent plus fees. Position-account and ATA rent are refunded on
close, so they are withheld working capital and belong in the [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] reserve but not in EV. Charging
them would overstate the cost roughly as badly as omitting the sunk portion understated it.

**3. It is subtracted inside `net_ev`, not added to the §4 hurdle's right-hand side.** This is the
decision's substance. The right-hand side is a *friction budget*, and its 1.5 multiplier is a margin
of safety over terms that are **estimates** of variable execution cost. Sunk rent is neither
estimated nor variable — it is exact lamport arithmetic over published rent constants — so it needs
no safety multiple, and applying one would penalise a known cost more heavily than an unknown one.
The placement also leaves §4's ratified inequality textually unchanged, which matters independently:
§6 forbids redefining the hurdle outside `strategy.config.ts`, and adding a term to its right-hand
side would have been exactly that.

**4. An absent plan charges zero, not the unknown-cost sentinel.** Rent is a cost of a *prospective*
deployment, so with no planned range there is nothing to charge. This is the one cost term that does
not follow §5b's unknown-cost discipline, and the asymmetry is deliberate — see below.

**5. The fee placeholder is renamed and made to scale.**
`PLACEHOLDER_DEPLOY_LAMPORTS` becomes `PLACEHOLDER_DEPLOY_TX_LAMPORTS_PER_CHUNK = 20_000`, charged
per chunk. The old name read as "the Solana cost of deploying", which is how the absence of a rent
term stayed invisible for the life of the module; the new name covers only what it is. With no plan,
`PLACEHOLDER_DEPLOY_CHUNKS_UNKNOWN = 10` reproduces the previous 200,000 magnitude, so an unplanned
deployment is never costed cheaper than before this change.

**6. `MAX_BINS_PER_POSITION` moves to `src/config/strategy.config.ts`**, re-exported from
`transactionLimits.ts`. The rent model needs the chunk width to know how many position accounts a
plan creates, and `src/decision/ev/` reads that model; importing it from `execution/` would invert
§5's `decision -> execution` arrow. This is the resolution TICKET O already applied to
`MIN_BINS_PER_POSITION`.

## Why an absent plan is zero — the mistake worth recording

The first implementation returned the unknown-cost sentinel when no range had been planned, by
analogy with [[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]]'s treatment of unknown funding drag. **That analogy is wrong, and four
orchestrator tests caught it**: the macro FSM went to `UNWINDING` on ticks whose only fault was that
no range had been planned.

Funding drag is a carry cost of the position that **already exists**, so it always applies and an
unpriceable one must refuse. Rent is a cost of a deployment that **might happen**. Returning a
sentinel there does not express caution — it asserts that a deployment nobody proposed is
unaffordable, and because the macro reducer consults this gate for hold and exit decisions as well as
entry, that assertion drives an exit. A gate that liquidates a healthy position because it could not
price a hypothetical deployment is worse than the omission being fixed.

This cannot let a deployment through unpriced. `dispatchDeploy` refuses on `plan === null` before any
capital moves, and both the tick-level gate and the deploy dispatch now pass the planned range, so a
deployment actually being evaluated always has one. Where a range **is** planned and its cost cannot
be derived, the term takes the sentinel, as §5b requires.

## Two smaller details that are load-bearing

**The sentinel is `MAX_SAFE_INTEGER`, not `MAX_VALUE`.** `UNKNOWN_FUNDING_DRAG` already uses
`MAX_VALUE`, and `net_ev` now subtracts both terms. Two `MAX_VALUE` costs in one sum give
`-Infinity`, which JSON serialises as `null` and destroys the diagnostic on exactly the tick that
refused — the failure `UNKNOWN_FUNDING_DRAG`'s own docblock exists to prevent. A second sentinel of
the same magnitude would have reintroduced it.

**`binArraysTouched` uses floor division, not truncation.** The pool's bin ids are negative, and
`Math.trunc(-5280 / 70)` is −75 where the array index is −76. Truncation undercounts arrays at
negative bin ids, in the direction that under-funds, and would fail at signing rather than in a test.

## Consequences

**A recorded signal changed.** `EvDecisionPayload` gained a field and `net_ev` changed meaning, so
**no EV or `gate_pass` series is comparable across this change**, exactly as [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]]'s wall series
are not. Any analysis spanning it must say so.

**The gate is now harder to pass, correctly.** A deployment must earn its permanent cost of
establishing the range, not merely its transaction fees. At the σ-derived width that is 0.2857 SOL of
sunk rent in the worst case, where the previous term charged 0.0002.

**`deployRentAmortizationDeployments` is UNRATIFIED at `1`.** Charging the one-time array rent in
full against a single deployment overstates the cost for a range that will be redeployed into;
charging nothing understates it for one abandoned after a single use. `1` is the conservative end —
it can only refuse a marginal deployment, never admit one that should have been refused — and it is
**not** an estimate of redeployment frequency, which nothing measures yet.

**The reserve and the EV term must not be confused.** [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]'s reserve is a *funding* guard: it
refuses deployments the wallet cannot pay for. This term prices deployments the wallet *can* pay for.
Fixing one never fixes the other, and F-026 exists because the reserve work made it tempting to think
otherwise.

## Alternatives rejected

- **Fold rent into `gas_fees`.** Minimal diff, and wrong twice: it puts an exact cost inside the 1.5
  friction multiple, and it re-buries rent inside a term named for fees — which is the very
  concealment that let F-026 survive as long as it did.
- **Add a term to the §4 hurdle's right-hand side.** Redefines the ratified inequality outside
  `strategy.config.ts`, which §6 forbids, and applies a safety multiple to a known quantity.
- **Charge the full reserve, recoverable rent included.** Overstates the cost by roughly the
  recoverable share — 37% at 203 bins — and misprices a refundable deposit as an expense.
- **Read which bin arrays already exist, to charge only the ones actually created.** More accurate,
  and rejected for the same reason [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] rejected it: it needs an RPC round trip, and the gate must
  remain computable from reconciled facts already in hand. It must also degrade to the pessimistic
  figure on any fetch failure, never a cheaper one.
- **Leave it until the estimators are calibrated.** The omission is harmless only while no capital
  moves, and calibration is precisely the moment capital starts moving. Fixing it afterwards means
  the first real deployments are the ones priced wrong.
