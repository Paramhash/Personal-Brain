---
domain: cl-market-making
tags: [curriculum, lvr, impermanent-loss]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 4
status: not-started
prerequisites: [m02-concentrated-liquidity-math]
bot_links: [adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost, finding-ev-gate-calibration-2026-10-01, finding-ev-gate-vs-simulator-2026-10-01, blueprint-ev-policy, cl-policy-report-2026-10-01]
---

# M4 — Loss-versus-rebalancing and impermanent loss

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m02-concentrated-liquidity-math|M2]].

## Learning objectives
- State LVR (Milionis et al.): the LP's loss against a portfolio that rebalances to the same holdings at market prices.
- Derive the LVR rate $\tfrac12\sigma^2 \rho V$ from the position's value density $\rho$, and its full-range case $\sigma^2/8$.
- Explain why LVR, not impermanent loss, is the right cost for a forward-looking decision.
- Explain how fees, arbitrage and block time interact (arbitrage only trades when the price gap exceeds the fee).

## Concepts to cover
`loss-versus-rebalancing`, `impermanent-loss`, `value-density-rho`, `life-averaged-density`, `arbitrage-profits-with-fees`.

## Existing vault notes to connect
[[realized-volatility]], [[option-greeks]] (gamma), [[delta_hedging]].

## Where it shows up in the bot
- The EV gate's LVR term, $\tfrac12\sigma_{pool}^2\bar\rho$:
  [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]], [[blueprint-ev-policy|EV policy]] §3b.
- Model vs exact accounting: [[finding-ev-gate-vs-simulator-2026-10-01|EV gate vs simulator]],
  [[finding-ev-gate-calibration-2026-10-01|calibration]] (Curve model ÷ simulator 0.98).
- Simulated hedged losses per policy: [[cl-policy-report-2026-10-01|CL policy report]] §A and §F.

## Self-test
> [!question]- What is LVR for a full-range constant-product pool, and roughly how large per day at a daily σ of 3%?
> $\sigma^2/8$ of position value per unit time. At $\sigma_d = 0.03$: $0.0009/8 \approx 1.1$ bps per day.

> [!question]- Why can impermanent loss be zero while LVR is large?
> IL compares end values only: after a round trip back to the start price it is zero. LVR accumulates along the path: every move that arbitrageurs trade against costs the LP relative to rebalancing at market prices, and that does not reverse.

> [!question]- The bot's old gate used $\sigma^2/8 \times 1.8$ for any range. Why was that about 48× too low for its live window?
> It treats the position as nearly full-range (effective density 0.45). The live 202-bin window concentrates value, with a density of about 22. LVR scales with density, so a range-blind formula understates the cost of a narrow range.

## Open questions
- (Add questions here after a quiz.)
