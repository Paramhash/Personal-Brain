---
domain: cl-market-making
tags: [curriculum, hedging]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 8
status: not-started
prerequisites: [m04-lvr-and-impermanent-loss, m09-perpetuals-and-funding]
bot_links: [blueprint-hedge-engine, adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost, adr-051-inventory-objective-benchmark-hedge, finding-ev-gate-calibration-2026-10-01]
---

# M8 — Hedging LP exposure

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m04-lvr-and-impermanent-loss|M4]] and
[[m09-perpetuals-and-funding|M9]].

## Learning objectives
- Delta-hedge an LP position with a perpetual short sized to its base inventory, and explain what remains after
  hedging: the short-gamma cost, LVR.
- Estimate hedge turnover and its taker cost for a band hedge checked at a fixed interval, and show how it grows
  with range narrowness and capital.
- Know the option-based hedges of LP loss (weighted variance swaps, options on the range) and when they make sense.

## Concepts to cover
`delta-hedging-lp`, `hedge-drag`, `band-hedging`, `hedge-turnover`, `variance-swap-hedge-of-impermanent-loss`.

## Existing vault notes to connect
[[delta_hedging]], [[option-greeks]], [[dynamic-greek-limits-scaling]], [[transaction_costs_in_options]].

## Where it shows up in the bot
- The hedge target $q^* = -x_{pos}$ and its 0.0625 SOL band: [[blueprint-hedge-engine|hedge engine]].
- Hedge drag as a gate cost, with the pool's burst factor: [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]].
  Measured ≈ 88 bps/day on the live window at the placeholder σ.
- A hedge to a benchmark inventory instead: [[adr-051-inventory-objective-benchmark-hedge|ADR-051]] (Proposed).

## Self-test
> [!question]- A perfectly delta-hedged LP still loses money on average. Why?
> Hedging removes the directional exposure but not the short gamma. Arbitrageurs still trade against the pool on every move, so LVR ($\tfrac12\sigma^2\rho$ per unit value) remains, and the hedge adds its own trading costs.

> [!question]- Why does hedge drag in bps of capital grow with capital only once the band binds?
> If every check trades (the per-check move is much larger than the band), turnover is proportional to capital, so drag per unit of capital is flat. With a band that binds, turnover goes as $s^2/\varepsilon$, which grows with the square of capital, so drag per unit of capital rises.

> [!question]- The bot found hedge cost about 26% below a Gaussian model's estimate. Where does the difference come from?
> The pool's active bin does not move in about half of 30 s checks, so inventory moves in bursts. Its mean absolute move per check is 0.74× a Gaussian's with the same variance, and turnover follows the mean absolute move.

## Open questions
- (Add questions here after a quiz.)
