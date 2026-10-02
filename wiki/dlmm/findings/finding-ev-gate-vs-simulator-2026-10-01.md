---
domain: cl-market-making
tags:
- dlmm-hedge-bot
- finding
aliases: []
created: '2026-10-02'
reviewed: true
bridge_managed: true
source_path: dlmm-hedge-bot/development/todo/findings/EV_GATE_VS_SIMULATOR_2026-10-01.md
bot_commit: e7421f6
source_sha256: 76061c550dd846a55b090b2ce96b505156027745c18d134ff13dee9d407595aa
exported_at: '2026-10-02T12:50:29Z'
---
> [!info] Read-only mirror of `dlmm-hedge-bot/development/todo/findings/EV_GATE_VS_SIMULATOR_2026-10-01.md` at commit `e7421f6`. Edit it in the bot repo; this note is overwritten by `bridges/dlmm_bridge.py`.

# EV gate vs simulator: why the gate's cost side is an order of magnitude low — 2026-10-01

**Question.** The 2026-10-01 research report (`todo/research/CL_POLICY_REPORT_2026-10-01.md`) gives a hedged
break-even of about 270–330 bps/day for the top policies. `sigma_surface.js` gives a required fee yield of about
6 bps/day. Which is right, and does it matter before §I's measured fee yield is used?

**Answer.** There are three cost models, and they disagree for two structural reasons:

1. **The gate's LVR ignores the range.**
2. **The gate has no hedge-cost term at all.**

The gate is safe today only because the fee placeholder is low. If Route 4's measured fee yield is ratified into the
gate with the cost side unchanged, the gate would **pass** positions the simulator says lose 150–240 bps/day.

**This is not a new discovery.** [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] (2026-09-29) recorded the LVR gap ("3.81 bps/day at any width, against
≈105"). It kept the gate unchanged by design, and its §5 set the evidence a later ADR needs before the model may
replace the gate's estimators. Its §3.1 already calls ρ(0) an upper bound for Curve, which is the residual below. What
is new is §I: a measured fee yield large enough to make the gap dangerous.

## The three numbers

The live state was taken from TICKET T record 2026-10-01T13:50:27Z:
- window -5450..-5248 (202 bins, about ±4%);
- 50 SOL-equivalent, curve shape;
- σ 1.4e-4/s (placeholder);
- funding 1 bps per 8 h (operator-supplied).

The figures are from `npm run hurdle`.

| Source | LVR | Hedge taker | Funding | Fixed (rent, slippage, gas) | Total, bps/day |
|---|---:|---:|---:|---:|---:|
| **EV gate** (`evCalculator.ts`, ratified structure) | 3.8 | — (no term) | 1.5 | ≈57 | **62.5** → FAIL against the 10 bps placeholder |
| **[[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model** (`hurdleMath.ts`, display only) | 183.4 | 190.8 | 1.5 | 67.2 (1 d life) | **442.9** |
| **Simulator** (report §A/§F, σ×0.5 policies, realised σ ≈ 1.1e-4) | ≈100–155 | ≈110–190 | 1 bps/8 h | per open | **≈270–330** break-even |

**The 6 bps/day was not the gate's hurdle.** It is `sigma_surface.js`'s y* = LVR + K with K = 3.57, a figure from
before [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]]. It leaves out `deploy_rent_sunk`, which dominates the gate's fixed term at 50 SOL.

## Cause 1 — the gate's LVR treats the position as nearly full-range

- **The gate:** `((σ_s²·3600/8)·1.8)·24 h` = `σ_d²/8 · 1.8` = `0.225·σ_d²` (`evCalculator.ts:284-297`). That is
  Uniswap v2's full-range LVR (`σ²/8`) times the placeholder `PLACEHOLDER_DLMM_CONCENTRATION_MULTIPLIER = 1.8`.
- **The model:** `½·σ_d²·ρ` (`hurdleMath.ts:33`), where ρ is the position's value density per unit log-price at the
  current price.
- **What that implies:** the gate's effective ρ is 0.45. The live 202-bin curve window has ρ ≈ 21.7 (backed out of
  the model's 183.4 bps/day at σ_d = 0.0412). That is **about 48×** the gate's figure.
- **The code already says so:** the constant's own doc comment says "a constant does not vary with the range the
  planner actually chose, which is the term's whole point", and leaves the fix to ratification.

## Cause 2 — the gate has no hedge cost

- `net_ev = fees − LVR − funding − rent` (`evCalculator.ts:526-561`). The cost of keeping the position delta-neutral
  does not appear.
- **How large it is:** a narrow range has high gamma. Inventory goes from all-SOL to all-USDC across about 8% of
  price, so the hedge trades about (path length ÷ range width) × capital.
- **Why the band doesn't help:** at 30 s checks the path length is about 1.4 per day. The 0.0625 SOL band is far
  below the per-check inventory move at 50 SOL, so the hedge trades on almost every check. That is about 28–35×
  capital a day at 5 bps taker, or about 140 bps/day.
- **Who prices it:** the simulator accounts for this cost exactly, and the model prices it at 190.8 bps/day. The gate
  prices it at zero.

## Residual — the model is about 2× the simulator

- Report §F gives model/sim ratios of 1.4–3.2 (median about 2) for **both** LVR and hedge cost, across every policy.
- **Hypothesis (not tested):** the model evaluates ρ once, at the open, where a curve shape is densest. The simulator
  integrates over the path. As price drifts off-centre inside the range, density falls, and it is zero while the
  position is out of range (in range 83–97% of the time).
- **Why the hypothesis fits:** LVR and hedge turnover are both linear in ρ (turnover ∝ s ∝ ρ when the per-check move
  dominates the band), so one ρ bias would inflate both by the same factor, which is what §F shows.
- **How to test it:** compare spot-shape rows (uniform ρ) against curve rows. The bias should shrink for spot.

## Consequence for §I and [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] D1

- §I measures 80–141 bps/day of fee yield for the top policies.
- [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]] D1 = yes lets Route 4 ratify `PLACEHOLDER_FEE_YIELD_PER_HORIZON`.
- **If Route 4 ratifies into today's gate:** a figure near 100 bps/day clears the gate's 62.5 bps/day hurdle, so the
  gate passes. The simulator's net on the same policies is −150 to −240 bps/day (§I).
- **So:** ratifying the fee side **must not** happen before the gate's cost side prices range-dependent LVR and the
  hedge's taker cost.
- **Timing:** the earliest a ratification could happen is when Route 4's window completes, 2026-10-21 16:48Z. That is
  the deadline for a fix.

## What would close this (for the dispatcher)

1. **Replace the 1.8 constant with ρ from the planned range.** The [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] model already computes this; it needs
   calibrating to the simulator (the ≈2× residual).
2. **Add a hedge-taker term to `net_ev`.** The [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]] §3.2 formula would do, with the same calibration.
3. **Tie ratification to the fix.** Make Route 4 ratification conditional on 1 and 2, for example as an [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]]
   amendment, so the gate cannot pass on measured fees alone.
4. **Possibly revisit the strategy itself.** A σ×1 window roughly halves both costs (§F), and a wider hedge band
   trades less often at the cost of more delta risk. These are strategy decisions, not calibration.

Read-only. No code, constant or process was changed.
