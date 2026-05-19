---
tags: ["synthesis", "multi-agent-systems", "options-trading", "regime-detection", "gex", "llm", "infrastructure"]
created: 2026-05-17
reviewed: false
source_origin: "level1-analysis"
---
# Vault Synthesis: Conceptual Compass

> This note is the single entry point for understanding how the vault's knowledge fits together. It identifies the five core conceptual clusters, their internal logic, and the non-obvious connections between clusters that define the research frontier.

---

## The Central Thesis

Options markets are unusual: they encode *forward-looking* crowd expectations in a structured, arbitrage-constrained form. This gives options data — implied volatility, skew, term structure, gamma exposure — a regime-detection advantage over historical price or return series. The vault's core bet is that **LLM agents specialized to read this encoded signal, debate under uncertainty, and enforce Greek discipline can outperform static rule-based options systems** on risk-adjusted returns. The [TradingAgents framework](../entities/tradingagents-framework.md) provides the organizational blueprint; the [MAOPM initiative](current%20research%20initiatives.md) extends it to the structurally richer domain of options portfolios.

---

## Cluster 1: Infrastructure Pipeline

**Core files**: [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md), [ThetaData](../entities/thetadata.md), [Polygon.io](../entities/polygon-io.md), [FlashAlpha](../entities/flashalpha.md), [Interactive Brokers API](../entities/interactive-brokers-api.md), [Ray](../entities/ray.md), [Multiprocessing](../entities/multiprocessing.md), [AMD Ryzen Threadripper 3990X](../entities/amd-ryzen-threadripper-3990x.md)

The infrastructure cluster presents a **compute-vs-cost trade-off**. Pre-computed analytics providers (FlashAlpha, ~$239/mo) require no math but constrain what you can calculate. Raw-data providers (ThetaData, ~$25–60/mo; Polygon.io, ~$200/mo) combined with high-core local hardware (Threadripper 3990X: 128 threads) enable custom GEX aggregation, novel regime metrics, and backtesting at a total cost competitive with pre-computed subscriptions.

The choice has downstream consequences: FlashAlpha's regime labels are a black box — the MAOPM cannot interrogate, modify, or extend them. ThetaData + local computation gives the [GEX Scanner Logic Flow](gex-scanner-logic-flow.md) full transparency into the Z-score pipeline, which is required if the GEX/Regime Analyst agent is to reason about the *confidence* of a regime classification, not just its label.

**Internal logic**: Raw data → parallelized Greek calculation (Ray/multiprocessing) → GEX aggregation per stock → GEX Z-score and Internal GEX Index → regime classification input.

---

## Cluster 2: Market Mechanics — Two Independent Signal Families

