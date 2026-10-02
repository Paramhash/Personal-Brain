---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- adr
aliases:
- ADR-046
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/docs/decisions/046-real-time-hurdle-rate-restates-the-ev-gate.md
bot_commit: e532796
source_sha256: 18d31784123993e07fc11de284cd35fa5771263ec1251ab01cc0d95e5f741345
exported_at: '2026-10-02T12:50:27Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/docs/decisions/046-real-time-hurdle-rate-restates-the-ev-gate.md` at commit `e532796`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] — A Real-Time Hurdle Rate (bps/day) Restates the EV Gate and Models Its Costs; It Is Not a Second Gate

- **Date:** 2026-09-29
- **Status:** **Active. Decided by the dispatcher 2026-09-29**, including the four departures from the request listed
  in §6. Drafted from the request *"Implement Real-Time Dynamic Hurdle Rate (BE_bps_day) Monitor and Pre-Trade Gating
  Check"*. Implementation: TICKET W.
- **Owns (when Active):** `ev_policy.md` §7 (new), `src/decision/ev/hurdleRate.ts`; display in `monitor.md` §4.
- **Cross-references:** [[adr-015-fsm-cold-start-and-ev-gate|ADR-015]] (EV gate), [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]]/031 (numeraire, funding), [[adr-033-fee-yield-measurement-route|ADR-033]] (fee-yield route), [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]
  (σ width), [[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]]/040 (rent), [[adr-043-research-simulator-reads-archive-offline|ADR-043]] (research simulator), [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] (+ amendment: Orca stats are display-only).

## 1. Context

The research simulator ([[adr-043-research-simulator-reads-archive-offline|ADR-043]]) ranks policies by **break-even yield on capital, bps/day** — the fee yield at which
a policy's costs are covered. The live EV gate answers the same question in different units: it computes

```text
net_ev = projected_dynamic_fees − projected_lvr_quote − binance_funding_drag − deploy_rent_sunk
gate_pass ⇔ net_ev ≥ 1.5 × (swap_slippage + gas_fees)                               (ev_policy.md §4)
```

over a 24 h horizon, so **the gate already has an implicit hurdle rate**: the fee yield at which the inequality is met
exactly. [[adr-033-fee-yield-measurement-route|ADR-033]]'s driver computed it at ≈ 7.38 bps/day for the soak notional. It is never shown, and its cost terms
are placeholders.

**Those placeholders disagree with the research by more than an order of magnitude.** `projected_lvr_quote` uses
F-001's `(σ²·3600/8)·C` with a constant concentration `C = 1.8`, which at σ = 1.4e-4/s is **3.81 bps/day** regardless
of range width. For a concentrated position of log-width `w` the LVR rate is `σ²/(2w)` for small `w` (§3.1); for the
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] σ window (`w ≈ 0.081`, ±4%) that is **≈ 105 bps/day**, an implied `C ≈ 50`. The simulator's exact per-bin
accounting on the archive puts narrow σ windows at **≈ 300–350 bps/day hedged break-even**
(`CL_POLICY_REPORT_2026-09-28.md` §B), and names hedge re-balancing cost — a term the live payload does not carry at
all — as the largest single cost for narrow windows. The live gate therefore understates the cost of the range it
would actually deploy.

The request asks for a real-time hurdle engine, a pre-trade gate against projected pool fee yield, and a regime
adjustment. Three standing rules constrain how:

1. **`ev_policy.md` §6:** no second EV rule for the same capital movement; the hurdle multiplier is owned by
   `strategy.config.ts`. A separate "edge ≥ 0 and edge/hurdle ≥ 1.25×" gate would be a second rule.
2. **[[adr-033-fee-yield-measurement-route|ADR-033]] and [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]'s amendment:** fee yield is ratified only by direct accrual on a live position (capital gate
   unapproved), and Orca's whole-pool statistics are display-only — "not an input to planning, EV, or research". The
   trading venue is Meteora DLMM; Orca is monitored, not traded ([[adr-001-deprecate-legacy-onnx-vpin-and-phantom-deps|ADR-001]], [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]).
