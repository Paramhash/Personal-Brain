---
tags:
  - research-agenda
  - multi-agent-systems
  - options-trading
  - llm
  - portfolio-management
created: 2026-05-16
reviewed: false
source_origin: level1-analysis
---
# Research Agenda: Multi-Agent LLM Options Portfolio Manager (MAOPM)

This note documents the highest-value open research questions for the [MAOPM initiative](Current%20Research%20Initiatives.md). Each question is tractable now given existing vault knowledge and available tools, and each represents a meaningful knowledge gain if answered.

---

## Q1: Which options strategies are most amenable to LLM-driven selection?

**Why it matters**: LLM agents reason in natural language. Some options decisions involve nuanced qualitative judgment (e.g., "the skew shape suggests fear rather than structural demand"); others are purely quantitative (e.g., "IVR = 78, PoP = 82%"). The former may benefit from LLM debate; the latter may not.

**Sub-questions**:
- Which decisions are better made by a rules engine (hard limits, PoP thresholds) vs. an LLM agent (strategy rationale, contextual override)?
- Does the Long-Vol vs. Short-Vol debate improve outcomes over a purely rules-based IV-regime → strategy mapping?
- Can LLMs effectively reason about multi-leg payoff diagrams, or do they require structured representations (breakeven levels, max loss, PoP) as input?

**Relevant vault concepts**: [Options Strategies](../concepts/options-strategies.md), [Multi-Agent LLM Financial Trading](../concepts/multi-agent-llm-financial-trading.md), [ReAct Prompting Framework](../concepts/react-prompting-framework.md)

---

## Q2: How should portfolio-level Greek limits be defined and dynamically adjusted?

**Why it matters**: Static Greek limits (fixed delta/vega caps) ignore market context. A ±$500 delta limit in a low-vol, positive-GEX regime is overly conservative; the same limit in a negative-GEX, vol-expansion regime may be dangerously permissive.

**Sub-questions**:
- What is the optimal function mapping regime state → Greek limit scaling? (Linear? Step-function? Regime-specific presets?)
- Should the [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md) serve as the primary scaler? Proposed rule: coherent band (0.5–2.0) → standard limits; ratio approaching band edge → tighten vega/gamma limits; outside band → suspend new premium selling, activate divergence-strategy mode. Is this the correct trigger function, or should other regime signals dominate?
- How frequently should Greek limits be recalibrated — per-cycle, daily, weekly?
- Should different Greeks have independent regime scaling (e.g., tighten vega limits in vol expansion without changing delta limits)?

**Relevant vault concepts**: [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Regime Detection](../concepts/regime-detection.md), [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md)

---

## Q3: What communication structures minimize information loss for options-specific data?

**Why it matters**: The [TradingAgents framework](../entities/tradingagents-framework.md) found that structured documents outperform pure natural language for preserving information across agent handoffs (the "telephone effect"). Options data is highly numerical and structured — strikes, expirations, Greeks, PoP. Passing these as free text will degrade precision.

**Sub-questions**:
- What JSON schema should the Greek exposure report, vol surface summary, and GEX regime report follow?
- Which information should be passed as structured data vs. narrative summary vs. both?
- How should the structured data representation handle multi-leg positions (e.g., iron condor: 4 legs, 4 sets of Greeks, net Greeks, max loss, PoP)?
- What is the minimum sufficient context an LLM needs to reason effectively about an options portfolio state?

**Relevant vault concepts**: [Structured Communication Protocol](../concepts/structured-communication-protocol.md), [Multi-Agent Systems](../concepts/multi-agent-systems.md), [Options Risk Metrics](../concepts/options-risk-metrics.md)

---

## Q4: How to backtest a multi-agent system with realistic options fills and slippage?

**Why it matters**: Backtesting equity strategies is straightforward (close prices, no expiration). Options backtesting is fundamentally harder: options expire, bid/ask spreads are wide, IV surfaces must be reconstructed historically, and fill assumptions are critical (mid? natural? improvement?).

