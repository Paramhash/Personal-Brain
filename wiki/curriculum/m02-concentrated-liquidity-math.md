---
domain: cl-market-making
tags: [curriculum, uniswap-v3, concentrated-liquidity]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 2
status: not-started
prerequisites: [m01-amm-fundamentals]
bot_links: [blueprint-range-planning, blueprint-liquidity-position-manager, adr-034-range-width-rule-for-fine-binned-pools]
---

# M2 — Concentrated liquidity math

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m01-amm-fundamentals|M1]].

## Learning objectives
- Use Uniswap v3's liquidity $L$ on a range $[P_a, P_b]$ to compute token holdings inside, below and above the range.
- Explain capital efficiency: the same capital gives a larger $L$ in a narrower range, so more fees **and** more loss.
- Read an in-range position as an option position: a covered call above, a short put below.

## Concepts to cover
`concentrated-liquidity`, `liquidity-l-uniswap-v3`, `tick`, `virtual-reserves`, `lp-position-as-option`, `capital-efficiency`.

## Existing vault notes to connect
[[option-greeks]], [[black-scholes-model]], [[options-strategies]].

## Where it shows up in the bot
- Range width and placement: [[blueprint-range-planning|range planning]],
  [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]] (width from σ),
  [[blueprint-liquidity-position-manager|position manager]].

## Self-test
> [!question]- For liquidity $L$ on $[P_a, P_b]$ with price $P$ inside the range, what are the holdings?
> Base $x = L\,(1/\sqrt{P} - 1/\sqrt{P_b})$ and quote $y = L\,(\sqrt{P} - \sqrt{P_a})$. Above $P_b$ the position is all quote; below $P_a$ it is all base.

> [!question]- Price rises through the top of the range. What does the position hold, and which option payoff is that like?
> All quote: the base was sold progressively on the way up, at prices inside the range. That is like a covered call that has been exercised: upside capped at the range top.

> [!question]- Why does narrowing the range raise both fee income and loss per unit of capital?
> The same capital buys more $L$, so the position takes a larger share of every trade (more fees), but its inventory also changes faster with price (higher value density $\rho$). LVR and hedge turnover both scale with $\rho$ (M4, M8).

## Open questions
- (Add questions here after a quiz.)