3. **Regime vocabulary:** `NEGATIVE_GEX` means total net Dollar GEX < 0 (`gexEngine.ts`), not "spot below ZGL"; the
   FSM already exits on `NEGATIVE_GEX` and on a hard ZGL cross (`macroStateMachine.ts`).

## 2. Decision

1. **The hurdle rate is defined as a restatement of the ratified gate, not a new gate.** Two quantities are computed:
   - **`hurdle_gate_bps_day`** — the fee yield on capital at which ev_policy §4 is met *exactly*, from the same EV
     payload the gate uses. By construction `projected fee ≥ hurdle_gate ⇔ gate_pass`, and a test pins that
     equivalence. This is what the gate does today, in the research's units.
   - **`hurdle_model_bps_day`** — the §3 cost model: width- and shape-dependent LVR, hedge re-balancing drag, funding,
     and fixed costs amortized over an expected lifespan, with the regime adjustment. **Display and research only**
     until §5's validation and a ratifying ADR replace the placeholder estimators with it.
2. **No minimum-edge multiplier as a separate rule.** `edge = projected − hurdle` and `edge / hurdle` are **displayed**.
   A required margin, if wanted, is a change to the §4 constant through `strategy.config.ts` and an ADR — one rule,
   one place. `Minimum_Edge_Multiplier = 1.25` from the request is recorded as a candidate for that change, not
   adopted.
3. **Projected fee inputs are labelled by source, and only the ratified one feeds the gate.**
   - *Gate:* `projected_dynamic_fees` as today (`PLACEHOLDER_FEE_YIELD_PER_HORIZON`, 10 bps/day, UNRATIFIED) until
     [[adr-033-fee-yield-measurement-route|ADR-033]]'s route ratifies a value.
   - *Display only:* a **position-yield estimate derived from Orca's measured whole-pool fees and depth** (§3.6),
     labelled "Orca pool, derived — not the trading venue, not [[adr-033-fee-yield-measurement-route|ADR-033]]". This is display, which [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]'s amendment
     permits; it never reaches `computeEvDecision`.
4. **The regime adjustment acts on σ, not on LVR alone.** `σ_eff = m_regime · σ`, with `m_regime` measured, per
   regime, as realized σ in that regime ÷ unconditional σ (archive spot series joined to TICKET T regime records).
   Because LVR and hedge drag scale with σ² and lifespan with 1/σ², one multiplier moves all three consistently.
   Regimes use the repository's labels (`NEGATIVE_GEX`, `ZERO_GAMMA_PROXIMITY`, `POSITIVE_GEX`) plus the signed
   spot-vs-ZGL distance; `m_regime = 1` (no effect) and UNRATIFIED until measured.
5. **Location.** A pure `src/decision/ev/hurdleRate.ts` (the EV domain owns the costs); the monitor displays its output
   (`monitor.md` §4) and a CLI prints one line per evaluation (§4.3). No execution, FSM or signer import.

## 3. Mathematical specification

Notation: capital `V` (quote), pool price `p` (quote per base, ev_policy §5a), per-second σ (the same σ the EV gate
uses), `σ_d = σ·√86 400`. A candidate range is `[p·e^{u_lo}, p·e^{u_hi}]` in log-price `u = ln(P/p)`, width
`w = u_hi − u_lo`. Its **value density** `ρ(u)` (per unit log-price, `∫ρ du = 1`) comes from the shape: Spot → uniform
`1/w`; Curve and BidAsk → the Meteora SDK weights (`src/backtest/research/dlmmPosition.ts` `shapeWeights`, reused, not
restated). All rates are **bps of V per day**.

### 3.1 Expected LVR

For a position whose value density at the current price is `V·ρ(0)`, the instantaneous LVR rate is
`½·σ²·p·|dx/du| = ½·σ²·V·ρ(0)`. Hence

```text
LVR_bps_day = 1e4 · ½ · σ_eff_d² · ρ̄
```

where `ρ̄` is the density price is expected to see over the lifespan. **v1 uses `ρ̄ = ρ(0)`** (centre density): exact at
entry; an upper bound for Curve and Spot, a lower bound for BidAsk. Checks: Spot of small width gives `σ²/(2w)`; a
full-range position gives `σ²/8` (with `ρ = 1/4` in the full-range limit). The regime multiplier enters through
`σ_eff`.