**Sub-questions**:
- Which historical options data provider supports realistic bid/ask reconstruction? (ORATS, OptionsDX, ThetaData historical — compare coverage, cost, Greeks availability)
- **Historical GEX availability is a concrete blocker**: GEX Z-scores require a 30-day rolling mean and standard deviation of per-stock GEX. This means any backtest needs at minimum 30 trading days of per-contract historical Greeks before the first signal can be computed. ThetaData provides historical per-contract Greeks; does any other provider? What is the earliest available date for this data?
- How do you simulate the LLM debate step in a backtesting loop without running live inference for every historical day? (Pre-cached agent decisions? Simplified rules-based proxy?)
- How do you measure alpha attributable to the multi-agent decision process vs. the underlying strategy type? (Control group: same strategy, mechanical execution)
- What performance metrics are most meaningful for an options portfolio? (Sharpe, Sortino, max drawdown, theta-adjusted return, PoP vs. realized profit rate, IV premium capture rate)

**Relevant vault concepts**: [Financial Trading Performance Metrics](../concepts/financial-trading-performance-metrics.md), [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md), [Algorithmic Trading Strategies Baselines](../concepts/algorithmic-trading-strategies-baselines.md)

**Relevant gap**: [options-backtesting-methodology.md](../research/gap-analysis-2026-05-17.md) (Gap 1.4) — no concept note yet exists

---

## Q5: What is the optimal LLM role assignment for multi-signal regime interpretation?

**Why it matters**: The MAOPM Regime Analyst must synthesize two structurally distinct signal families — (A) GEX/microstructure signals (dealer positioning, gamma flip, Regime Divergence Ratio) and (B) option-implied macro signals (IV term structure, vol skew, and the horizon spread metric from [Lai 2022](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md)). Signal Family A is real-time and microstructure-sensitive; Signal Family B is forward-looking and detected the COVID-19 regime shift in December 2019 — three months before GEX or historical-vol methods signaled it. The split between compute (rules-based/code) and interpretation (LLM) is not obvious, and the fusion architecture has not been specified.

**Sub-questions**:
- Should GEX Z-score computation and horizon spread estimation both be done in code (Python/Ray), with the LLM only interpreting the synthesized output, or can an LLM handle signal integration?
- How much GEX context (index GEX, internal GEX index, top-5 weighted stock GEX, gamma flip level, Regime Divergence Ratio) is necessary for the LLM to produce reliable regime classifications?
- Can a deep-reasoning model (o1/o3) improve on FlashAlpha's pre-calculated regime labels, or is FlashAlpha's output sufficient as direct input?
- How should the GEX/Regime Analyst's output interact with the Volatility Analyst's horizon spread output — are these independent signals to be debated, or should a single fused Regime Analyst hold both?
- When GEX/microstructure signals and horizon spread signals conflict (e.g., GEX positive/stabilizing but horizon spread inverting toward crisis), which signal should take precedence in the strategy debate?

**Relevant vault concepts**: [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md), [Regime Detection](../concepts/regime-detection.md), [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md), [Agent Role Specialization](../concepts/agent-role-specialization-in-llm-systems.md)

**Relevant research**: [GEX Scanner Logic Flow](gex-scanner-logic-flow.md), [Optimizing Greek Calculations with Ray](optimizing-greek-calculations-with-ray.md), [Synthesis 2026-05-17](synthesis-2026-05-17.md) (Cluster 2)

**Relevant gap**: [option-implied-erp-horizon-spread.md](gap-analysis-2026-05-17.md) concept note not yet created (Gap 1.3)

---

## Q6: What is the appropriate portfolio scope for MAOPM Phase 1?

**Why it matters**: The system could manage a single underlying (e.g., SPY) or a multi-symbol portfolio. Complexity, data requirements, and Greek netting all scale with the number of underlyings.

