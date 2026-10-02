---
domain: cl-market-making
tags: [curriculum, funding, perpetuals]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 9
status: not-started
prerequisites: []
bot_links: [adr-031-funding-drag-numeraire-and-unknown-cost-policy, adr-029-binance-premium-index-mark-price, adr-018-binance-userdata-freshness]
---

# M9 — Perpetual futures and funding

Part of [[00-cl-mm-timing-moc|the curriculum]].

## Learning objectives
- Explain how a perpetual future stays near spot without expiry: the funding payment between longs and shorts, set
  from the premium of the perp over its index.
- Know mark price, index price and the funding schedule (every 8 hours on Binance), and read the sign of a funding rate.
- Treat funding as a carry cost (or income) of the LP's short hedge, and know when an unknown funding rate must
  block a decision.

## Concepts to cover
`perpetual-futures`, `funding-rate`, `mark-price-vs-index-price`, `basis`, `funding-as-carry`.

## Existing vault notes to connect
[[delta_hedging]], [[cost-of-capital-spreads]].

## Where it shows up in the bot
- Funding drag in the EV gate, priced in the pool's quote asset, and refusing when the rate is unknown:
  [[adr-031-funding-drag-numeraire-and-unknown-cost-policy|ADR-031]].
- Mark price source: [[adr-029-binance-premium-index-mark-price|ADR-029]].
- Freshness of the hedge venue's data: [[adr-018-binance-userdata-freshness|ADR-018]].

## Self-test
> [!question]- Funding is +0.01% per 8 hours. Who pays whom, and what does that mean for the LP's short hedge?
> Positive funding means longs pay shorts, so the short hedge **earns** about 0.03% of its notional per day. Negative funding means the short pays.

> [!question]- Why does the bot's gate refuse, rather than assume zero, when the funding rate is unknown?
> Funding is a cost. Setting an unknown cost to zero raises net EV, so the gate could pass because the pipeline did not know the cost rather than because the cost was small (ADR-031).

> [!question]- What keeps a perpetual's price near spot?
> When the perp trades above its index, longs pay shorts, which rewards shorting and pulls the price down; below the index, the reverse.

## Open questions
- (Add questions here after a quiz.)