### 3.2 Expected hedge re-balancing drag

The short hedge tracks base inventory `X`, re-hedging when drift exceeds the band `ε` (hedge_engine.md, 0.0625 SOL),
checked every `Δt` seconds. Inventory moves with price at `|dX/du| = V·ρ(0)/p`, so its standard deviation per day is
`s = V·ρ(0)·σ_eff_d / p` (base units), and per check interval `s_Δ = s·√(Δt / 86 400)`.

- A continuously watched band is crossed about `s²/ε²` times a day with trades of `≈ ε`: turnover `≈ s²/ε`.
- A band checked every `Δt` cannot trade more than once per check; when `s_Δ ≫ ε` every check trades
  `E|ΔX| = s_Δ·√(2/π)`, so turnover `≈ (86 400/Δt)·s_Δ·√(2/π) = s² / (s_Δ·√(π/2))`.

One expression covers both regimes:

```text
turnover_base_per_day ≈ s² / max(ε, s_Δ·√(π/2))
HedgeTaker_bps_day     = 1e4 · τ_taker · p · turnover_base_per_day / V
```

**The continuous form alone is wrong here, by about 7×.** On today's σ window at 50 SOL, `s ≈ 25 SOL/day` and
`s_Δ ≈ 0.48 SOL` per 30 s — already far above `ε`. So every check trades, and the check cadence, not the band, sets the
turnover: ≈ 1 100 SOL/day, ≈ 110 bps/day. The simulator's hedged runs on the archive put it at ≈ 150. The continuous
`s²/ε` would give ≈ 1 000 bps/day. **Drag grows with capital `V`** through `s`, because the band is fixed in SOL.
`τ_taker` is the taker fee fraction (5 bps placeholder, UNRATIFIED), and `Δt` the hedge check interval.

No live hedge has ever run, so there are **no hedge_engine logs** to parameterize from (§6). The turnover model is
validated against the research simulator's discrete hedge instead (§5).

### 3.3 Funding

```text
Funding_bps_day = 1e4 · f_8h · 3 · (h·p / V)
```

`h` = hedged base quantity (≈ the position's base inventory), valued at the pool price exactly as ev_policy §5b values
it; `f_8h` the Binance funding rate per 8 h, signed (a negative rate is income). An unknown rate takes ev_policy §5b's
refusing sentinel.

### 3.4 Fixed costs amortized over the expected lifespan

```text
Fixed_bps_day = 1e4 · (rent_sunk + tx_fees + s_swap · N_swap) / (V · T_life_days)
```

- `rent_sunk` — ev_policy §3a / [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]], with its UNRATIFIED amortization (`deployRentAmortizationDeployments`).
- `tx_fees` — deploy and withdraw transactions for the planned chunks ([[adr-039-deploy-reserve-is-derived-from-the-plan|ADR-039]] breakdown).
- `s_swap · N_swap` — re-ratio slippage (10 bps placeholder) on the swapped notional at open and close.
- **Lifespan** from the exit rule, for driftless log-price starting at `u = 0` in `(u_lo, u_hi)`:
  `E[τ_exit] = (−u_lo · u_hi) / σ_eff²` (in seconds; `= (w/2)²/σ²` when centred). Then
  `T_life = min(H_recentre, E[τ_exit] + N_out)` for a policy "close after `N_out` out of range" and/or "re-centre every
  `H_recentre`". **The live bot has no out-of-range exit today** (its exits are ZGL cross, `NEGATIVE_GEX` and the EV
  gate), so for the live gate `T_life` is the EV horizon (24 h) until an exit policy is ratified; the research
  policies' rules are available for display.

### 3.5 Totals, edge

```text
hurdle_model_bps_day = LVR + HedgeTaker + Funding + Fixed
hurdle_gate_bps_day  = 1e4 · ( projected_lvr_quote + binance_funding_drag + deploy_rent_sunk
                               + 1.5 · (swap_slippage + gas_fees) ) / (V · horizon_days)          (exact inversion of §4)
edge_bps_day = projected_fee_bps_day − hurdle_bps_day          edge_ratio = edge / hurdle
```

