---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-033
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/033-fee-yield-measurement-route.md
bot_commit: 93d497d
source_sha256: 011d8980b7abf298d6e6fef21f44e40326713b399a5adf46426126b79f4f7141
exported_at: '2026-10-02T12:50:26Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/033-fee-yield-measurement-route.md` at commit `93d497d`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-033-fee-yield-measurement-route|ADR-033]] — Fee Yield Is Measured by Direct Accrual on a Small Mainnet Position, and Ratified as a Conservative Floor

- **Date:** 2026-09-25
- **Status:** Active. **The capital gate this route requires is UNAPPROVED.**
- **Context:** `PLACEHOLDER_FEE_YIELD_PER_HORIZON = 0.001` is labelled in its own source comment as "UNRATIFIED, and the single most consequential number in this file … not derived from this pool's observed volume, because nothing in the pipeline observes volume yet." The gate is linear in it, so the sensitivity table in the ticket is a statement about the decision boundary: 10 bps/day passes, 6 bps/day fails. Solving the canonical inequality at the soak14/soak15 notional of 17,189,612 quote units gives the boundary exactly — **the gate requires ≈7.38 bps/day**, so the placeholder carries only **35% headroom** over the value at which the verdict flips. [[adr-032-observation-archive-ownership-and-isolation|ADR-032]] gave the archive an owner, a schema and gap semantics but deliberately left the measurement route open, and `SolanaPoolStateSnapshot` still carries no fee field, so no route is currently implemented. A second fact discovered while deciding this route materially constrains it: **79% of that 7.38 bps threshold is itself built from unratified constants.** Decomposed, the threshold is 3.81 bps of projected LVR (from `PLACEHOLDER_SIGMA_1S_STDDEV` and `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER`, both UNRATIFIED), 2.04 bps of hurdle (from a slippage *cap* rather than an expectation, and `PLACEHOLDER_DEPLOY_LAMPORTS`), and only 1.53 bps of funding, which is the one measured term. Because `placeholderProjectedLvrQuote` computes `((σ² × 3600) / 8) × multiplier × horizon × notional`, the threshold is **quadratic in σ**: at 1.5× the assumed σ the threshold becomes 12.14 bps/day and the current placeholder fails regardless of what fee yield turns out to be.
- **Decision:** **Route 3 — direct accrual on a small real position on the intended mainnet SOL/USDC pool.** Fee accrual is read from the position itself and recorded into the [[adr-032-observation-archive-ownership-and-isolation|ADR-032]] archive as `fee_observation.route: POSITION_ACCRUAL`, with cumulative `fee_base_cumulative` / `fee_quote_cumulative` counters and the observed `position_liquidity_share`. Route 3 is selected because it is the only route that measures the quantity the gate actually consumes — fee accrual on a real position, in a real range, net of the protocol fee share, across both token sides, with the dynamic fee component included and at the position's true liquidity share — as a single observed number requiring no transaction decoding, no liquidity-share model and no interpolation. Fee yield is a *rate*, so a small position measures it as faithfully as a large one. **Selecting the route does not authorize the position.** The capital gate is separate, is listed below, and remains unapproved.
- **Consequences:** The archive's other three series — spot for σ, `bins[]` for the concentration multiplier, `cost_observations` for deploy lamports — are route-independent and can begin recording immediately under [[adr-032-observation-archive-ownership-and-isolation|ADR-032]] with `fee_observation: null`, which is why [[adr-032-observation-archive-ownership-and-isolation|ADR-032]] made the field nullable from schema version 1. Fee measurement itself cannot begin until the capital gate opens, so the recording start date and the fee-measurement start date differ and the archive must tolerate that; it does, by construction. The costs are real and are accepted: mainnet capital at market risk for the measurement window, a mainnet signer, custody of a live position, and a dependency on preconditions that do not exist yet. Because σ is quadratic in the threshold and comes free from the same run, a fee-yield measurement alone cannot settle the gate verdict — the ratification path below therefore requires a two-dimensional sensitivity surface rather than the one-dimensional table that motivated this ticket. `PLACEHOLDER_FEE_YIELD_PER_HORIZON` is unchanged by this ADR, and `ev_policy.md` §6's single-EV-rule prohibition is untouched: all conservatism introduced here lives in a constant's *value*, never in a second rule.
- **Alternatives rejected:**
  - **Route 1 — reserve-delta inference. Rejected as unboundable, per the ticket's own instruction.** Reserve changes confound swaps with LP adds and removes, and the confound cannot be separated from reserve snapshots alone, because the LP flow that would separate it is precisely what a reserve delta cannot see. It is also *systematically biased low* at any practical cadence: a swap that moves price out and back within one sampling interval nets to approximately zero reserve change while having earned fees in both directions. An error that is unbounded in magnitude and biased in a known direction cannot be presented as calibrated yield.
  - **Route 2 — swap-transaction parsing. Rejected, and it was the closer call.** It measures *pool* volume correctly, which is the wrong quantity by one step: the gate needs what a position in a given range earns. Bridging that gap requires attributing each swap's volume to the bins it crossed, which requires the bin state at that swap's slot — and the archive samples bin liquidity at 30 s, so per-swap attribution is not reconstructable from it. The resulting share model's error therefore lands in the **same magnitude band as the decision boundary**: the gate flips on a 35% change in fee yield, which is well inside the error of a share model built on 30-second liquidity snapshots. A measurement whose error is as large as the margin it is meant to resolve does not resolve it. RPC cost is a secondary objection but not a small one — a busy mainnet SOL/USDC DLMM pool transacting 10k–100k times a day implies roughly 200k–2M `getTransaction` calls over 21 days, on a paid endpoint.
  - **Deferring the decision until the archive has run.** Rejected: the route determines whether a signer, a funded wallet and a guard fix are on the critical path, and all three have lead times measured in weeks. Deciding late would not preserve optionality, it would only start the clock later.