**Core files**: [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [Gamma Flip](../concepts/gamma-flip.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md), [Implied Volatility](../concepts/implied-volatility.md), [Volatility Surfaces](../concepts/volatility-surfaces.md), [Volatility Surface Dynamics](../concepts/volatility-surface-dynamics.md), [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md), [Stock Market Regimes](../concepts/Stock%20Market%20Regimes.md), [Regime Detection](../concepts/regime-detection.md)

The vault contains two distinct mechanisms for reading market state — both derived from options markets, but measuring different things:

**Signal Family A — GEX / Dealer Microstructure**
- Measures *current dealer hedging behavior* and its feedback effect on price dynamics.
- Positive GEX → dealers long gamma → stabilizing (buy dips, sell rallies) → mean-reversion regime.
- Negative GEX → dealers short gamma → accelerating (sell dips, buy rallies) → momentum/trend regime.
- The [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md) ($\text{Index GEX} / \sum \text{Component GEX}$) determines whether the gamma flip level is a reliable signal: inside the coherent band (0.5–2.0), gamma rules work; outside it, GEX divergence strategies apply.
- GEX is *real-time*: it captures today's hedging pressures. It does not directly forecast multi-week regime transitions.

**Signal Family B — Option-Implied Macro Regime**
- Measures *market participants' aggregate expectations* embedded in option prices across strikes and expirations.
- IV rank/percentile (IVR/IVP): coarse regime label (high-vol / low-vol).
- Vol surface shape: skew steepness and term structure inversion as stress indicators (see [Volatility Surface Dynamics](../concepts/volatility-surface-dynamics.md)).
- Horizon spread (Wan Ni Lai, 2022): $HS = \text{ERP}_{180d} - \text{ERP}_{30d}$; turns negative during crises when short-term risk premium exceeds long-term; detected the COVID-19 regime shift in December 2019 — three months before historical returns or GARCH volatility signaled it. Source: [Detecting stock market regimes from option prices](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md).
- Option-implied metrics are *forward-looking*: they capture what the market prices as likely, not what has already happened.

**The gap between these two families is the vault's most important unresolved structural issue.** Neither the [current research initiatives](current%20research%20initiatives.md) document nor any agent role note specifies how Signal Family A (GEX/microstructure) and Signal Family B (vol surface/option-implied macro) are fused before reaching the Strategy Research Team debate. They are documented in separate concept clusters with no bridge note.

---

## Cluster 3: Strategy Selection — IV Regime × GEX Overlay

**Core files**: [Options Strategies](../concepts/options-strategies.md), [Expiration Management](../concepts/expiration-management.md), [Event-Driven Options Risk](../concepts/event-driven-options-risk.md), [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md), [Fragility Short Strategy](../concepts/fragility-short-strategy.md), [Dispersion Trade Strategy](../concepts/dispersion-trade-strategy.md), [Gamma Flip Mean Reversion Strategy](../concepts/gamma-flip-mean-reversion-strategy.md), [Term Structure Catch-Up Strategy](../concepts/term-structure-catch-up-strategy.md), [Zero Days to Expiration](../concepts/zero-days-to-expiration.md)

Strategy selection operates on a two-dimensional decision surface:

| | Low IVR (< 30) | Moderate IVR (30–50) | High IVR (> 50) |
|---|---|---|---|
| **Coherent GEX / Positive GEX** | Calendars, debit spreads, LEAPS | Defined-risk spreads, diagonals | Iron condors, credit spreads, CSPs |
| **Divergent GEX (Ratio > 2.0)** | Fragility shorts on weak components | Dispersion trades | Dispersion trades, term structure catch-up |
| **Divergent GEX (Ratio < 0.5)** | Long vol on fragile index | Gamma flip mean reversion | Gamma flip mean reversion |

Expiration management constrains the DTE dimension: 21–45 DTE is the premium-selling sweet spot; 21 DTE is the forced-exit threshold for short-vol to avoid asymmetric gamma blow-up; event windows (earnings, FOMC) impose hard no-open rules. These temporal constraints interact with GEX signal reliability: 0DTE GEX is pinning-dominated; 45DTE GEX reflects structural positioning.

**The Term Structure Catch-Up strategy** is the most sophisticated integration of both signal families: 0DTE positive GEX (daily pinning) plus 45DTE negative GEX (structural weakness) triggers a calendar spread — sell 0DTE theta, hold 45DTE long-vol protection. This is the only vault concept that explicitly uses multi-expiration GEX signals together.

---

## Cluster 4: Agent Architecture — Options-Extended TradingAgents

**Core files**: [Multi-Agent LLM Financial Trading](../concepts/multi-agent-llm-financial-trading.md), [Agent Role Specialization](../concepts/agent-role-specialization-in-llm-systems.md), [Structured Communication Protocol](../concepts/structured-communication-protocol.md), [Structured Communication in Multi-Agent LLM Systems](../concepts/structured-communication-in-multi-agent-llm-systems.md), [ReAct Prompting Framework](../concepts/react-prompting-framework.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Options Risk Metrics](../concepts/options-risk-metrics.md), all agent role notes

The [TradingAgents framework](../entities/tradingagents-framework.md) established: specialized roles + structured document communication + natural language debate + ReAct loop = measurably better risk-adjusted returns than all tested baselines (Sharpe 5.60–8.21 vs. 2.31–3.53). MAOPM transplants this architecture into options by replacing the equity Analyst Team with three options-specific analysts (Greeks, Vol, GEX/Regime) and replacing the Trader's directional bet with a **Greek-target constraint system**.

The key design decision this creates: in equities, the Trader asks "buy/sell/hold X shares." In options, the Portfolio Manager must ask "which multi-leg structure achieves the strategy signal while keeping net delta within ±$2,000, net vega within ±$3,000, and net theta positive?" This is a constrained optimization problem that the equity architecture never encounters. Structured communication is therefore even more critical in MAOPM: Greek exposure reports must be machine-readable (JSON schema) to feed the constraint checker, not just human-readable for the debate.

The MAOPM state machine (ANALYZING → DEBATING → REVIEWING → APPROVED → EXECUTING → MONITORING) adds an interrupt path when Greek thresholds are breached — a real-time risk circuit that has no equivalent in TradingAgents' batch-cycle architecture.

---

## Cluster 5: Performance & Evaluation

**Core files**: [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md), [Financial Trading Performance Metrics](../concepts/financial-trading-performance-metrics.md), [Algorithmic Trading Strategies Baselines](../concepts/algorithmic-trading-strategies-baselines.md), [Traditional Trading Strategies](../concepts/traditional-trading-strategies.md)

The evaluation cluster is equity-centric and underdeveloped for options. Cumulative return, Sharpe, and max drawdown are necessary but insufficient for an options portfolio:
- **Theta-adjusted return**: how much of the P&L came from time decay vs. realized moves?
- **PoP vs. realized profit rate**: does the system's actual win rate match the modeled probability of profit?
- **IV premium capture**: is the system systematically selling options when IV > realized volatility (positive expected value)?

The existing baselines (buy-and-hold, MACD, SMA, KDJ+RSI, ZMR) are all equity strategies. Options-native baselines needed for fair MAOPM evaluation — mechanical weekly iron condors, systematic covered-call ETFs (XYLD), VIX-regime switching — are absent from the vault.

---

## Non-Obvious Cross-Cluster Connections

### 1. TradingGPT Layered Memory ↔ DTE Tier Management
[TradingGPT](../entities/tradinggpt.md) introduced short-term, medium-term, and long-term memory tiers to overcome LLM context window limits. [Expiration Management](../concepts/expiration-management.md) defines three management time horizons: 0DTE/intraday (extreme gamma), 21–45 DTE (premium-selling core), 90–180+ DTE (LEAPS/structural). These are structurally identical — three time-horizon tiers, each with distinct signal salience and decision frequency. A MAOPM agent with layered memory could retrieve 0DTE hedging history from short-term memory, open position Greeks from medium-term memory, and structural regime context from long-term memory, without context-window overflow.

### 2. Regime Divergence Ratio as Greek Limit Scaler
The [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md) determines whether the market is in a coherent or divergent dealer-hedging regime. Inside the coherent band (0.5–2.0), gamma flip levels are reliable and standard Greek limits apply. Outside the band — a violent re-hedging event is likely. This maps directly to [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md)'s open question about dynamic Greek limit adjustment: the ratio could serve as the primary scaler (coherent band → standard limits; approaching band edge → tighten vega and gamma limits; outside band → activate divergence-strategy mode and suspend new premium selling).

### 3. Telephone Effect + Options Numerical Precision = Same Problem
The [Structured Communication Protocol](../concepts/structured-communication-protocol.md) solves the telephone effect (information degradation through agent handoffs). Options data has the same vulnerability from a different direction: a 4-leg iron condor has 4 sets of per-leg Greeks plus net Greeks plus max loss plus PoP — approximately 20 numerical values. Passing this as natural language between agents guarantees precision loss. JSON schema enforcement solves both problems simultaneously: structured documents preserve numerical precision *and* prevent information loss through the agent graph.

### 4. Lai (2022) Horizon Spread as Vol Analyst Input
The [Detecting Stock Market Regimes](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md) paper's horizon spread metric ($HS = \text{ERP}_{180d} - \text{ERP}_{30d}$, estimated from option prices nonparametrically) outperformed IV and historical returns for regime detection by a wide margin (4.6% indecisive probability vs. 16% for returns, 34% for volatility). The Vol Analyst role in MAOPM is currently specified to monitor IVR/IVP and vol surface shape — both Signal Family B metrics. Adding horizon spread computation gives the Vol Analyst a leading indicator that has empirically detected crises months before standard vol metrics, enabling the Long-Vol/Short-Vol debate to shift earlier.

### 5. Event Calendar Convergence
[Event-Driven Options Risk](../concepts/event-driven-options-risk.md) defines a News Analyst–maintained event calendar that triggers position review 2 days pre-earnings and blocks new short-vol opens. [Expiration Management](../concepts/expiration-management.md) defines an expiration calendar that triggers 21 DTE roll alerts, pin risk monitoring at 3 PM ET, and assignment risk escalation. Both are time-indexed lists of future position-action requirements. In implementation, these should resolve to a single unified alert queue consumed by the interrupt path of the MAOPM state machine — not two separate monitoring processes.

### 6. Observer Track as Longitudinal Memory Across All Clusters
The five clusters above each generate data that is ephemeral in the current design: infrastructure metrics, regime classifications, strategy debates, agent recommendations, and performance results all exist only within a single cycle. The [Two-Track Architecture](current%20research%20initiatives.md) introduced in May 2026 addresses this directly: the [Recording Secretary](../concepts/recording-secretary-agent.md) observes all five clusters' outputs via Seam A and persists them in the [Decision Ledger](../concepts/decision-ledger.md). This creates the first longitudinal memory layer spanning all clusters simultaneously:
- **Cluster 1 (Infrastructure)**: Data provider outages and compute anomalies are logged as `state-transition` and `analyst-report` events.
- **Cluster 2 (Market Mechanics)**: Each regime classification is a ledger entry, enabling regime-transition history to be queried across cycles.
- **Cluster 3 (Strategy Selection)**: Every strategy recommendation and its disposition (approved/rejected/overridden) is traceable to the market state that prompted it.
- **Cluster 4 (Agent Architecture)**: Debate transcripts are append-only entries; agent accountability (which agent recommended the losing trade?) becomes answerable.
- **Cluster 5 (Performance)**: The Performance Observer links every `performance-summary` entry back to its originating `agent-recommendation` entry via `position_id`, closing the feedback loop that the evaluation cluster currently lacks.

The [Board Directive Protocol](../concepts/board-directive-protocol.md) adds a governance dimension: Board instructions become first-class ledger entries, their enforcement is logged, and their effect on strategy outcomes is queryable. This is the mechanism by which the operator (Board) exercises oversight without disrupting the autonomous agent cycle.

---

## Conceptual Map

```
INFRASTRUCTURE                MARKET MECHANICS               AGENT ARCHITECTURE
─────────────────             ──────────────────             ──────────────────
ThetaData ──────────→         GEX Z-scores         ─────→   GEX/Regime Analyst
Polygon.io          │         Regime Div. Ratio     │
FlashAlpha          │         (Signal Family A)     │         Vol Analyst  ←── Horizon Spread
Ray/Multiprocessing │                               │         Greeks Analyst      (Lai 2022)
Threadripper 3990X  │         IV / Skew / Term      ─────→   (Signal Family B)
                    │         Horizon Spread                        │
                    │         (Signal Family B)                     ▼
                    └──→ Options Tape ──────────────→   Long-Vol ↔ Short-Vol Debate
                                                              │
STRATEGY SELECTION                                            ▼
──────────────────                                     Portfolio Manager
IVR × GEX overlay                                      (Greek constraint check)
→ strategy space                                              │
→ DTE tier selection                                          ▼
→ event calendar gate                                  Risk Management Team
                                                       (3-perspective debate)
EVALUATION                                                    │
──────────────                                                ▼
Options-native metrics                                 Execution Agent → IBKR
(PoP rate, theta-adj.)                                 (multi-leg combo orders)
Options-native baselines                                      │
(needed; absent)                                             ▼

OBSERVER TRACK (Track 2 — persistent, spans all cycles and all clusters above)
────────────────────────────────────────────────────────────────────────────────
← ─ ─ ─ ─ ─ ─ ─ ─ ─ Seam A (all events in from Track 1) ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
Recording Secretary  │  Board Interface       │  Performance Observer
(Decision Ledger)    │  (Active Directives)   │  (Attribution Log)
─ ─ ─ ─ ─ ─ ─ ─ ─ ─ Seam B (context block out → ANALYZING start) ─ ─ ─ ─ ─ ─ →
```

---

*This note should be read alongside [current research initiatives](current%20research%20initiatives.md) for the operational roadmap and [research-agenda-options-maopm](research-agenda-options-maopm.md) for open questions.*
