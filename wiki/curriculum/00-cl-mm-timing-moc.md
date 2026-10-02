---
domain: cl-market-making
tags: [curriculum, moc]
aliases: [CL curriculum, market making curriculum]
created: 2026-10-02
reviewed: false
source_origin: level1-analysis
---

# Concentrated liquidity, market making and timing — map of content

**Purpose:** a learning track that ends where the trading bot's decision lives: whether to deploy liquidity, where,
how wide, and how to hedge. Each module ties theory to the place it shows up in `dlmm-hedge-bot`, so what you learn
can be checked against measured numbers.

**Why this order:** the bot's EV gate currently refuses to deploy. On the live window the hurdle is about
234 bps/day, against a measured fee yield of 80–141 bps/day
([[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost|ADR-052]],
[[cl-policy-report-2026-10-01|CL policy report]]). Modules 1–5 explain the cost and revenue sides of that comparison.
Modules 6–9 explain its inputs: volatility, inventory, hedging and funding. Modules 10–11 turn it into a decision.

## Modules

| # | Module | Prerequisites | Bot anchor |
|---|---|---|---|
| 1 | [[m01-amm-fundamentals\|AMM fundamentals]] | — | [[blueprint-ev-policy\|EV policy]] |
| 2 | [[m02-concentrated-liquidity-math\|Concentrated liquidity math]] | 1 | [[blueprint-range-planning\|range planning]] |
| 3 | [[m03-bin-based-cl-dlmm\|Bin-based CL: DLMM and Whirlpools]] | 2 | [[adr-034-range-width-rule-for-fine-binned-pools\|ADR-034]] |
| 4 | [[m04-lvr-and-impermanent-loss\|LVR and impermanent loss]] | 2 | [[adr-052-ev-gate-prices-range-dependent-lvr-and-hedge-cost\|ADR-052]] |
| 5 | [[m05-fee-economics\|Fee economics]] | 3 | [[adr-050-fee-yield-from-on-chain-bin-fee-counters\|ADR-050]] |
| 6 | [[m06-volatility-estimation-and-forecasting\|Volatility estimation and forecasting]] | — | [[adr-047-provisional-sigma-estimator\|ADR-047]] |
| 7 | [[m07-inventory-and-market-making-theory\|Inventory and market-making theory]] | 1 | [[adr-051-inventory-objective-benchmark-hedge\|ADR-051]] |
| 8 | [[m08-hedging-lp-exposure\|Hedging LP exposure]] | 4, 9 | [[blueprint-hedge-engine\|hedge engine]] |
| 9 | [[m09-perpetuals-and-funding\|Perpetuals and funding]] | — | [[adr-031-funding-drag-numeraire-and-unknown-cost-policy\|ADR-031]] |
| 10 | [[m10-timing-as-regime-conditional-deployment\|Timing as regime-conditional deployment]] | 4, 6 | [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot\|ADR-038]] |
| 11 | [[m11-strategic-lps-and-the-decision-rule\|Strategic LPs and the decision rule]] | 5, 8, 10 | [[adr-046-real-time-hurdle-rate-restates-the-ev-gate\|ADR-046]] |

```dataview
TABLE module AS "#", status, prerequisites
FROM "wiki/curriculum"
WHERE module
SORT module ASC
```

## How to use it
1. Drop a module's seed sources into `raw/` ([[seed-sources|seed sources]]) and run `python ingest.py --once`.
   Gemini creates the concept and source notes.
2. In the IDE, ask Level 1 to **teach** the module (see `LEVEL1.md`). It writes an explainer grounded in the vault's
   notes and links the new concepts into the module.
3. Ask Level 1 to **quiz** you. Wrong answers become open questions in the module.
4. After each daily bot report, run **bot-digest**. It names which module the day's numbers touch.
5. Set the module's `status` to `in-progress` or `done` as you go.

## Read-only bot mirrors
- [[adr-index|All ADRs]] · [[blueprint-ev-policy|EV policy]] · [[blueprint-backtest-research|research simulator]]
- Findings: [[finding-ev-gate-calibration-2026-10-01|EV gate calibration]] ·
  [[finding-ev-gate-vs-simulator-2026-10-01|EV gate vs simulator]] ·
  [[finding-pool-sigma-forecast-2026-10-01|pool σ forecast]] · [[finding-fee-counter-g1-2026-09-30|fee counters (G1)]]