---

## What this route does not measure

Stated explicitly, per the ticket's Part 2. Route 3 measures position-specific fee accrual — not pool volume and not an inference. It captures the dynamic fee component, protocol-fee deductions and both token sides, because it reads what the position actually received. It does **not** establish the following, and none of these may be presented as measured:

1. **Transfer across ranges.** The measurement is taken in one range. Fee yield per unit of in-range liquidity depends on bin width and on placement relative to the active bin. A yield measured in a 47-bin range does not license the same constant for a 22-bin range.
2. **Transfer across volatility and volume regimes.** One window is one regime. This is the residual the ratification threshold below exists to constrain, and it cannot be removed by any route.
3. **Own-liquidity dilution — the measurement is an upper bound.** At measurement size the position's share of its bins is negligible, so it measures the **marginal** yield. A materially larger deployment dilutes its own share and earns strictly less per unit of liquidity. This is the single strongest reason the ratified value must be a conservative floor rather than the measurement itself.
4. **Range-selection quality, unless normalized.** Fees accrue only while the price is in range. Raw accrual over wall-clock time conflates fee yield with how well the range was chosen, so yield **must** be normalized by in-range time, using only `OK` samples per `observation_archive.md` §7.
5. **What a hedged position nets.** LVR and funding drag are separate EV terms with separate inputs. This route measures the reward term only.

**Residual `UNRATIFIED` estimates introduced by this route: none.** That is the reason it was chosen. Items 1–3 are limits on generalization, constrained by the threshold rules below and by the conservative floor, not new free parameters. The pre-existing `UNRATIFIED` constants — σ, the concentration multiplier, deploy lamports and the horizon — are untouched and remain labelled as they are.

---

## Ratification threshold, fixed before any data is collected

- **Minimum observation window: 21 consecutive days at ≥95% coverage**, and this is a floor, not a sufficiency claim. Three complete weeks is the shortest window that contains the weekday/weekend structure of crypto volume more than twice and yields seven non-overlapping 3-day sub-windows to test stability against. **The stability criterion, not the duration, is the gate** — 21 days that fail it are not ratifiable, and the answer is a longer window.
- **Sub-window stability.** Partition the window into seven non-overlapping 3-day sub-windows. Ratification is blocked if the ratio of highest to lowest sub-window yield exceeds **3×**, or if any sub-window's coverage is below 95%. A sub-window below coverage is excluded from the stability test and **reported** rather than dropped silently.
- **The ratifiable quantity is the 10th-percentile sub-window yield, not the mean.** The gate is a go/no-go on capital, and a mean-based constant passes the gate in roughly half the periods where the true yield would not support it. Blind spot 3 above independently requires the same direction.
- **Regime treatment: ratify a single conservative value.** Regime covariates — realized σ from the spot series, pool volume, and the in-range fraction — are recorded and reported as conditional yields, but a conditioned constant introduces a model with its own unratified parameters and would trade one guess for several. Conditioning is escalated to only if the stability criterion fails, and then as its own ADR.
- **Coverage and gaps.** Yield is computed as cumulative fees over total in-range `OK`-sample time, which is why `observation_archive.md` §5b requires cumulative counters. Intervals whose fee difference spans a gap are excluded from per-interval statistics and retained in the cumulative total, marked by `delta_spans_gap`. No published figure omits its coverage ratio.
- **If the measured floor is below the level the gate needs: the strategy is not deployed.** The threshold is not renegotiated after seeing the result. Three specific renegotiations are pre-closed: the placeholder is not raised to meet the gate; the hurdle multiplier is not reduced; and **the horizon is not lengthened**, which `PLACEHOLDER_HORIZON_HOURS`'s own comment already identifies as improving the verdict monotonically and therefore as the obvious way to rescue a failing gate by tuning.

