---
tags: ["research-agenda", "multi-agent-systems", "options-trading", "llm", "portfolio-management"]
created: 2026-05-16
reviewed: true
source_origin: "level1-analysis"
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
- How frequently should Greek limits be recalibrated — per-cycle, daily, weekly?
- Should different Greeks have independent regime scaling (e.g., tighten vega limits in vol expansion without changing delta limits)?

**Relevant vault concepts**: [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Regime Detection](../concepts/regime-detection.md), [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md)

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
- How do you simulate the LLM debate step in a backtesting loop without running live inference for every historical day? (Pre-cached agent decisions? Simplified rules-based proxy?)
- How do you measure alpha attributable to the multi-agent decision process vs. the underlying strategy type? (Control group: same strategy, mechanical execution)
- What performance metrics are most meaningful for an options portfolio? (Sharpe, Sortino, max drawdown, theta-adjusted return, PoP vs. realized profit rate)

**Relevant vault concepts**: [Financial Trading Performance Metrics](../concepts/financial-trading-performance-metrics.md), [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md), [Algorithmic Trading Strategies Baselines](../concepts/algorithmic-trading-strategies-baselines.md)

---

## Q5: What is the optimal LLM role assignment for GEX regime interpretation?

**Why it matters**: GEX regime analysis (from [gex-scanner-logic-flow.md](gex-scanner-logic-flow.md)) involves numerical computation (GEX Z-scores across 500 stocks) followed by qualitative interpretation (what does a decoupling regime imply for strategy?). The split between compute (rules-based / code) and interpretation (LLM) is not obvious.

**Sub-questions**:
- Should GEX Z-score computation be done in code (Python/Ray) with the LLM only interpreting the output, or can an LLM handle both?
- How much GEX context (index GEX, internal GEX index, top-5 weighted stock GEX, gamma flip level) is necessary for the LLM to produce accurate regime classifications?
- Can a deep-reasoning model (o1/o3) improve on FlashAlpha's pre-calculated regime labels, or is FlashAlpha's output sufficient as direct input?
- How should the GEX/Regime Analyst's output interact with the Volatility Analyst's output — are they independent signals or should they be synthesized before reaching the Strategy Research Team?

**Relevant vault concepts**: [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md), [Regime Detection](../concepts/regime-detection.md), [Agent Role Specialization](../concepts/agent-role-specialization-in-llm-systems.md)

**Relevant research**: [GEX Scanner Logic Flow](gex-scanner-logic-flow.md), [Optimizing Greek Calculations with Ray](optimizing-greek-calculations-with-ray.md)

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

**Why it matters**: A live options portfolio requires continuous management decisions (roll, close early, adjust strikes) in addition to new position decisions. These are fundamentally different tasks — management is reactive (existing positions approaching risk limits or DTE thresholds); initiation is proactive (deploying capital per strategy signal).

**Sub-questions**:
- Should management decisions (rolling, early close) use the same agent debate loop as new positions, or a separate faster path?
- What triggers a management review cycle vs. the standard analysis cycle? (DTE threshold, Greek breach, P&L threshold, event calendar alert)
- How should the system prioritize management actions over new position initiation when capital is constrained?

**Relevant vault concepts**: [Expiration Management](../concepts/expiration-management.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Event-Driven Options Risk](../concepts/event-driven-options-risk.md)

---

## Q8: Can TradingAgents-style performance claims be replicated and exceeded in options?

**Why it matters**: [TradingAgents](../entities/tradingagents-framework.md) demonstrated 23–26.62% cumulative returns vs. 7.78% buy-and-hold over Q1 2024 (Sharpe 5.60–8.21 vs. 2.31–3.53 for baselines). Options strategies have different return and risk characteristics — the comparison baseline must be options-native (mechanical iron condors, systematic covered calls, VIX-regime switching).

**Sub-questions**:
- What are the appropriate baseline options strategies for comparison? (Mechanical weekly iron condors on SPY? Tastytrade-style 45-DTE CSPs? Covered call ETFs like XYLD?)
- What Sharpe ratio is achievable with a well-implemented systematic short-vol strategy (no LLM)? Is the multi-agent overhead justified by the improvement?
- Over what time horizon and market conditions does LLM-driven strategy adaptation add the most value? (High-vol regimes? Regime transitions?)

**Relevant vault concepts**: [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md), [Algorithmic Trading Strategies Baselines](../concepts/algorithmic-trading-strategies-baselines.md), [Traditional Trading Strategies](../concepts/traditional-trading-strategies.md)

---

## Prioritization

| Question | Priority | Tractable Now? | Effort |
|---|---|---|---|
| Q3 — Communication schemas | Critical | Yes | Medium |
| Q2 — Dynamic Greek limits | High | Yes | Medium |
| Q4 — Backtesting approach | High | Partial (need data provider research) | High |
| Q1 — LLM vs. rules-based split | High | Yes | Low–Medium |
| Q5 — GEX/Regime LLM role | Medium | Yes | Medium |
| Q7 — Management vs. initiation | Medium | Yes | Medium |
| Q6 — Portfolio scope | Medium | Yes (decision, not research) | Low |
| Q8 — Performance baseline | Low (Phase 4) | Partial | High |

---
