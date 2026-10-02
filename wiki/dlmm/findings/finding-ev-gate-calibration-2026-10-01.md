---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/EV_GATE_CALIBRATION_2026-10-01.md
bot_commit: afc819c
source_sha256: b1dd7a639d3ddbac44664dfee37dfbe6d94b37c0a31a898f4e997845a971f3e9
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/EV_GATE_CALIBRATION_2026-10-01.md` at commit `afc819c`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# EV gate calibration — TICKET 028 Part 0 — 2026-10-01

**Verdict: FAIL against [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D2 as drafted. Per the ticket, Parts 1–5 stop and [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D1/D2 are revisited.**

The ρ(0) hypothesis is **confirmed**: ρ̄ removes the shape dependence. Three things remain:
- a shape-independent residual of about 1.1–1.3× on LVR;
- about 1.5× on hedge drag;
- a per-day spread that is mostly σ forecast error, not model error.

## Method

- **Simulator:** `dist-research/`'s real one (report §F's accounting), over the full archive span: 2026-09-26 11:16Z →
  2026-10-01 ~14:00Z, 6 UTC days, [[adr-033-fee-yield-measurement-route|ADR-033]] sub-windows sw1 (complete) and sw2 (23 h).
- **Policies:** 96 σ-window policies with out-of-range, re-centre or hold closes (§F's set), at 50 SOL.
- **Only the model's inputs were swapped:**
  - **ρ(0)** — today's model: the active-bin weight ÷ the log step;
  - **ρ̄** — the life-averaged density, the shape's weights averaged over the occupation density of driftless Brownian
    motion started at the open and killed at the range edges. That density is a tent (Green's function),
    `g(u) = (u−a)·b` for u ≤ 0 and `(−a)·(b−u)` for u ≥ 0;
  - **oracle σ** — the σ realized over the next 24 h, in place of the trailing 24 h σ at the open. This is a form test
    only, run on the 72 policies whose placement does not itself use the 24 h σ.
- **Ratio:** model ÷ simulator, for LVR (vs hedged loss) and for hedge drag (vs taker cost).
- **Scripts:** `docs/operations/ev_gate_calibration/` (read-only).

**ρ̄/ρ(0) for the live 202-bin window:** Spot 1.00, Curve **0.71**, BidAsk **3.88**.

## Results

### 1. Shape — the ρ(0) hypothesis (whole span, median over policies, [min–max])

| shape | ρ(0) LVR | ρ(0) hedge | ρ̄ LVR | ρ̄ hedge |
|---|---|---|---|---|
| Spot | 1.27 [1.06–1.88] | 1.55 [0.71–2.39] | 1.27 (identical: ρ̄ = ρ(0)) | 1.55 |
| **Curve** (live) | **1.58** [1.25–3.17] | **2.07** [1.01–4.06] | **1.12** [0.88–2.20] | **1.46** [0.71–2.82] |
| BidAsk | 0.36 [0.27–0.70] | 0.43 [0.13–0.52] | 1.45 [1.07–2.78] | 1.72 [0.75–2.46] |

- **Confirmed:** ρ(0) overstates Curve and understates BidAsk (below 1), exactly as [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §3.1's bounds say.
- **With ρ̄, the three shapes converge** to a common 1.1–1.5× on LVR and 1.5–1.7× on hedge.

### 2. Out-of-range accrual — negligible

The model accrues over every deployed second, including out-of-range time. The median in-range share of deployed ticks
is 1.00 (range 0.73–1.00), and scaling the model by it moves the medians by ≤ 0.07.

### 3. Per-day spread — mostly σ forecast error

Curve, ρ̄, median over policies:

| UTC day | hours | trailing σ: LVR / hedge | oracle σ: LVR / hedge |
|---|---:|---|---|
| 2026-09-26 | 12.7 | 1.28 / 1.71 | 1.36 / 1.73 |
| 2026-09-27 | 23.1 | 1.08 / 1.30 | 1.81 / 1.68 |
| 2026-09-28 | 22.2 | 0.73 / 0.99 | 1.12 / 1.20 |
| 2026-09-29 | 24.0 | 1.90 / 1.72 | 1.10 / 1.29 |
| 2026-09-30 | 24.0 | 0.88 / 1.23 | 0.93 / 1.24 |
| 2026-10-01 | 14.0 | 1.88 / 1.73 | 1.12 / 1.38 |

(The oracle columns use the 72-policy set, so they differ slightly from §1.)

- **With the trailing σ, the ratio tracks the day's volatility inversely.** It is low on the volatile 09-28 (realized
  σ 1.17e-4) and high on the calm 09-29 and 10-01 (10-01's σ was 0.76e-4), because the trailing 24 h σ carries
  yesterday's level into today.
- **With the realized σ, 5 of 6 days fall in 0.93–1.36 on LVR.** 09-27 rises to 1.81, partly because the soak and the
  archive runs change over that day.
- **What this means for D2:** that error belongs to [[adr-047-provisional-sigma-estimator|ADR-047]]'s σ estimator, which TICKET Z measures, not to the cost
  model's form. A per-day D2 test that uses the forecast σ judges both at once.

### 4. Residual form bias (ρ̄, oracle σ, whole span)

| shape | LVR | hedge |
|---|---|---|
| Spot | 1.41 | 1.64 |
| Curve | 1.28 | 1.51 |
| BidAsk | 1.69 | 1.85 |

- With the right density and the right σ, the model still overstates: LVR by about 1.3–1.7×, hedge by about 1.5–1.85×.
- It is roughly shape-independent, so it is not a density problem.
- **Not yet explained. Candidates:**
  - **The hedge band.** The model's per-check turnover `s_Δ·√(2/π)` ignores the 0.0625 SOL band. Below it nothing
    trades, and at ρ̄ the band is about 20–25% of `s_Δ`, which would account for a large share of the hedge residual.
  - **DLMM's constant-sum bins.** Within a bin no inventory converts, so LVR accrues only at bin crossings.
  - **The σ horizon.** The σ estimator uses 5 s returns while the simulator marks every 30 s. That should push the other
    way (variance ratio 1.15–1.20), so it does not explain an overstatement.

## Against [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D2 (as drafted: ±25% median, no day outside ±50%)

| test (Curve, ρ̄) | result | pass? |
|---|---|---|
| LVR, whole-span median | 1.12 | **pass** |
| hedge, whole-span median | 1.46 | fail |
| LVR, sub-window medians (sw1, sw2) | 1.49 overall [0.74–2.40] | fail |
| per day within ±50% (trailing σ) | 09-29 1.90, 10-01 1.88 on LVR | fail |

## Recommendation (for revisiting [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]])

1. **D1: adopt ρ̄.** It is confirmed, closed-form and derived, not fitted. It is necessary but not sufficient.
2. **Fix the hedge-turnover form before fitting anything.** Make the turnover band-aware (expected trade per check
   given the band) and re-score. If the hedge residual closes, only the LVR residual (about 1.1–1.3×) remains.
3. **Split D2 into two tests:**
   - **form:** model ÷ simulator with the realized σ, per day and per sub-window, within ±25%;
   - **σ forecast:** [[adr-047-provisional-sigma-estimator|ADR-047]]'s own evidence (report §H).

   As drafted, D2 fails the model for the estimator's errors.
4. **Decide what to do about the residual.** Either fit one shape-independent factor per term ([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]] D1's
   alternative), or ship ρ̄ without it.
   - **The case for shipping without it:** the residual overstates costs, so the gate errs towards refusing. On the
     live state that is about a 1.1–1.5× too-high hurdle, against today's 4–5× too-low one (62.5 bps/day against a simulated break-even of about 270–330).
5. **Re-run the scripts at sw2's close (2026-10-03 14:30Z) and again at 21 days.** Today's data is 4 full days and one
   complete sub-window, so every number here is provisional.

Read-only. No code in `src/`, no constant and no process changed.

---

## Step 2 — the residual explained (2026-10-01 14:22Z)

**Verdict: the residual is explained, and the fix is not the hedge band.** It comes from two measured properties of the
pool's own price, which the model reads from Deribit spot instead:

1. the pool's σ is lower than spot's;
2. the pool's price moves in bursts.

With ρ̄ and both pool properties, Curve agrees with the simulator to within 2–3% on both terms. The scripts are
`calib028_band.js` and `calib028_burst.js`, read-only.

### Band-aware hedge turnover: rejected as the cause

- **The formula:** turnover per check is `s_Δ·φ(ε/s_Δ)`, with φ tabulated by a seeded Monte Carlo of the simulator's
  rule (trade the whole drift once it exceeds ε). φ(0) = √(2/π) = 0.798, and φ → 1/k for a wide band.
- **Why it doesn't matter here:** at ρ̄ the band is k ≈ 0.13 of the per-check move, where φ = 0.79. Hedge ratios moved
  by only 0.01–0.04 (Curve went from 1.46 to 1.45).
- **Correction:** the shared write-up called the band the likeliest cause. It isn't.

### Cause 1 — the pool's σ is lower than Deribit spot's

- **At the simulator's 30 s cadence:** pool active-price σ is 9.37e-5/s, against Deribit spot's 1.06e-4/s. The ratio
  is **0.882** (variance 0.778).
- **Per day:** 0.82–0.91.
- **Why it matters:** the simulator's position moves with the pool, while the model's σ is Deribit's.
- **The test:** feeding the model the pool's realized σ over the next 24 h.

| shape (ρ̄) | LVR, trailing spot σ | LVR, realized spot σ | **LVR, realized pool σ** |
|---|---:|---:|---:|
| Spot | 1.31 | 1.42 | **1.06** |
| Curve | 1.16 | 1.28 | **0.98** |
| BidAsk | 1.47 | 1.68 | 1.29 |

### Cause 2 — the pool's price moves in bursts

The hedge model assumes each check's inventory move is Gaussian, with E|ΔX| = sd·√(2/π). The pool does not behave
that way:

| 30 s series | unchanged | E\|r\| ÷ (sd·√(2/π)) | kurtosis |
|---|---:|---:|---:|
| pool active bin | **50.6%** | **0.739** | 12.3 |
| Deribit spot | 0.1% | 0.878 | 10.9 |

- **The effect:** at the same variance, the pool trades 1/0.739 = **1.35×** less than the model assumes. That matches
  the hedge residual of 1.31 under the pool σ.
- **Per day:** the burst factor is 0.60–0.81. It is 0.76–0.81 since 09-28; the two lower days are the soak run, when
  the pool was unchanged in 62–70% of checks.

### Curve with ρ̄, the realized pool σ and the burst factor (0.739 overall)

The hedge model is linear in this factor, so the hedge column scales exactly.

| | whole span | per UTC day (09-26 … 10-01) |
|---|---:|---|
| LVR | **0.98** | 0.93, 1.36, 0.79, 1.00, 0.85, 0.88 |
| hedge | **0.97** (1.31 × 0.739) | 1.03, 1.06, 0.75, 0.90, 0.87, 0.90 |

Every day is within ±50%. Within ±25%, only 09-27's LVR (1.36) falls outside; that was the day the soak run handed
over to the archive run. The sub-windows were not re-run for this variant.

### What this changes for [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]]

- **D1 is now three measured inputs, none fitted to the simulator:**
  - ρ̄ from the planned range;
  - the **pool's** σ, either estimated from the pool price or as Deribit σ × the measured pool/spot ratio (≈ 0.88);
  - the pool's **burst factor** on hedge turnover (≈ 0.74 overall, 0.76–0.81 recently).

  Because each is measured independently of the simulator, the agreement above is a prediction, not a fit.
- **D2 should be split as recommended.** The form test now passes. What remains is the σ forecast: the gate must
  forecast the **pool's** σ, which [[adr-047-provisional-sigma-estimator|ADR-047]]'s spot-based estimator overstates by about 1/0.88.
- **Re-run at sw2's close (2026-10-03 14:30Z)** to check that both pool factors hold.

---

## Part 0b — provisional check, 2026-10-02T11:36Z (final run scheduled for 2026-10-03 14:35Z)

**Provisional: both pool factors are in range in both [[adr-033-fee-yield-measurement-route|ADR-033]] sub-windows.** `calib028_burst.js` now reports per
sub-window, which is what [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]]'s "Reversed by" judges.

| sub-window | hours | pool/spot σ (0.82–0.91) | burst factor (0.60–0.81) |
|---|---:|---:|---:|
| sw1 (complete) | 72.0 | 0.891 | 0.781 |
| sw2 (in progress) | 45.0 | 0.858 | 0.762 |

- **The whole span** (2026-09-26 → 2026-10-02 11:33Z): burst factor 0.742, against 0.739 at calibration. The pool's
  active bin is unchanged in 50.5% of 30 s checks.
- **Per day:** 2026-10-02 (11.5 h so far) reads 0.818 on the pool/spot σ ratio, just under 0.82. That is a single
  partial day inside a sub-window at 0.858, so it does not trigger the reversal rule.
- **The final run:** the one-shot scheduled task `dlmm-part0b` runs `docs/operations/ev_gate_calibration/run_part0b.ps1`
  at 2026-10-03 14:35Z. It runs the window check, `sigma_surface.js`, the pool factors, `calib028.js`,
  `calib028_oracle.js`, `pool_sigma_forecast.js` and the research report, and writes them to
  `todo/findings/PART0B_2026-10-03/` and `todo/research/CL_POLICY_REPORT_2026-10-03.md`.
- **The verdict** is written into this finding once those outputs are read.
