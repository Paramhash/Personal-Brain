---
domain: cl-market-making
tags: [curriculum, amm]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 1
status: not-started
prerequisites: []
bot_links: [blueprint-ev-policy, adr-020-ev-numeraire-active-bin-pricing]
---

# M1 — AMM fundamentals

Part of [[00-cl-mm-timing-moc|the CL / market-making / timing curriculum]].

## Learning objectives
- Write the constant-product rule and derive the pool price and an LP position's value as functions of price.
- Explain who moves an AMM's price (arbitrageurs, against an external reference) and what the LP earns in exchange (fees).
- Show that an LP position is concave in price: short gamma, the root of every later cost.

## Concepts to cover (new notes the seed sources should create)
`automated-market-maker`, `constant-function-market-maker`, `constant-product-amm`, `arbitrage-in-amms`, `lp-position-value`.

## Existing vault notes to connect
[[liquidity]], [[option-greeks]] (gamma), [[transaction_costs_in_options]].

## Where it shows up in the bot
- The EV gate prices everything in the pool's own quote asset at the active-bin price:
  [[adr-020-ev-numeraire-active-bin-pricing|ADR-020]], [[blueprint-ev-policy|EV policy]] §5.

## Self-test
> [!question]- In a constant-product pool $x\,y = k$ (x base, y quote), what is the price, and what is the LP position worth at price $P$?
> Price $P = y/x$. Holdings are $x = \sqrt{k/P}$ and $y = \sqrt{kP}$, so the value in quote is $V(P) = xP + y = 2\sqrt{kP}$. It is concave in $P$.

> [!question]- Why does concavity mean the LP loses to "just holding" when price moves?
> Holding the initial tokens has value linear in $P$, tangent to $V(P)$ at the start price. A concave function lies below its tangent, so after any move the LP's value is lower: divergence (impermanent) loss. Equivalently the LP is short gamma.

> [!question]- What keeps the pool price in line with the market, and what does it cost the LP?
> Arbitrageurs trade against the pool whenever its price differs from the external price by more than the fee. They profit at the LP's expense. The fee is the LP's compensation (M4, M5).

## Open questions
- (Add questions here after a quiz.)