---

## Ratification path

- **Follow-up artifact:** a further ADR amending `ev_policy.md` with a ratified fee-yield subsection carrying the value and its provenance. That ADR, not this one, moves the constant.
- **Re-running the sensitivity analysis: as a two-dimensional surface over (fee yield, σ), not the one-dimensional table.** This is required rather than preferred, because 79% of the gate threshold comes from unratified constants and LVR is quadratic in σ — at 1.5× the assumed σ the threshold reaches 12.14 bps/day and no plausible fee yield saves the verdict. σ is measured by the same archive run at no additional cost, so presenting a one-dimensional table would assert a precision the inputs do not have.
- **The placeholder is replaced by a conservative floor, not by the measured mean.** `ev_policy.md` §6 forbids a second EV rule, so the conservatism lives in the constant's value. The ratified constant is the 10th-percentile sub-window yield.
- **Required evidence:** the `observer_run_id` set; the UTC date range; coverage ratio per sub-window and overall; the seven sub-window yields; the in-range fraction; the derivation of the floor; and the measured σ used in the surface.
- **Rollback.** Ratification is not permanent and the archive keeps recording after it. If realized yield falls below the ratified floor for three consecutive sub-windows, a further ADR revises the constant downward and the gate is re-evaluated. A ratified constant whose provenance can no longer be traced to retained raw samples is void, per `observation_archive.md` §9.
- **The exact point at which a measurement becomes a strategy constant:** when the amending ADR is accepted **and** `src/config/strategy.config.ts` carries the value. Until both are true the placeholder stands, labelled UNRATIFIED. No ADR arising from this ticket authorizes a live mainnet deployment of the strategy.

---

## Capital gate — UNAPPROVED

Route 3 requires mainnet capital. **This ADR does not approve it.** Approval is a separate, explicit, written decision by the human operator, and these preconditions must be satisfied first. They are not currently satisfied.

1. **The bot has never broadcast a transaction.** Across all fifteen Step 6 soaks, `sendRawTransaction` count is 0 and every result exposing a signature reports `signature: null`. The first live broadcast in this project's history must be demonstrated **on Devnet**, not on mainnet with real capital.
2. **The capital-return path has never run live.** `dlmmWithdraw.ts` has no committed live execution. Proving the position can be closed and funds recovered precedes opening one.
3. **The mainnet guard gap must be closed first.** `productionEndpointsIn` exists at `adapter.config.ts:163` but is called only from tests, and `assertNonProductionDefaults` — named in its own doc comment as the caller — does not exist in `src/`. There is therefore **no runtime enforcement** preventing a mainnet endpoint, and `PRODUCTION_HOST_MARKERS` holds only `api.mainnet-beta.solana.com`, so the paid endpoint this route assumes would not trip it even once wired. Route 3 deliberately places a mainnet RPC URL and a funded signer in one environment; the guard must exist, and must allowlist deliberately rather than merely fail to match.
4. **A dedicated wallet holding only measurement capital**, never a wallet that could later hold more.
5. **The measurement position is inert with respect to the trading FSM.** It must not be opened, rebalanced, withdrawn from or otherwise managed by the bot. A position under FSM control can be withdrawn mid-window by a defensive trigger, which would destroy the series it exists to produce. The measurement position is operated by a dedicated one-shot path or manually.
6. **A stated capital amount, and a size floor with a reason.** The position must be large enough that per-interval accrual is well above the smallest representable token unit at 6 quote decimals and 9 base decimals, and small enough that its loss is immaterial. The amount is named in the capital approval, not here.
7. **Monitoring and a manual kill path**, including the operator check that the position is still in range and still accruing.

The capital at risk during the window is exposed to market movement — an unhedged DLMM position carries LVR. This is not a fee-only exposure and must not be approved as one.