`hurdle_gate` uses the payload's own terms and so agrees with `gate_pass` exactly; `hurdle_model` shows what the terms
would be under this model. The gap between the two is the size of the placeholders' error, which is the point of
showing both.

### 3.6 Display-only position-yield estimate from Orca ([[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]] amendment)

A position earns in proportion to its share of liquidity at the traded price. With Orca's measured whole-pool fees
`F` (quote/day) and pool value depth `D` at price (quote per unit log-price, = 100 × the monitor's "depth per 1%"):

```text
position_fee_bps_day ≈ 1e4 · F · ρ(0) / (D + V · ρ(0))
```

— the marginal yield, diluted by the position's own liquidity. It assumes volume at the current price is
representative of the day and ignores bins crossed within a tick; it is **Orca's** pool, not the trading venue's, and
it is never an EV input. It is shown because it is the only *measured* fee figure the system has.

## 4. Interfaces

### 4.1 TypeScript (the repository's language; the request's Python signature is not used)

```ts
export type Shape = 'spot' | 'curve' | 'bidask';
export type RegimeLabel = 'POSITIVE_GEX' | 'ZERO_GAMMA_PROXIMITY' | 'NEGATIVE_GEX' | 'DEGRADED';

export interface HurdleParams {
  readonly capitalQuote: number;               // V
  readonly lowerLog: number;                   // u_lo < 0
  readonly upperLog: number;                   // u_hi > 0
  readonly shape: Shape;
  readonly hedgeBandBase: number;              // ε, SOL
  readonly hedgeCheckIntervalSeconds: number;  // Δt — caps turnover when per-check moves exceed ε (§3.2)
  readonly takerFeeFraction: number;           // τ_taker (UNRATIFIED 0.0005)
  readonly swapSlippageFraction: number;       // s_swap (UNRATIFIED 0.001)
  readonly exitPolicy: { readonly outOfRangeSeconds: number | null; readonly recentreSeconds: number | null };
  readonly regimeSigmaMultiplier: Readonly<Record<RegimeLabel, number>>;   // m_regime (UNRATIFIED, all 1)
}

export interface MarketState {
  readonly poolPriceQuotePerBase: number;      // ev_policy §5a
  readonly sigmaPerSecond: number;             // the EV gate's σ; units in the name
  readonly regimeLabel: RegimeLabel;
  readonly spotToZglSignedPct: number | null;  // negative when spot is below ZGL
  readonly fundingRatePer8h: number | null;    // null → §5b sentinel
  readonly rentSunkQuote: number;              // ev_policy §3a
  readonly txFeesQuote: number;
}

export interface HurdleBreakdown {
  readonly lvrBpsDay: number;
  readonly hedgeTakerBpsDay: number;
  readonly fundingBpsDay: number;
  readonly fixedBpsDay: number;
  readonly lifespanDays: number;
  readonly sigmaEffPerSecond: number;
  readonly hurdleModelBpsDay: number;
  readonly status: 'MODEL_UNRATIFIED';        // travels with the number
}

export function computeHurdleRate(params: HurdleParams, market: MarketState): HurdleBreakdown;

/** The gate's own hurdle, inverted from an EvDecision payload. Agrees with `gate_pass` by construction. */
export function hurdleFromEvDecision(decision: EvDecision, capitalQuote: number, horizonDays: number): number;

export interface DeploymentGateView {
  readonly projectedFeeBpsDay: number;         // the gate's input
  readonly projectedFeeSource: 'PLACEHOLDER' | 'RATIFIED_ADR033';
  readonly hurdleGateBpsDay: number;
  readonly hurdleModelBpsDay: number;
  readonly edgeGateBpsDay: number;             // projected − hurdleGate
  readonly edgeRatio: number | null;           // displayed, not gated
  readonly gatePass: boolean;                  // === EvDecision.gate_pass, never recomputed differently
  readonly orcaDerivedFeeBpsDay: number | null;// §3.6, display only
}

/** Assembles the view. Its `gatePass` is the EV gate's own verdict; it adds no condition. */
export function evaluateDeploymentGate(candidate: HurdleParams, pool: MarketState, ev: EvDecision): DeploymentGateView;
```

### 4.2 Units and failure

Everything in bps of `V` per day. Non-finite or non-positive `V`, `w ≤ 0`, `σ ≤ 0` or a missing pool price →
`null` breakdown with a reason code, never a zero cost. An unknown funding rate follows ev_policy §5b (refuse).

### 4.3 Monitor and CLI line

```text
[Proj fee 10.00 bps/d (PLACEHOLDER) | Hurdle(gate) 7.38 | Hurdle(model) 289 UNRATIFIED | Edge(gate) +2.62 (ratio 0.36) | Gate PASS]
  model: LVR 105.0 · hedge 109.2 · funding 1.5 · fixed 72.9 · life 0.96 d · σ_eff 1.40e-4/s (m=1.00 POSITIVE_GEX)
  Orca-derived position yield 62.4 bps/d — Orca pool, not the trading venue, not ADR-033
```

Illustrative figures, all real inputs as of 2026-09-28, with a placeholder σ:

- the [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] σ window (Spot density, `w ≈ 0.081`) at 50 SOL, hedge checked every 30 s, funding 1 bp per 8 h;
- 0.3 SOL of rent and 10 bps re-ratio slippage on half the capital at open and at close;
- Orca's measured $76k/day of fees at $1.51M depth per 1%.

The gate verdict printed is the EV gate's own; the model hurdle is printed beside it, never in place of it. In this
example the gate passes at 7.38 bps/day while the modelled cost of the same range is ≈ 289. Even the one measured fee
figure, 62 bps/day on Orca, does not cover the modelled cost. That is exactly the discrepancy this ADR exists to show.

## 5. Validation before the model may replace the placeholders

`hurdle_model` becomes eligible to replace `placeholderProjectedLvrQuote` (and to add a hedge-drag term to the EV
payload) only when a later ADR ratifies it on this evidence:

1. **Against the research simulator** on the archive ([[adr-043-research-simulator-reads-archive-offline|ADR-043]]): for the σ-window policies, the model's LVR and hedge
   terms agree with the simulator's exact LVR-eq and hedge costs within a stated tolerance, per UTC day and [[adr-033-fee-yield-measurement-route|ADR-033]]
   sub-window.
2. **Regime multipliers measured**, with sample counts, from ≥ 21 days of archive + TICKET T records.
3. `ev_policy.md` amended (§3's canonical payload gains the hedge-drag field; §4 unchanged or changed by the same ADR).

## 6. Departures from the request (need the dispatcher's acceptance)

1. **No second gate.** The request's "reject if edge ≤ 0 or edge/hurdle < 1.25" is displayed, not enforced; the gate
   remains ev_policy §4. Reason: §6's single-rule prohibition. A margin belongs in the §4 constant.
2. **Venue-API fee yield does not feed the gate.** The gate keeps its projected-fee input until [[adr-033-fee-yield-measurement-route|ADR-033]] ratifies one;
   the Orca-derived estimate is display-only. Reasons: [[adr-033-fee-yield-measurement-route|ADR-033]], [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]]'s amendment, and Orca is not the trading venue.
3. **Regime definition and form.** "Spot < ZGL = negative dealer gamma" is replaced by the repository's labels plus the
   signed ZGL distance, and the adverse-selection adjustment is a measured σ multiplier (default 1) rather than an LVR
   multiplier with an assumed value.
4. **No hedge_engine logs exist**, so hedge churn is modelled (§3.2) with the ratified band and placeholder taker fee,
   and validated against the simulator, rather than parameterized from logs. TypeScript, not Python.

## 7. Consequences

- The live gate's implicit hurdle becomes visible in the research's units, beside a model that says how far its
  placeholders are from the costs of the range actually planned — **≈ 3.8 vs ≈ 105 bps/day of LVR** for today's σ
  window. That gap is itself the most useful output until ratification.
- No change to `gate_pass` for any input while this ADR is in force: the gate's verdict and the displayed gate hurdle
  agree by construction, and the model hurdle is not an input to anything.
- **UNRATIFIED:** the model as a whole; `ρ̄ = ρ(0)`; τ_taker 5 bps; s_swap 10 bps; `m_regime`; `T_life` for the live
  bot (= 24 h horizon). Each is labelled wherever it is shown.
- **Recorded cost:** two hurdle figures on one screen invite reading the model one as the gate. The display labels
  them `(gate)` and `(model) UNRATIFIED`, and only the gate's verdict is printed as PASS/FAIL.

## 8. Reversed by

A ratifying ADR under §5 that replaces the estimators (this ADR then becomes its history); a ratified [[adr-033-fee-yield-measurement-route|ADR-033]] fee value
(which replaces the placeholder fee input but not this structure); or a decision to add a separate pre-trade gate,
which must first amend ev_policy §6.

## Implementation note — 2026-09-29 (TICKET W)

- **Where it landed.**
  - The equations are in `src/intelligence/range/hurdleMath.ts`, one copy that both the EV engine
    (`src/decision/ev/hurdleRate.ts`) and the research report call.
  - The shape weights moved to `src/intelligence/range/liquidityShape.ts`; the research report's sections A–E are
    byte-identical after the move.
  - The CLI is `src/decision/ev/hurdleMain.ts` (`npm run hurdle`). It reads the newest TICKET T decision record, not
    the archive, and builds EV inputs for a flat wallet of `--capital` SOL.
- **Refinements to the text above, none changing a decision.**
  1. **Hedge scaling.** With the band checked every 30 s at today's size, every check trades. Hedge drag therefore
     scales **linearly** with σ, not as σ²; it is σ² only for a watched band. The regime multiplier's effect on hedge
     drag follows that, and test H04 pins both regimes.
  2. **Ranges in bins.** Ranges are passed as bins either side of the active bin plus the lattice step, as the planner
     expresses them, rather than as `lowerLog`/`upperLog`; the edges sit half a step outside the outer bins.
  3. **Unknown funding.** Where funding is not read (the monitor), the model marks it unknown and excludes it from its
     total, with that stated, instead of taking §5b's sentinel. The gate's refusal is unchanged, and the CLI prints it.
  4. **Recorded Orca frames.** Frames carry the hurdle from schema 7. Earlier recorded Orca frames (schema 6) replay
     with `hurdle: null`, and `RECORD_SCHEMA` is unchanged.
- **Evidence at adoption** (report `CL_POLICY_REPORT_2026-09-29.md`, archive to 2026-09-28 16:27Z):
  - **§F:** model LVR is 1.05–3.0× the simulator's LVR-equivalent across the σ-window policies, and model hedge
    0.86–3.3× the simulator's taker cost. The model is closest for σ×2 windows (LVR 1.05–1.09×) and furthest for
    narrow windows held out of range. The per-day ratio holds its direction on both days (1.2–2.4×). The model is
    conservative, not yet calibrated.
  - **§G:** σ below the ZGL is 1.33× the all-regime σ (37 returns, wide interval); above it, 0.94× (254 returns). The
    direction the request assumed; not enough data to ratify.
  - **CLI on live state, 50 SOL:**
    - the ratified gate's own hurdle is 62.5 bps/day against its 10 bps/day placeholder fee: **FAIL**, mainly from
      203 bins of sunk rent charged over one day;
    - the model puts the full cost at ≈ 443 bps/day.

## History note — 2026-10-01 ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]], TICKET 028)

[[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] is the ratifying ADR §5 and §8 anticipated, for the LVR and hedge-drag terms only.
- **What it changed:** the model's ρ(0) became ρ̄, its σ is scaled to the pool (`poolSpotSigmaRatio`), and its hedge
  turnover takes the pool's burst factor.
- **Where those terms now live:** `hurdleMath.rangeCostRates`, which the EV gate also prices with.
- **What remains this ADR's UNRATIFIED model, display and research only:**
  - the model hurdle as a total (lifespan-amortized fixed costs);
  - the regime multipliers (all 1);
  - the derived Orca fee estimate.
