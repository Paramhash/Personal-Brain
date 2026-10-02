---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- blueprint
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/architect/ev_policy.md
bot_commit: e532796
source_sha256: 8a70e6e842406406bc097c8a1115414101220a2790d30a11d1b089921461f0e9
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/architect/ev_policy.md` at commit `e532796`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# EV Policy

**Domain owner:** Expected-value gating, projected fees, projected LVR, and friction budgeting
**Status:** authored and binding
This blueprint owns the expected-value gate used by decision and orchestration layers.

---

## 1. Scope

This blueprint governs:

- projected fee forecasting inputs consumed by `EVALUATING`
- projected LVR use in forward EV gating
- realized LVR use in monitoring and audit
- the canonical friction-budget inequality applied before capital movement

It does not own macro regime transitions, hedge sizing, or execution sequencing.

---

## 2. Dual-mode LVR rule

LVR is a two-mode metric and the modes must not be collapsed:

- `EVALUATING` uses forward-looking `projected_lvr_quote`
- `MONITORING` uses realized `realized_lvr_quote`

Operationally:

- `projected_lvr_quote` is the ex-ante drag term priced into deployment or redeploy decisions
- `realized_lvr_quote` is the ex-post audit and monitoring term written for attribution

The forward gate must never substitute a backward-looking realized average in place of
`projected_lvr_quote`.

**The σ in `projected_lvr_quote` ([[adr-047-provisional-sigma-estimator|ADR-047]], TICKET Z Part B).** A realized σ used as the *input* to the forward term
is permitted, as before; what is forbidden is realized *LVR* standing in for projected LVR. The root passes the [[adr-047-provisional-sigma-estimator|ADR-047]]
chain's σ (trailing 24 h → 6 h → placeholder), and the range planner uses the same value (`range_planning.md` §2b).
`SIGMA_SOURCE=placeholder` restores the placeholder. The EV input field is still named `realizedVol1m_t`, holds a
**per-second** σ, and is filled by the root; the macro FSM's own `realizedVol1m_t` input is not.

---

## 3. Canonical EV payload rule

The canonical EV payload fields are:

- `projected_dynamic_fees`
- `projected_lvr_quote`
- `projected_hedge_drag_quote` ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]])
- `binance_funding_drag`
- `swap_slippage`
- `gas_fees`
- `deploy_rent_sunk`
- `net_ev`
- `gate_pass`

Feature modules may consume this payload, but they may not rename or reinterpret these
fields ad hoc.

### 3a. `deploy_rent_sunk` — the sunk cost of establishing the range ([[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]])

`deploy_rent_sunk` is the portion of [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]'s deployment reserve that is **never returned**, priced
in the pool's quote asset: bin-array rent plus transaction fees for the planned bin range.

**Only the sunk portion belongs here.** Position-account and ATA rent are refunded when the accounts
close, so they are withheld working capital rather than expense; they belong in the [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] reserve
and must not be charged against expected value. Charging them would overstate the cost roughly as
badly as omitting the sunk portion understated it, which is the defect **F-026** records: before
[[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] the only Solana cost in this payload was `gas_fees`, and sunk bin-array rent is **three
orders of magnitude larger** than the value that term carried.

**The term scales with range width**, because rent does: a range wider than
`MAX_BINS_PER_POSITION` is chunked into several position accounts, and a wider range crosses more
bin arrays. Omitting it therefore made wider ranges look cheaper than they are — the direction
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] §2b and [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] both push, which is what made the omission dangerous rather than merely
incomplete.

**An absent plan is zero, not unknown.** Rent is a cost of a *prospective* deployment, so where no
range has been planned there is nothing to charge. This is the one term that does **not** follow
§5b's unknown-cost discipline, and the asymmetry is deliberate: funding drag is a carry cost of the
position that already exists, so an unpriceable one must refuse, whereas an unknown-cost sentinel
here would assert that a deployment nobody proposed is unaffordable. The macro reducer consults this
gate for hold and exit decisions too, so that assertion drives an exit. Where a range **is** planned
and its cost cannot be derived, the term takes an unknown-cost sentinel as §5b requires.

**Amortization is a policy choice and is UNRATIFIED.** Bin-array rent is paid once per array ever, so
it is the cost of *establishing* a price range rather than a per-deployment toll — charging it in full
against one deployment overstates the cost for a range that will be redeployed into, and charging
nothing understates it for one abandoned after a single use. `deployRentAmortizationDeployments`
defaults to `1` — charge in full — because that is the end that can only refuse a marginal
deployment, never admit one that should have been refused.

### 3b. Range-dependent LVR and hedge drag ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]])

`projected_lvr_quote` and `projected_hedge_drag_quote` are priced for the **planned range**. Before [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]], LVR was
full-range `σ²/8` times a constant 1.8, at any width, and the hedge had no term at all. On the 2026-10-01 live window
that put the gate's hurdle at 62.5 bps/day, against a simulated break-even of about 270–330.

Both terms come from one function, `rangeCostRates` (`src/intelligence/range/hurdleMath.ts`). The research simulator's
§F and [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]]'s model call the same function, so the gate, the hurdle display and the evidence cannot drift apart.

```text
σ_pool       = σ · poolSpotSigmaRatio · m_regime                       σ: the per-tick PlanningSigma (§2)
ρ̄            = life-averaged value density of the planned range         closed form (below)
LVR_bps_day  = 1e4 · ½ · σ_pool,d² · ρ̄                                  σ_pool,d = σ_pool · √86 400
s            = V · ρ̄ · σ_pool,d / p                                    base inventory s.d. per day
s_Δ          = s · √(Δt / 86 400)                                      per hedge check
turnover     = poolBurstFactor · s² / max(ε, s_Δ · √(π/2))              base per day
hedge_bps_day = 1e4 · τ_taker · p · turnover / V
term_quote   = rate_bps_day / 1e4 · V · horizon_hours / 24
```

The inputs:
- **ρ̄** weights each bin's share of the position's value (the shape's weights, `dlmmStrategyType`) by how long
  driftless price is expected to spend in it before leaving the range. That time is the occupation density of Brownian
  motion started at the active bin and killed at the range edges: a tent, `g(u) = (u − a)·b` for u ≤ 0 and
  `(−a)·(b − u)` for u ≥ 0. Spot gives ρ̄ = ρ(0); the live Curve window gives ρ̄ ≈ 0.71 ρ(0).
- **`poolSpotSigmaRatio` (0.88) and `poolBurstFactor` (0.74)** are measured properties of the pool, owned by
  `strategy.config.ts` and UNRATIFIED (`config_contract.md` §5):
  - the simulated position moves with the pool, whose 30 s σ is 0.88× Deribit spot's;
  - the pool's active bin is unchanged in about half of 30 s checks, so its mean absolute move is 0.74× a Gaussian's of
    the same variance.
- **`m_regime` is 1** ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D3) until the regime multipliers are measured.
- **V, p, ε, Δt and τ_taker:**
  - V is `deployableNotionalQuote`;
  - p is the §5a active-bin price;
  - ε is `epsilonBase`;
  - Δt and τ_taker are EV placeholders in `evCalculator.ts`.

**Calibration** (TICKET 028 Part 0, `todo/findings/EV_GATE_CALIBRATION_2026-10-01.md`): run against the simulator's
exact accounting, with the realized pool σ, Curve model ÷ simulator is 0.98 for LVR and 0.97 for hedge drag. Every UTC
day falls within ±50%. [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D2's form test is that comparison, and the research report re-runs it. Whether the
trailing σ forecasts the realized σ is [[adr-047-provisional-sigma-estimator|ADR-047]]'s question, not this section's.

**No plan is zero; an unpriceable plan refuses.** This follows §3a's reasoning for rent, by the dispatcher's
2026-10-01 decision:
- **No plan** (`deployBinRange === null`): both terms are 0. The macro reducer consults this gate for hold and exit, so a
  refusal on a tick with no plan would withdraw a held position for want of a GEX signal.
- **A plan that exists but cannot be priced** (no pool snapshot, no pool price, an empty range, or the active bin outside
  it): both terms take `UNKNOWN_RANGE_COST`, which is large and finite on the `UNKNOWN_DEPLOY_RENT_SUNK` reasoning.

σ itself is never missing: §2's chain ends at the placeholder.

---

## 4. Canonical EV hurdle

The EV hurdle is binding across the repository:

```text
net_ev >= 1.5 * (swap_slippage + gas_fees)
```

This rule is owned by `src/config/strategy.config.ts` and must not be redefined in
feature modules, reducers, or execution paths.

**[[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]] did not change this inequality, and the placement of `deploy_rent_sunk` is why.** The
right-hand side is a *friction budget*: the multiplier is a margin of safety over terms that are
**estimates** of variable execution cost. Sunk rent is neither estimated nor variable — it is exact
lamport arithmetic over published rent constants — so it needs no safety multiple, and applying one
would penalise a known cost more heavily than an unknown one. `deploy_rent_sunk` is therefore
subtracted inside `net_ev`, alongside the carry costs, leaving this inequality textually unchanged.
Adding a term to its right-hand side would have been the redefinition §6 forbids.

**[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] placed `projected_hedge_drag_quote` inside `net_ev` for the same reason.** Hedge drag is a carry cost that
scales with time and capital, like LVR and funding, not an execution friction:

```text
net_ev = projected_dynamic_fees − projected_lvr_quote − projected_hedge_drag_quote − binance_funding_drag − deploy_rent_sunk
```

The inequality above is unchanged.

`ev_policy.md` owns the semantics of the inequality; `strategy.config.ts` owns the
ratified numeric constant surface consumed by code.

---

## 5. Price-base and numeraire discipline

Projected and realized LVR must be stored and compared in the same quote-denominated
numeraire used by EV and PnL accounting.

If fees arrive in token units, convert them before EV comparison. The gate must not mix
token-denominated fees and quote-denominated LVR or friction terms.

### 5a. Which quote — the AMM terms are priced by the pool ([[adr-020-ev-numeraire-active-bin-pricing|ADR-020]])

"The same quote-denominated numeraire" names a rule but not a unit, and the unit is where this
went wrong. **The numeraire for an AMM-facing term is the DLMM pool's own quote asset**, and the
base side of such a term must be converted to it at the pool's **active-bin price**:

```text
quotePerWholeBase = (1 + binStep / 10_000) ^ activeBinId * 10 ^ (baseDecimals - quoteDecimals)
```

That is the inverse of the canonical Meteora conversion `range_planning.md` §3 already fixes,
with the decimal factor that converts a base-unit ratio into a per-token price. Both inputs come
from the reconciled Solana snapshot; no other price source is admissible for these terms.

**A perpetual's mark price is not this numeraire.** It denominates the venue's own quote asset,
which is the same asset only when the pool happens to quote in it. Pricing DLMM base inventory
at `binance.mark_price_t` and adding the result to a pool-token balance is a violation of §5
whether or not the two assets coincide — on a SOL/USDC mainnet pool they do, which is precisely
why the error survives inspection and only surfaces on a pool that quotes in something else.

The rule applies to every term whose quantities come from the pool — today
`projected_dynamic_fees` and `swap_slippage`, through the deployable notional both are computed
from. It did **not** silently extend to terms whose quantities come from the perpetual venue.
Those were brought in by the ADRs that addressed them: `gas_fees` by [[adr-028-ev-calculator-zero-inventory-support|ADR-028]], and
`binance_funding_drag` by [[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]] in §5b below.

### 5b. Funding drag is a pool-quote term, and an unknown funding cost refuses ([[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]])

**Every value term on the payload is now in one numeraire.** `binance_funding_drag` is the last
one that was not. It is computed by valuing the hedged base exposure at the pool's active-bin
price — the §5a conversion, reused and never restated — and multiplying by the Binance funding
rate and the horizon's funding periods. The funding **rate** stays a perp fact and needs no
conversion: it is a dimensionless fraction, so it carries no numeraire. `binance.mark_price_t` is
**not** an input to this term, and moving it must not move any pool-quote quantity.

This is an approximation and is recorded as one. The cost is genuinely incurred in the perp's
quote asset, and converting it exactly would need a perp-quote-to-pool-quote rate that no
admissible source supplies — importing a third venue's price is the mixing §5 forbids. Valuing
the hedged *quantity* at the pool's price states the same exposure in the payload's numeraire,
exactly when the two quote assets coincide or are pegged. It replaces a dimensional error with a
stated assumption, which is an improvement and not a claim of exactness.

**Which facts make the term known.** A Solana snapshot, a derivable pool price, a Binance
snapshot that is not stale, and a finite funding rate. A rate of exactly `0` is **known** —
funding is genuinely zero at times, and refusing on a value the venue supplied would be a
different error. A **negative** rate stays signed and raises `net_ev`, because a short that is
paid funding earns it; that benefit is admitted only when every fact above is valid.

**An unknown funding cost fails the gate, arithmetically.** Funding drag is a cost, so replacing
an unknown one with zero raises `net_ev` and lets the gate pass because the pipeline did not know
the cost — not because the economics were favourable. The term instead evaluates to a sentinel
large enough that `net_ev` cannot clear the §4 hurdle. That keeps the refusal inside the ratified
inequality: §6 forbids a second rule, and `if (facts missing) gate_pass = false` would be one.
The sentinel is finite rather than infinite so the payload still serializes as a number, because
the diagnostic matters most on precisely the tick that refused.

**Fail closed on a missing pool price.** §5 is a rule about *which* numeraire, so a pool price
that cannot be derived is a numeraire that is not available, and the affected terms evaluate to
zero. Substituting another venue's price is the mixing this section forbids, and doing it as a
fallback performs it exactly when the pipeline is least able to notice.

---

## 6. Prohibitions

- Do not use `realized_lvr_quote` in `EVALUATING`.
- Do not use `projected_lvr_quote` as a monitoring attribution metric.
- Do not redefine the EV hurdle multiplier outside `strategy.config.ts`.
- Do not let execution modules invent a second EV rule for the same capital movement.
- Do not feed the [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model **hurdle** (its lifespan-amortized total), or any venue-API fee yield, into
  `computeEvDecision` without a ratifying ADR (§7). [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] ratified only the model's LVR and hedge-drag terms (§3b).
- Do not replace `PLACEHOLDER_FEE_YIELD_PER_HORIZON` with a Route 4 measured value while [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] Amendment 1 stands.
- Do not price DLMM base inventory at a perpetual venue's mark price, and do not fall back to one
  when the pool's active-bin price cannot be derived (§5a).
- Do not add a base amount converted at one venue's price to a quote balance denominated in
  another's, even when the two assets are expected to be the same.

---

## 7. Hurdle rate — a restatement and a model ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]])

Two figures in bps of capital per day, and **only the first is the gate**.

- **Gate hurdle** — `hurdleFromEvDecision` (`src/decision/ev/hurdleRate.ts`): the projected fee yield at which §4 is
  met exactly, `(lvr + funding + rent + k·(slip + gas)) / (capital · horizon)` with `k` read from
  `strategy.config.ts`. `projected fee ≥ gate hurdle ⇔ gate_pass`, pinned by test. It is an inversion of §4, not a
  second rule, and a refusing sentinel in any term (§3a, §5b) makes it refuse.
- **Model hurdle** — `computeHurdleRate`, over the equations in `src/intelligence/range/hurdleMath.ts`.
  - The terms: width- and shape-dependent LVR, hedge re-balancing drag (turnover capped by the check interval), signed
    funding, and fixed costs amortized over an expected first-exit lifespan.
  - A per-regime σ multiplier adjusts it.
  - **UNRATIFIED, display and research only.** It is never an input to `computeEvDecision`. Where funding is not read
    (the monitor), it is excluded from the model total and labelled; the gate's §5b refusal is unaffected.

**What may consume which.** `evaluateDeploymentGate` copies `gate_pass` and adds no condition. The edge and its ratio
are displayed and never gated; a required margin would be a change to §4's constant by ADR. Venue-API fee yield
([[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]) is display-only and never a projected-fee input; the gate's fee input stays the placeholder until [[adr-033-fee-yield-measurement-route|ADR-033]]
ratifies one.

**Ratification path** ([[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §5): research report §F (the model against the simulator's exact accounting, per policy
and per day) and §G (measured regime σ multipliers), then an ADR that replaces the placeholder estimators. At adoption
the model sat 1.05–3.0× above the simulator's LVR and 0.9–3.3× its hedge cost — conservative, and closest for wide
windows.

**[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] took that path for the LVR and hedge terms (2026-10-01).**
- **The cause of the over-statement:** it came from ρ(0) and from reading σ and the move distribution from Deribit
  rather than from the pool.
- **The model now** uses `rangeCostRates` (§3b): ρ̄, `poolSpotSigmaRatio` and `poolBurstFactor`. Its LVR and hedge-drag
  rates are the gate's own.
- **What stays model-only:** the lifespan-amortized fixed costs and the regime multipliers, which are all 1.
