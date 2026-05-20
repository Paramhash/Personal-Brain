# Central Directory

## Learning Inbox (Awaiting Human Review)

```dataview
TABLE tags AS "Category", created AS "Ingested Date"
FROM "wiki"
WHERE reviewed = false
SORT created DESC
LIMIT 10
```

---

## Active Project: MAOPM

> Multi-Agent LLM Options Portfolio Manager — primary research and build target.

### Research & Planning
- [[wiki/research/research-agenda-options-maopm|Research Agenda (Q1–Q12)]]
- [[wiki/research/current research initiatives|current research initiatives]]
- [[wiki/research/tooling-requirements-maopm|Tooling Requirements (Tool 1 & 2)]]
- [[wiki/research/gex-scanner-logic-flow|GEX Scanner Logic Flow]]
- [[wiki/research/optimizing-greek-calculations-with-ray|Optimizing Greek Calculations with Ray]]
- [[wiki/research/strategies-by-regime-review-2026-05-19|Strategies by Regime Review (2026-05-19)]]
- [[wiki/research/hmm-estimates-of-probability-from-option-prices|HMM Approaches: Options Pricing & Agent Architecture]]

### Synthesis & Gap Analysis
- [[wiki/research/synthesis-2026-05-17|Synthesis 2026-05-17]]
- [[wiki/research/gap-analysis-2026-05-20|Gap Analysis 2026-05-20]]
- [[wiki/research/gap-analysis-2026-05-17|Gap Analysis 2026-05-17]]
- [[wiki/research/gap-analysis-2026-05-16|Gap Analysis 2026-05-16]]

### Architecture Concepts
- [[wiki/concepts/multi-agent-option-pricing-market-making-maopm|MAOPM Architecture Overview]]
- [[wiki/concepts/maopm-architecture-horizon-spread-gex-fusion|Horizon Spread ↔ GEX Fusion Architecture]]
- [[wiki/concepts/dual-engine-temporal-risk-architecture|Dual-Engine Temporal Risk Architecture]]
- [[wiki/concepts/dynamic-portfolio-greek-limits|Dynamic Portfolio Greek Limits]]
- [[wiki/concepts/regime-risk-scaling-engine|Regime Risk Scaling Engine]]
- [[wiki/concepts/board-directive-protocol|Board Directive Protocol]]

### Signal & Regime Concepts
- [[wiki/concepts/regime-divergence-ratio-rdr|Regime Divergence Ratio (RDR)]]
- [[wiki/concepts/gex-divergence-strategies|GEX Divergence Strategies]]
- [[wiki/concepts/market-regimes-rdr|Market Regimes — RDR Framework]]
- [[wiki/concepts/Option-Implied Regimes|Option-Implied Regimes]]
- [[wiki/concepts/option-implied-horizon-spread|Option-Implied Horizon Spread (ΔIHS)]]
- [[wiki/concepts/vvix|VVIX — Volatility of Volatility Index]]
- [[wiki/concepts/hidden-markov-model-hmm-in-finance|HMM Latent Regime Engine]]

### Strategy Concepts
- [[wiki/concepts/dispersion-trade-strategy|Dispersion Trade Strategy]]
- [[wiki/concepts/fragility-short-strategy|Fragility Short Strategy]]
- [[wiki/concepts/gamma-flip-mean-reversion-strategy|Gamma Flip Mean Reversion Strategy]]
- [[wiki/concepts/term-structure-catch-up-strategy|Term Structure Catch-Up Strategy]]

### JSON Schemas (Structured Agent I/O)
- [[wiki/entities/gex-regime-report-json-schema|GEX Regime Report Schema]]
- [[wiki/entities/vol-surface-summary-json-schema|Vol Surface Summary Schema]]
- [[wiki/entities/greek-exposure-report-json-schema|Greek Exposure Report Schema]]

---

## Infrastructure & Data

- [[wiki/entities/tastytrade-dxfeed-data-engine|Tastytrade / dxFeed Data Engine]] — real-time chain snapshots, BSM IV solver, OTM-blend surface (Tool 1 & 2 live data layer)
- [[wiki/entities/thetadata|ThetaData]] — historical options chain, constituent GEX, IV (Tool 1 & 2 history layer; required for HMM training)
- [[wiki/entities/polygon-io|Polygon.io]] — underlying price & volume; Tool 3 log returns
- [[wiki/entities/ray|Ray]] — distributed compute (Tool 1 parallelization)
- [[wiki/entities/interactive-brokers-api|Interactive Brokers TWS API]] — positions, P&L, execution
- [[wiki/entities/amd-ryzen-threadripper-3990x|AMD Threadripper 3990X]] — local compute hardware
- [[wiki/entities/thetaclient-python-library|ThetaClient Python Library]]
- [[wiki/entities/redis|Redis]] — caching layer

---

## Core Concept Index

- [[wiki/concepts/Master Concept Map|Global Systems Graph]]
- [[wiki/concepts/gamma-exposure-gex|Gamma Exposure (GEX)]]
- [[wiki/concepts/implied-volatility|Implied Volatility]]
- [[wiki/concepts/options-greeks|Options Greeks]]
- [[wiki/concepts/regime-detection|Regime Detection]]
- [[wiki/concepts/multi-agent-llm-financial-trading|Multi-Agent LLM Financial Trading]]
- [[wiki/concepts/structured-communication-protocol|Structured Communication Protocol]]
- [[wiki/research/options_portfolio_research_guide|Options Portfolio Research Guide]]

---

## Key Sources

- [[wiki/sources/lai-2022-horizon-spread|Lai 2022 — Horizon Spread (option-implied regimes)]]
- [[wiki/sources/Detecting stock market regimes from option prices|Detecting Stock Market Regimes from Option Prices]]
- [[wiki/sources/arxiv-2412.20138v7-tradingagents|TradingAgents (arXiv 2412.20138)]]
- [[wiki/sources/gex_compute_pipeline_blueprint|GEX Compute Pipeline Blueprint]]
