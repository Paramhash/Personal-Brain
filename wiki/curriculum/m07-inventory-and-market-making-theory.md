---
domain: cl-market-making
tags: [curriculum, inventory-control, market-making]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 7
status: not-started
prerequisites: [m01-amm-fundamentals]
bot_links: [adr-051-inventory-objective-benchmark-hedge, adr-025-dynamic-reratio-imbalance-calculation, blueprint-hedge-engine]
---

# M7 — Inventory and market-making theory

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m01-amm-fundamentals|M1]].

## Learning objectives
- Explain the three costs a market maker is paid for: order processing, inventory risk (Ho–Stoll) and adverse
  selection (Glosten–Milgrom, Kyle).
- Derive Avellaneda–Stoikov's reservation price and optimal spread, and say what each term means.
- Map the theory onto an LP, which cannot quote per trade: its controls are range location and width, deployment
  timing, and the hedge.
- Say what an LP is trying to grow — quote value, base count, or both — and why that changes the hedge.

## Concepts to cover
`market-making-inventory-risk`, `adverse-selection`, `glosten-milgrom-model`, `kyle-lambda`, `avellaneda-stoikov-model`,
`reservation-price`, `lp-as-passive-market-maker`.

## Existing vault notes to connect
[[liquidity]], [[order-flow]], [[multi-agent-option-pricing-market-making-maopm]].

## Where it shows up in the bot
- What the bot should grow, and what its hedge targets: [[adr-051-inventory-objective-benchmark-hedge|ADR-051]]
  (Proposed; hedge to a benchmark SOL count). It answers the bot's research notes 00–02, which go into the vault
  through `raw/` (bridge).
- The 50/50 re-ratio before deploying: [[adr-025-dynamic-reratio-imbalance-calculation|ADR-025]].
- The hedge target today: [[blueprint-hedge-engine|hedge engine]].

## Self-test
> [!question]- Write Avellaneda–Stoikov's reservation price and explain it.
> $r = s - q\,\gamma\,\sigma^2\,(T - t)$: mid price $s$, inventory $q$, risk aversion $\gamma$, time left $T-t$. A long position (q > 0) shades quotes down so the maker is more likely to sell; the shading grows with risk aversion, volatility and time left.

> [!question]- What does a Glosten–Milgrom spread pay for, and what is its LP equivalent?
> It compensates the maker for losing to informed traders, who trade only when they know the price will move. For an LP the equivalent is arbitrage flow (LVR), paid for by the fees from uninformed flow.

> [!question]- An LP cannot change its quotes per trade. Which levers does it have instead?
> Where and how wide to place the range, when to deploy or withdraw, the liquidity shape, and how much to hedge.

## Open questions
- (Add questions here after a quiz.)
