---
domain: cl-market-making
tags: [curriculum, fee-economics]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 5
status: not-started
prerequisites: [m03-bin-based-cl-dlmm]
bot_links: [adr-033-fee-yield-measurement-route, adr-050-fee-yield-from-on-chain-bin-fee-counters, blueprint-fee-growth, finding-fee-counter-g1-2026-09-30, cl-policy-report-2026-10-01]
---

# M5 — Fee economics

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m03-bin-based-cl-dlmm|M3]].

## Learning objectives
- Compute an LP's fee yield from its share of the liquidity that trades: own value ÷ (bin value + own value).
- Separate fee volume into uninformed (noise) flow, which pays the LP, and arbitrage flow, which costs it (LVR).
- Explain why fee yield on capital falls as more liquidity joins (dilution) and rises in narrower ranges.
- Know how a measured fee yield differs from a modelled one, and why the bot measures it before using it.

## Concepts to cover
`fee-yield`, `fee-growth-counter`, `lp-fee-share`, `toxic-flow`, `noise-traders-vs-arbitrageurs`, `volume-to-tvl`.

## Existing vault notes to connect
[[liquidity]], [[order-flow]].

## Where it shows up in the bot
- How fee yield may be ratified: [[adr-033-fee-yield-measurement-route|ADR-033]]; Route 4, from on-chain per-bin
  fee counters: [[adr-050-fee-yield-from-on-chain-bin-fee-counters|ADR-050]], [[blueprint-fee-growth|fee growth]].
- Verifying the counters: [[finding-fee-counter-g1-2026-09-30|G1 finding]].
- Measured yield per policy: [[cl-policy-report-2026-10-01|CL policy report]] §I (80–141 bps/day for the top
  policies).

## Self-test
> [!question]- How does the bot measure what a position would have earned without holding one?
> It samples each bin's cumulative fee-per-share counters every 5 minutes. A hypothetical position is credited its share — own value ÷ (bin value + own value) — of each bin's fee growth over the intervals it would have been open.

> [!question]- Measured fees are 80–141 bps/day and the gate's hurdle is about 234. Why is the measured yield still locked out of the gate?
> ADR-050 Amendment 1: until the gate's cost side was correct (ADR-052), a real fee figure would have made a range-blind gate pass positions the simulator showed losing money. The lock holds until ADR-052 is in a promoted root.

> [!question]- Why does fee yield on capital fall as more LPs join the same range?
> The fee volume is fixed by traders; more liquidity in the same bins splits it more ways, so each unit of capital earns less.

## Open questions
- (Add questions here after a quiz.)
