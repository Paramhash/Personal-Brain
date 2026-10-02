---
domain: cl-market-making
tags: [curriculum, dlmm, meteora, orca]
aliases: []
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
module: 3
status: not-started
prerequisites: [m02-concentrated-liquidity-math]
bot_links: [adr-034-range-width-rule-for-fine-binned-pools, adr-022-range-planner-numeraire-alignment, adr-044-read-only-orca-whirlpool-adapter-for-the-monitor, blueprint-liquidity-position-manager]
---

# M3 — Bin-based CL: Meteora DLMM and Orca Whirlpools

Part of [[00-cl-mm-timing-moc|the curriculum]]. Builds on [[m02-concentrated-liquidity-math|M2]].

## Learning objectives
- Explain DLMM bins: each bin trades at one fixed price $(1 + \text{binStep})^{\text{id}}$; only the active bin holds both tokens.
- Compare liquidity shapes (Spot, Curve, BidAsk) by where they put value relative to the active bin.
- Compare bins (DLMM, Liquidity Book) with ticks (Uniswap v3, Orca Whirlpools), and DLMM's dynamic (variable) fee.
- Explain why a bin pool's price moves in bursts, and what that does to hedging.

## Concepts to cover
`dlmm-bin`, `bin-step`, `active-bin`, `liquidity-shape-spot-curve-bidask`, `dynamic-fee-dlmm`, `whirlpool-tick-spacing`.

## Existing vault notes to connect
[[liquidity]], [[realized-vol-intraday]].

## Where it shows up in the bot
- The bot's pool is SOL/USDC with bin step 4 bps, Curve shape:
  [[blueprint-liquidity-position-manager|position manager]],
  [[adr-022-range-planner-numeraire-alignment|ADR-022]] (bin ↔ price conversion),
  [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]].
- Orca Whirlpool as a second venue: [[adr-044-read-only-orca-whirlpool-adapter-for-the-monitor|ADR-044]].
- The burst behaviour, measured: [[finding-ev-gate-calibration-2026-10-01|EV gate calibration]] (step 2).

## Self-test
> [!question]- What price does a swap get inside the active bin, and when does the price change?
> A single fixed price: within a bin the swap is constant-sum, with no price impact. The price changes only when the active bin is exhausted and the swap moves into the next bin.

> [!question]- The bot measured the pool's active bin unchanged in about 50% of 30-second checks. What does that do to a delta hedge?
> The inventory changes in jumps rather than smoothly, so its mean absolute move per check is smaller than a Gaussian's of the same variance (0.74× here, the "burst factor"). A hedge checked every 30 s trades about 26% less than a Gaussian model predicts.

> [!question]- How does the Curve shape differ from Spot in where the value sits, and why does that matter for cost estimates?
> Curve concentrates value at the active bin and tapers towards the edges; Spot is uniform. Price spends time away from the centre, so a cost model that uses the centre density overstates Curve's cost: the life-averaged density is about 0.71× the centre density for the bot's 202-bin window.

## Open questions
- (Add questions here after a quiz.)
