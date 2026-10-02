---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/F-026 - The EV gate has no rent term, so wider ranges look cheaper than they are.md
bot_commit: 3f1eec9
source_sha256: 838cc6eaa706c213593f4b7a92b6909723f06ebda26193cc58f4c60933fbed13
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/F-026 - The EV gate has no rent term, so wider ranges look cheaper than they are.md` at commit `3f1eec9`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# F-026 — The EV gate has no rent term, so wider ranges look cheaper than they are

**Status: CLOSED 2026-09-27 by [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]].** Implemented and verified: 847/847 tests, `tsc --noEmit` clean.
**Raised:** 2026-09-27, while grounding [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]'s reserve arithmetic. Found by checking whether rent
reaches the EV gate, not by any failure — nothing has failed, because no capital has deployed.
**Type:** missing cost term in a gate that authorises capital. Not a defect in what is implemented; the
implemented terms are correct, and a term that should exist does not.

## The gap

`src/decision/ev/evCalculator.ts` takes its Solana cost through a single injected estimator, `gasFees`,
backed by:

```ts
export const PLACEHOLDER_DEPLOY_LAMPORTS = 200_000;   // 0.0002 SOL
```

Its comment is accurate about what it covers — "a chunked deploy plus its re-ratio swap is on the order of
ten transactions, and priority fees dominate under load" — and it is labelled UNRATIFIED. The problem is
what it does **not** cover. **There is no rent term anywhere in the EV inputs.** Deployment rent is not a
transaction fee, is not estimated by any of the five injected estimators, and does not appear in the
inequality.

## Why that matters, quantitatively

[[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] establishes that a deployment's rent scales with range width, and that the **bin-array** portion
is permanently sunk — bin arrays are program-owned shared state the depositor never closes, so whoever
first initialises one pays for it and nobody gets it back. Position and ATA rent are recoverable on close
and are correctly excluded from EV as working capital. The sunk portion is not.

Measured at the pool's live active bin (−5280, 4 bps), worst case where every touched array is
uninitialised:

| Plan width | Sunk bin-array rent | Versus the 0.0002 SOL placeholder |
| --- | --- | --- |
| 203 bins (today's σ-derived width) | 0.2857 SOL | **1,429×** |
| 940 bins ([[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] envelope bound) | 1.0001 SOL | **5,001×** |

The gate that decides whether a deployment is worth making is therefore blind to the largest sunk cost of
making it, by three orders of magnitude.

## The direction of the error is the dangerous part

The omission is not neutral. Rent grows with width, so **omitting it makes wider ranges look cheaper than
they are** — and widening is exactly what [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] §2b and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] both do. The two decisions that were
adopted to make the strategy deploy sensibly are also the two that inflate the missing term. A gate biased
toward the change being made will not catch the case where the change costs more than it earns.

[[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] does not fix this, and must not be read as fixing it. A reserve is a **funding** guard: it refuses
deployments the wallet cannot pay for. It says nothing about whether a deployment the wallet *can* pay for
is worth making. Those are different questions with different failure modes, and only the first is covered.

## Why no failure has been observed

No capital has deployed. `docs/status/current.md` records the EV estimators as uncalibrated placeholders,
so the gate has never been the binding constraint on a real deployment. This finding is therefore
pre-emptive: it describes a defect that becomes live the moment the estimators are calibrated and capital
is authorised, which is precisely when it would be most expensive to discover.

## Next steps

1. **Add a sunk-rent term to the EV inputs**, computed from the plan by the same arithmetic [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]
   ratified, and taking **only** the bin-array and fee components. Position and ATA rent must stay out:
   they are recoverable, and counting them would overstate the cost as badly as omitting array rent
   understates it.
2. **Decide how to amortise it.** Bin-array rent is paid once per array ever, so charging it in full
   against a single deployment's EV overstates the cost for a range that will be redeployed into, and
   charging nothing understates it for a range abandoned after one use. This is a policy question, not an
   arithmetic one, and it should be recorded as UNRATIFIED with whatever default is chosen.
3. **Separate the placeholder.** `PLACEHOLDER_DEPLOY_LAMPORTS` currently reads as "the Solana cost of
   deploying", which is how the rent omission stayed invisible. Rename it to name only what it covers —
   transaction and priority fees — so the absence of a rent term is legible at the call site.
4. **Make it scale with chunk count.** The placeholder is flat, but a 940-bin plan is 14 transactions
   against a 20-bin plan's one. Whatever replaces it should take the chunk count the same way the reserve
   now does.
5. **Do not calibrate the estimators or authorise capital until 1–3 are done.** This is the ordering that
   matters: the gap is harmless while no capital moves and becomes a direct capital risk the moment it does.

---

## Closure, 2026-09-27 — [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]]

All five next steps are done, and step 2's policy question is recorded as UNRATIFIED rather than
silently defaulted.

1. **Sunk-rent term added.** `deploy_rent_sunk` joins `ev_policy.md` §3, computed by
   `src/config/deployRentModel.ts` from the plan's bin range and carrying **only** bin-array rent plus
   fees. Position and ATA rent are excluded as this finding required.
2. **Amortization decided and labelled.** `deployRentAmortizationDeployments = 1` — charge in full —
   **UNRATIFIED**, chosen because it is the end that can only refuse a marginal deployment, never admit
   one that should have been refused. It is not an estimate of redeployment frequency.
3. **Placeholder renamed.** `PLACEHOLDER_DEPLOY_LAMPORTS` is now
   `PLACEHOLDER_DEPLOY_TX_LAMPORTS_PER_CHUNK`, naming only what it covers.
4. **It scales with chunk count.** Per chunk, with `PLACEHOLDER_DEPLOY_CHUNKS_UNKNOWN = 10` preserving
   the old magnitude when no range is planned, so an unplanned deployment is never costed cheaper.
5. **Ordering honoured** — this landed before any calibration or capital authorisation.

### What the fix also settled, which this finding did not anticipate

The term's **placement** turned out to be the substantive question, not its existence. It is subtracted
inside `net_ev` at 1.0x rather than added to §4's friction budget at 1.5x: the multiplier is a safety
margin over *estimates* of variable cost, and sunk rent is exact arithmetic over published constants.
That placement also leaves §4's ratified inequality textually unchanged, which §6 requires
independently.

### And one error this finding's framing invited

Implementing "an unknown cost must refuse" by analogy with [[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]] was wrong for this term. Returning
the unknown-cost sentinel when **no range had been planned** drove the macro FSM to `UNWINDING` —
caught by four orchestrator tests. Funding drag is a carry cost of a position that already exists;
rent is the cost of a deployment that might happen, and a sentinel there asserts that a deployment
nobody proposed is unaffordable. Since the macro reducer consults the gate for exit as well as entry,
that assertion liquidates a healthy position. An absent plan now charges **zero**; only a *planned*
range whose cost cannot be derived takes the sentinel.

### Not closed by this, and deliberately so

The EV estimators remain uncalibrated placeholders. This finding was about a **missing term**, not an
inaccurate one, and adding it does not make the gate an economic judgment. `docs/status/current.md`
continues to carry that caveat.
