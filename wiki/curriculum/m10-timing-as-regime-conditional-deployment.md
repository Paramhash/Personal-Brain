---
domain: cl-market-making
tags: [curriculum, market-timing, gex, regime]
aliases: [market timing for LPs]
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 10
status: not-started
prerequisites: [m04-lvr-and-impermanent-loss, m06-volatility-estimation-and-forecasting]
bot_links: [adr-034-range-width-rule-for-fine-binned-pools, adr-038-gex-walls-are-selected-on-the-correct-side-of-spot, adr-041-wall-buffer-and-proximity-exit-are-one-policy, blueprint-gex-intelligence, finding-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds]
---

# M10 — Timing as regime-conditional deployment

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m04-lvr-and-impermanent-loss|M4]] and
[[m06-volatility-estimation-and-forecasting|M6]].

**Framing:** for an LP, "timing" is not predicting price direction; the evidence for that is weak. It is deciding
**when to be deployed and how wide**, given a regime that changes the expected fee income and the expected LVR. That
is a decision the EV gate can actually make.

## Learning objectives
- Explain how dealer gamma (GEX), call/put walls and the zero-gamma level relate to volatility and pinning, and what
  the evidence for that is.
- Use regime signals (volatility level, GEX sign, HMM states) to condition the deployment decision and range width.
- Separate what timing evidence supports (volatility regimes persist; trend-following has documented returns) from
  what it does not (short-horizon price prediction).

## Concepts to cover
`regime-conditional-deployment`, `range-width-from-volatility`, `dealer-gamma-and-volatility`, `wall-envelope`.

## Existing vault notes to connect
[[gamma-exposure-gex]], [[gamma-flip]], [[spot-to-gamma-wall-distance]], [[market-regime-pinning]],
[[market-regime-gamma-squeeze]], [[regime-detection]], [[hidden-markov-model]], [[stock-market-regimes]],
[[trend-following-trading]], [[volatility-clustering]].

## Where it shows up in the bot
- Range width from σ: [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]].
- Walls from dealer gamma: [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]],
  [[adr-041-wall-buffer-and-proximity-exit-are-one-policy|ADR-041]],
  [[blueprint-gex-intelligence|GEX intelligence]].
- What the data showed: [[finding-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds|F-024]],
  [[finding-f-021-the-call-wall-oscillates-between-strikes-and-the-planner-accepts-uncontaining-bounds|F-021]],
  [[finding-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule|F-022]].
- Regime σ multipliers, measured but not yet used: [[cl-policy-report-2026-10-01|CL policy report]] §G.

## Self-test
> [!question]- Why frame LP timing as "when and how wide" rather than "up or down"?
> An LP's P&L is fees minus LVR minus hedge costs, which depend on volume and σ² far more than on direction. Volatility regimes are persistent and forecastable to a degree, so they inform the decision; price direction largely is not.

> [!question]- Positive dealer gamma is associated with what kind of price behaviour, and why does that matter to an LP?
> Dealers hedging long gamma sell into rallies and buy dips, which damps moves and favours pinning. Lower realized σ means lower LVR and hedge cost for the same fees, so it is a better regime to be deployed in.

> [!question]- F-024 found the wall envelope routinely narrower than the σ-width. What does that tell you about using walls to set the range?
> The walls were constraining the range more tightly than the volatility rule wanted, so the σ rule never set the width. A tighter range concentrates value and raises LVR and hedge cost.

## Open questions
- (Add questions here after a quiz.)
