---
domain: cl-market-making
tags: [curriculum, decision-rule, game-theory]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 11
status: not-started
prerequisites: [m05-fee-economics, m08-hedging-lp-exposure, m10-timing-as-regime-conditional-deployment]
bot_links: [adr-046-real-time-hurdle-rate-restates-the-ev-gate, adr-015-fsm-cold-start-and-ev-gate, adr-040-sunk-deployment-rent-is-an-ev-term, blueprint-ev-policy, finding-f-026-the-ev-gate-has-no-rent-term-so-wider-ranges-look-cheaper-than-they-are]
---

# M11 — Strategic LPs and the decision rule

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m05-fee-economics|M5]], [[m08-hedging-lp-exposure|M8]]
and [[m10-timing-as-regime-conditional-deployment|M10]].

## Learning objectives
- Explain how LPs compete for the same fee flow: dilution, just-in-time (JIT) liquidity, and the equilibrium of range
  choices.
- Write the bot's decision rule and read its hurdle rate: deploy only when expected fees cover LVR, hedge drag,
  funding and rent, with a margin over execution friction.
- Name the levers that can turn a failing gate into a passing one, and the cost of each.

## Concepts to cover
`lp-competition`, `just-in-time-liquidity`, `hurdle-rate`, `ev-gate`, `nash-equilibrium-range-choice`.

## Existing vault notes to connect
[[multi-agent-option-pricing-market-making-maopm]], [[regime-risk-scaling-engine]], [[liquidity]].

## Where it shows up in the bot
- The rule: `net_ev = fees − LVR − hedge_drag − funding − rent ≥ 1.5 × (slippage + gas)`,
  [[blueprint-ev-policy|EV policy]] §3–§4, [[adr-015-fsm-cold-start-and-ev-gate|ADR-015]].
- The same rule in bps/day: [[adr-046-real-time-hurdle-rate-restates-the-ev-gate|ADR-046]].
- Rent as a cost of wider ranges: [[adr-040-sunk-deployment-rent-is-an-ev-term|ADR-040]],
  [[finding-f-026-the-ev-gate-has-no-rent-term-so-wider-ranges-look-cheaper-than-they-are|F-026]].
- LP competition: the bot's research note 02 on Nash strategies, which goes into the vault through `raw/` (bridge).

## Self-test
> [!question]- On the live window the gate's hurdle is about 234 bps/day and measured fees are 80–141. Name the levers that could close the gap.
> Higher fee yield (a pool or fee tier with more volume relative to liquidity), a wider range (lower density, so lower LVR and hedge drag, but also a smaller fee share), cheaper hedging (a wider band, slower checks or maker execution, at the cost of delta risk), or deploying only in low-σ regimes (M10). Each trades one cost against another.

> [!question]- Why is rent subtracted inside net EV rather than added to the friction side of the inequality?
> The friction side carries a 1.5× safety margin over estimated, variable costs. Sunk rent is exact arithmetic, so it needs no margin; putting it inside net EV also leaves the ratified inequality unchanged (ADR-040).

> [!question]- What does JIT liquidity do to a passive LP's fee yield?
> A JIT provider adds liquidity just before a large trade and removes it right after, taking a share of that trade's fees without bearing the LVR between trades. The passive LP's fee share on the largest, least toxic flow is diluted.

## Open questions
- (Add questions here after a quiz.)
