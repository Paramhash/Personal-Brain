---
tags: ["research-initiative", "multi-agent-systems", "options-trading", "llm", "portfolio-management"]
created: 2026-05-16
reviewed: true
source_origin: "level1-analysis"
---
# Current Research Initiatives

## Active Initiative: Multi-Agent LLM Options Portfolio Manager (MAOPM)

**Status**: In Design  
**Started**: 2026-05-16  
**Horizon**: 12–18 months to paper-trading validation

---

### Motivation

The [TradingAgents framework](../entities/tradingagents-framework.md) demonstrates that a [multi-agent LLM system](../concepts/multi-agent-llm-financial-trading.md) modeled on a realistic trading firm structure — with role-specialized analysts, a debate-driven research team, and layered risk oversight — outperforms all single-agent and rules-based equity trading baselines by a substantial margin (Sharpe ratio improvement of +2–4 points; cumulative return improvement of 6–25%).

Options portfolio management is a strictly harder problem than equity selection:
- Positions have **four dimensions of risk** simultaneously: price (Delta), curvature (Gamma), volatility (Vega), and time (Theta)
- Strategy selection is **regime-dependent**: vol expansion favors long-vol strategies; vol contraction and stable [GEX](../concepts/gamma-exposure-gex.md) favor premium capture
- Execution requires **multi-leg combo orders** with complex fill logic
- [Regime detection](../concepts/regime-detection.md) and GEX microstructure signals are first-class inputs, not ancillary indicators

No existing multi-agent LLM framework addresses this domain natively. MAOPM is the first attempt to do so.

---

### Core Hypothesis

Specialized agents for real-time [Options Greeks](../concepts/options-greeks.md) management, volatility surface interpretation, and [GEX/regime](../concepts/gamma-exposure-gex.md) detection — combined with debate-driven strategy selection between a Long-Vol Researcher and a Short-Vol Researcher — can outperform static rules-based options strategies (covered calls, mechanical iron condors, buy-and-hold) on risk-adjusted return metrics over a rolling 12-month paper-trading horizon.

---

### Agent Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ANALYST TEAM (parallel)                   │
│  Greeks Analyst │ Vol Analyst │ GEX/Regime Analyst │ News/Catalyst │ Technical │
└───────────────────────────┬─────────────────────────────────────┘
                            │ structured reports (JSON-schema)
┌───────────────────────────▼─────────────────────────────────────┐
│                   STRATEGY RESEARCH TEAM (debate)                │
│              Long-Vol Researcher  ↔  Short-Vol Researcher        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ strategy recommendation + rationale
┌───────────────────────────▼─────────────────────────────────────┐
│                      PORTFOLIO MANAGER                           │
│         Greek target alignment │ position sizing │ approval      │
└───────────────────────────┬─────────────────────────────────────┘
                            │ trade proposal
┌───────────────────────────▼─────────────────────────────────────┐
│                    RISK MANAGEMENT TEAM                          │
│    Aggressive │ Conservative │ Neutral (three-perspective debate) │
└───────────────────────────┬─────────────────────────────────────┘
                            │ approved order (with hard limits)
┌───────────────────────────▼─────────────────────────────────────┐
│                      EXECUTION AGENT                             │
│         Multi-leg combo orders │ IB TWS API │ fill confirmation  │
└─────────────────────────────────────────────────────────────────┘
```

**State machine**: `ANALYZING → DEBATING → REVIEWING → APPROVED → EXECUTING → MONITORING`

Risk Management can interrupt and revert to ANALYZING on any Greek threshold breach.

---

### Two-Track Architecture

MAOPM runs on two parallel, structurally separate tracks:

```
╔══════════════════════════════════════════════════════════════════╗
║              TRACK 1: AGENT STATE TRACK (per-cycle, in-memory)  ║
║                                                                  ║
║  ANALYZING → DEBATING → REVIEWING → APPROVED → EXECUTING →      ║
║  MONITORING   (← Risk interrupt path)                           ║
║                                                                  ║
║  Analysts │ Researchers │ Portfolio Manager │ Risk Team │ Exec   ║
╚══════════════╤═══════════════════════════════╤═══════════════════╝
               │ Seam A: events + documents    │ Seam B: context
               ▼                               ▲