**Sub-questions**:
- Should Phase 1 focus on a single liquid ETF (SPY, QQQ) or a basket of 5–10 individual stocks (similar to TradingAgents' AAPL/GOOGL/AMZN/NVDA/META)?
- How does the multi-symbol case change the Portfolio Manager's Greek management challenge? (Net Greeks across different underlyings require correlation assumptions)
- Is the [Magnificent 7](../entities/magnificent-7-stocks.md) basket a natural starting universe given existing vault coverage?

**Relevant vault concepts**: [Multi-Agent LLM Financial Trading](../concepts/multi-agent-llm-financial-trading.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md)

---

## Q7: How should the system handle position management vs. new position initiation?

**Why it matters**: A live options portfolio requires continuous management decisions (roll, close early, adjust strikes) in addition to new position decisions. These are fundamentally different tasks — management is reactive (existing positions approaching risk limits or DTE thresholds); initiation is proactive (deploying capital per strategy signal). The vault's [Expiration Management](../concepts/expiration-management.md) note documents time-critical requirements — 21 DTE forced-close rule, pin risk monitoring at 3:00 PM ET on expiration day, assignment risk escalation when |delta| > 0.70 — that are **incompatible with a standard analysis-cycle cadence**. These are not periodic events; they are triggered events requiring sub-minute response at certain DTE thresholds. A slow LLM debate loop cannot handle them. This pushes a fast-path management agent into Phase 2, not Phase 3 as currently planned.

**Sub-questions**:
- Should management decisions (rolling, early close) use the same agent debate loop as new positions, or a separate deterministic fast path (rules engine) for time-critical events?
- What triggers a management review cycle vs. the standard analysis cycle? Specific thresholds: DTE ≤ 21 (roll review), |delta| > 0.20 at DTE < 14 (escalation alert), underlying within 0.5% of short strike at 3:00 PM ET on expiration day (forced close).
- How should the unified alert queue (merging the expiration management calendar and the event-driven options risk calendar) be implemented to avoid duplicate or conflicting alerts on the same position?
- How should the system prioritize management actions over new position initiation when capital is constrained?

**Relevant vault concepts**: [Expiration Management](../concepts/expiration-management.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Event-Driven Options Risk](../concepts/event-driven-options-risk.md)

**Relevant gap**: Gap 3.4 in [gap-analysis-2026-05-17](gap-analysis-2026-05-17.md) — event calendar and expiration calendar not yet integrated

---

## Q8: Can TradingAgents-style performance claims be replicated and exceeded in options?

**Why it matters**: [TradingAgents](../entities/tradingagents-framework.md) demonstrated 23–26.62% cumulative returns vs. 7.78% buy-and-hold over Q1 2024 (Sharpe 5.60–8.21 vs. 2.31–3.53 for baselines). Options strategies have different return and risk characteristics — the comparison baseline must be options-native (mechanical iron condors, systematic covered calls, VIX-regime switching).

**Sub-questions**:
- What are the appropriate baseline options strategies for comparison? (Mechanical weekly iron condors on SPY? Tastytrade-style 45-DTE CSPs? Covered call ETFs like XYLD?)
- What Sharpe ratio is achievable with a well-implemented systematic short-vol strategy (no LLM)? Is the multi-agent overhead justified by the improvement?
- Over what time horizon and market conditions does LLM-driven strategy adaptation add the most value? (High-vol regimes? Regime transitions?)

**Relevant vault concepts**: [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md), [Algorithmic Trading Strategies Baselines](../concepts/algorithmic-trading-strategies-baselines.md), [Traditional Trading Strategies](../concepts/traditional-trading-strategies.md)

---

---

## Q9: How does the option-implied horizon spread complement GEX-based regime detection in the MAOPM architecture?

**Why it matters**: Wan Ni Lai (2022) demonstrates that the horizon spread — the difference between the option-implied equity risk premium at 180-day and 30-day horizons — achieves only 4.6% probability mass in the "indecisive" zone (0.1–0.9 posterior probability) vs. 34% for GARCH volatility and 16% for historical returns. It detected COVID-19 in December 2019 while returns and volatility only signaled in March 2020. This makes it a materially superior leading indicator for macro regime shifts. The GEX Z-score and Regime Divergence Ratio capture dealer microstructure (days-to-weeks horizon). The horizon spread captures macro regime transitions (weeks-to-months horizon). These are complementary, not competing, signals. How they are fused in the MAOPM agent architecture is unspecified.

**Sub-questions**:
- What is the minimum data infrastructure required to compute the horizon spread in near-real-time? (Requires per-strike put/call prices at 30-day and 180-day tenors; is this available from ThetaData or Polygon.io at the required granularity?)
- Should the horizon spread be computed by the Vol Analyst agent (it is derived from the vol surface / option prices) or by a dedicated Regime Analyst agent (it is a regime signal)?
- How should a horizon spread inversion (HS < 0, signaling short-term risk > long-term) affect the Long-Vol/Short-Vol Researcher debate — does it immediately shift the prior toward long-vol, or is it one input among several?
- What is the lag structure between horizon spread inversion and GEX regime transition? If horizon spread leads GEX by weeks, can MAOPM position early before GEX confirms?
- How do you handle the case where horizon spread signals a macro crisis regime while GEX/Regime Divergence Ratio still signals a coherent, stable microstructure regime?

**Relevant vault concepts**: [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md), [Regime Detection](../concepts/regime-detection.md), [Volatility Surface Dynamics](../concepts/volatility-surface-dynamics.md), [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md)

**Relevant source**: [Detecting Stock Market Regimes from Option Prices](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md)

**Relevant gap**: [option-implied-erp-horizon-spread.md](gap-analysis-2026-05-17.md) concept note needed (Gap 1.3); Lai source stub needs upgrade (Gap 3.2)

---

## Q10: Can TradingGPT's layered memory architecture improve MAOPM position management across DTE tiers?

**Why it matters**: [TradingGPT](../entities/tradinggpt.md) introduced short-term, medium-term, and long-term memory tiers specifically to overcome LLM context-window limits in multi-horizon trading tasks. The MAOPM manages positions across structurally distinct time horizons: 0DTE/intraday (extreme gamma, minute-by-minute delta hedging), 21–45 DTE (premium-selling core, periodic rolling decisions), and 90–180+ DTE LEAPS (structural, monthly reviews). These three horizons map precisely onto TradingGPT's three memory tiers. Without layered memory, a MAOPM agent reviewing a 0DTE hedge decision would need to carry full context about all 45-DTE positions and LEAPS simultaneously — context-window overflow or token cost explosion is the likely failure mode.

**Sub-questions**:
- What information belongs in each memory tier for MAOPM? (Short-term: intraday delta hedges, 0DTE alerts, breach events; Medium-term: open 21–45 DTE position Greeks, recent vol regime classifications, last debate outcomes; Long-term: structural regime state, LEAPS positions, performance history, strategy bias parameters)
- What is the eviction policy for each tier? (Short-term: rolling session window; Medium-term: position close or roll; Long-term: regime transition event)
- Does layered memory require persistent storage (database) for the medium and long-term tiers, given that MAOPM runs continuously and must survive process restarts?
- Can layered memory be implemented as a structured document (JSON) rather than a vector embedding store, given that MAOPM's data is numerical and structured rather than textual and semantic?
- How does the Portfolio Manager agent query cross-tier memory when making a position sizing decision that depends on both current Greeks (medium-term) and structural regime (long-term)?

**Relevant vault concepts**: [Expiration Management](../concepts/expiration-management.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Multi-Agent Systems](../concepts/multi-agent-systems.md), [Zero Days to Expiration](../concepts/zero-days-to-expiration.md)

**Relevant entity**: [TradingGPT](../entities/tradinggpt.md) (source stub incomplete — see Gap 2.2 in [gap-analysis-2026-05-17](gap-analysis-2026-05-17.md))

---

## Q11: How should the Observer Track be designed to minimize overhead on the Agent State Track?

**Why it matters**: The Observer Track (Recording Secretary, Board Interface, Performance Observer) runs in parallel with every Track 1 cycle. If Seam A event emission introduces latency into the Track 1 critical path — particularly in EXECUTING, where sub-second order routing matters — the audit infrastructure becomes a liability. The design must keep Track 1 fully decoupled from Track 2's write performance.

**Sub-questions**:
- Should Seam A be synchronous (Track 1 waits for Recording Secretary acknowledgment) or asynchronous (fire-and-forget to an event queue)? The latter eliminates latency coupling but introduces the possibility of missed events on crash.
- What is the minimum event set Track 2 must receive to reconstruct a full cycle audit? Can analyst reports be omitted from Seam A (stored separately in Track 1) and only the summary events forwarded?
- How should the Prior Decisions Context Block (Seam B) be pre-computed — eagerly at cycle end or lazily at the next ANALYZING start? Lazy generation risks adding latency to cycle startup.
- Should the Performance Observer run synchronously at position close or in a nightly batch? The latter avoids any impact on live trading cycles.
- What is the maximum acceptable size for the Seam B context block before it materially consumes LLM context window budget in the ANALYZING phase?

**Relevant vault concepts**: [Recording Secretary Agent](../concepts/recording-secretary-agent.md), [Decision Ledger](../concepts/decision-ledger.md), [Structured Communication Protocol](../concepts/structured-communication-protocol.md), [Multi-Agent Systems](../concepts/multi-agent-systems.md)

**Relevant research**: [Current Research Initiatives](Current%20Research%20Initiatives.md) — Two-Track Architecture section

---

## Q12: What is the correct state persistence model for MAOPM across process restarts?

**Why it matters**: The current MAOPM design specifies Track 1 as in-memory per cycle. Track 2's Decision Ledger is the authoritative persistent state. But "persistent state" for a live options portfolio is multi-layered: the ledger records decisions, but the Portfolio Manager also needs current position Greeks, open order status, and margin availability on restart — data that lives in the broker API (IB TWS), not the ledger. The rehydration sequence on restart is unspecified and could leave Track 1 agents with stale or incomplete state.

**Sub-questions**:
- What is the complete set of state that Track 1 needs at ANALYZING start after a process restart? (Candidate list: open positions + current Greeks from IB TWS; Active Directives from Decision Ledger; last regime classification from Decision Ledger; unresolved Greek breach events from Decision Ledger; last N cycle summaries from Decision Ledger.)
- Should MAOPM maintain a separate "portfolio snapshot" store (updated after every EXECUTING phase) distinct from the Decision Ledger, or can the portfolio state be fully reconstructed from the ledger's `fill` and `expiry-alert` entries?
- What is the restart sequence? Proposed order: (1) load Active Directives from ledger, (2) query IB TWS for live position state, (3) query IB TWS for current Greeks, (4) load last regime classification from ledger, (5) generate Seam B context block, (6) enter ANALYZING. Is this the correct order and are there dependencies?
- How should MAOPM handle the case where IB TWS is unavailable on restart (e.g., outside market hours)? Should it enter a suspended state until market open or proceed with stale Greeks from the ledger?
- Does the Decision Ledger's SQLite recommendation (from [Decision Ledger](../concepts/decision-ledger.md)) support the concurrent read pattern needed during rehydration without locking?

**Relevant vault concepts**: [Decision Ledger](../concepts/decision-ledger.md), [Recording Secretary Agent](../concepts/recording-secretary-agent.md), [Board Directive Protocol](../concepts/board-directive-protocol.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md)

**Relevant entity**: [Interactive Brokers API](../entities/interactive-brokers-api.md)

---

## Prioritization

| Question | Priority | Tractable Now? | Effort | Phase |
|---|---|---|---|---|
| Q3 — Communication schemas | Critical | Yes | Medium | 1 |
| Q2 — Dynamic Greek limits + Regime Div. Ratio scaler | High | Yes | Medium | 2 |
| Q1 — LLM vs. rules-based split | High | Yes | Low–Medium | 1–2 |
| Q7 — Management fast-path vs. initiation | **High** *(elevated)* | Yes | Medium | **2** *(moved up)* |
| Q5 — Multi-signal regime fusion (GEX + horizon spread) | **High** *(elevated)* | Yes — Lai paper ingested | Medium | 2 |
| Q9 — Horizon spread in MAOPM architecture | High | Yes — Lai paper ingested | Medium | 2 |
| Q4 — Backtesting approach + historical GEX blocker | High | Partial (GEX data availability TBD) | High | 4 |
| Q10 — TradingGPT layered memory → DTE tiers | Medium | Partial (source stub incomplete) | Medium | 2–3 |
| Q11 — Observer Track overhead and Seam A/B design | **High** | Yes | Medium | **0** |
| Q12 — State persistence and restart rehydration | **High** | Yes | Medium | **0** |
| Q6 — Portfolio scope | Medium | Yes (decision, not research) | Low | 1 |
| Q8 — Performance baseline vs. options-native strategies | Low | Partial | High | 4 |

---