╔══════════════════════════════════════════════════════════════════╗
║           TRACK 2: OBSERVER TRACK (persistent, across cycles)   ║
║                                                                  ║
║  Recording Secretary  │  Board Interface  │  Performance Obs.   ║
║  (Decision Ledger)    │  (Active Directives)│ (Attribution Log) ║
╚══════════════════════════════════════════════════════════════════╝
```

**Seam A** (Track 1 → Track 2): Every state transition and structured document emitted by Track 1 is forwarded to the Recording Secretary for ledger append.

**Seam B** (Track 2 → Track 1): At the start of each ANALYZING phase, Track 1 receives a Prior Decisions Context Block containing: (a) last 5 approved proposals with outcomes, (b) Active Directives List, (c) last regime classification, (d) any unresolved Greek breach events, (e) latest Performance Observer summary.

| Track 2 Sub-agent | Role | Storage |
|---|---|---|
| [Recording Secretary](../concepts/recording-secretary-agent.md) | Appends all Track 1 events to the Decision Ledger; generates Seam B context block | Append-only ledger |
| [Board Interface](../concepts/board-directive-protocol.md) | Accepts Board directives; manages Active Directives List; handles Board interrupt path | Active directives store |
| Performance Observer | Post-trade attribution: links realized P&L, win rate, IV premium capture to originating agent recommendation | Attribution log |

Track 1 is **ephemeral per cycle** (in-memory). Track 2 is the **persistence layer** for the whole system — the Decision Ledger is the authoritative state on process restart.

---

### Agent Roles (Summary)

| Agent | Specialty | Key Output |
|---|---|---|
| Greeks Analyst | Portfolio net Δ/Γ/ν/Θ; threshold monitoring | Greek exposure report |
| Vol Analyst | IV rank/percentile, surface shape, vol regime | Volatility context report |
| GEX/Regime Analyst | GEX Z-score, decoupling regime, gamma flip | Regime classification report |
| News/Catalyst Analyst | Earnings calendar, FOMC, macro events | Event risk calendar |
| Technical Analyst | Price levels, S/R, trend, directional bias | Technical context report |
| Long-Vol Researcher | Argues straddles/calendars/debit spreads | Vol-bull case |
| Short-Vol Researcher | Argues iron condors/spreads/credit strategies | Vol-bear case |
| Portfolio Manager | Greek target alignment, sizing, trade approval | Trade proposal |
| Risk Team (×3) | Aggressive / Conservative / Neutral perspectives | Hard limits + sizing approval |
| Execution Agent | Multi-leg IB TWS combo order routing | Fill confirmation |

---

### Communication Protocol

Adapted from TradingAgents' hybrid approach:
- **Structured documents** (not free-text): Greek exposure reports, vol surface summaries, GEX regime reports — JSON-schema enforced to preserve numerical precision and eliminate the "telephone effect" over long agent conversations
- **Natural language debate**: Long-Vol vs. Short-Vol researcher exchange; Risk Team three-perspective deliberation
- **Interrupt path**: Risk Manager can halt execution on Greek threshold breach at any state

---

### Data Sources

| Data Type | Provider | Used By |
|---|---|---|
| Real-time Greeks, IV, options chain | [ThetaData](../entities/thetadata.md) | Greeks Analyst, Vol Analyst |
| GEX, regime labels | [FlashAlpha](../entities/flashalpha.md) | GEX/Regime Analyst |
| Underlying price, volume | [Polygon.io](../entities/polygon-io.md) | Technical Analyst, delta hedge triggers |
| News, earnings calendar | Financial news APIs | News/Catalyst Analyst |
| Live positions, P&L, margin | [Interactive Brokers API](../entities/interactive-brokers-api.md) | Portfolio Manager, Risk Team, Execution Agent |

GEX Z-score computation across 500 S&P 500 constituents uses [Ray](../entities/ray.md) distributed processing per the architecture in [[optimizing-greek-calculations-with-ray.md]].

---

### LLM Backbone Strategy

| Model Type | Role | Examples |
|---|---|---|
| Quick-thinking | Data retrieval, report parsing, Greek routing | gpt-4o-mini |
| Deep-reasoning | Strategy debate, risk review, Portfolio Manager decisions | o1/o3 series |
| Specialist | News sentiment analysis | Domain-tuned models |

No GPU required — fully API-based, model-agnostic (mirrors TradingAgents design).

---

### Implementation Milestones

| Milestone | Scope | Status |
|---|---|---|
| M0 — Observer Track | Decision Ledger (SQLite); Recording Secretary service; Board Directive Protocol; Seam A/B interfaces | Not started |
| M1 — Foundation | ThetaData + Polygon + IB TWS pipeline; Greeks Analyst + Vol Analyst; portfolio state | Not started |
| M2 — Strategy Generation | GEX/Regime Analyst; debate loop; Portfolio Manager | Not started |
| M3 — Risk & Execution | Risk Team (3 perspectives); Execution Agent; Greek alert system | Not started |
| M4 — Full Loop | Closed-loop paper trading; backtesting; performance vs. baselines; Performance Observer attribution | Not started |

---

### Knowledge Gaps Being Addressed

The following concept files are being created to support this initiative:
- [[../concepts/recording-secretary-agent.md|Recording Secretary Agent]] — Observer Track agent; Decision Ledger maintenance; Seam A/B interfaces
- [[../concepts/decision-ledger.md|Decision Ledger]] — Append-only audit trail; entry schema; query patterns; storage options
- [[../concepts/board-directive-protocol.md|Board Directive Protocol]] — Directive structure; hard-block vs. advisory; Board interrupt path; enforcement points
- [[../concepts/implied-volatility.md|Implied Volatility]] — IV rank, IV percentile, vol crush/expansion
- [[../concepts/volatility-surface-dynamics.md|Volatility Surface Dynamics]] — skew, term structure (extends [[../concepts/volatility-surfaces.md]])
- [[../concepts/options-strategies.md|Options Strategies]] — single-leg and multi-leg strategy taxonomy
- [[../concepts/portfolio-greeks-management.md|Portfolio Greeks Management]] — net Greek targets, delta-neutral, gamma scalping
- [[../concepts/options-risk-metrics.md|Options Risk Metrics]] — max loss, PoP, expected value, buying power
- [[../concepts/expiration-management.md|Expiration Management]] — DTE selection, rolling, pin risk
- [[../concepts/event-driven-options-risk.md|Event-Driven Options Risk]] — earnings IV crush, FOMC vol spikes, binary events

---

### Scope Decisions

- **Domain**: Equities options only (no crypto, futures, forex)
- **Execution**: Interactive Brokers paper trading first; live trading after M4 validation
- **Compute**: API-based LLMs only; no GPU / custom ML (Phase 1)
- **Backtesting**: Requires historical options data with realistic bid/ask; ORATS or equivalent TBD

---

### Related Research Notes

- [[gap-analysis-2026-05-16.md]] — Gap analysis that identified missing sources and shallow coverage this initiative addresses
- [[gex-scanner-logic-flow.md]] — GEX Z-score computation logic reused directly by the GEX/Regime Analyst
- [[optimizing-greek-calculations-with-ray.md]] — Compute architecture for real-time Greek calculation at scale
- [[research-agenda-options-maopm.md]] — Open research questions for this initiative
- [[../concepts/recording-secretary-agent.md]] — Observer Track agent spec
- [[../concepts/decision-ledger.md]] — Decision Ledger schema
- [[../concepts/board-directive-protocol.md]] — Board Directive Protocol

---
