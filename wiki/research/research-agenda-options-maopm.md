---
tags:
  - research-agenda
  - multi-agent-systems
  - options-trading
  - llm
  - portfolio-management
created: 2026-05-16
reviewed: 2026-05-19
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

**Status**: Substantially answered (~85%). All four sub-questions resolved by `dynamic-portfolio-greek-limits.md`. Open gap: the horizon spread (Q9) has no integration point in the 3-layer trigger hierarchy — it is a macro leading signal that should sit at or adjacent to Layer 2 but is currently absent from the dynamic limits architecture.

**Sub-questions**:
- ✅ What is the optimal function mapping regime state → Greek limit scaling? → Bi-symmetric sigmoid M(x) ∈ [0,1]; linear (sluggish at boundaries) and step-function (cliff effects) explicitly rejected. See [Dynamic Portfolio Greek Limits](../concepts/dynamic-portfolio-greek-limits.md).
- ✅ Should RDR serve as the primary scaler? → RDR is Layer 3 of a 3-layer hierarchy. Layer 1 (Index GEX sign — binary hard cap on Γ/ν) and Layer 2 (VVIX >3σ tail acceleration — suspend all short-vega) take precedence over the sigmoid. Open gap: horizon spread not yet integrated as a trigger layer.
- ✅ How frequently should Greek limits be recalibrated? → 3-tier governance: (1) daily batch EOD (RDR, term structure, net GEX recalculated; M(x) coefficients locked), (2) intraday streaming (gamma flip crossing or VVIX >3σ spike — immediate override), (3) per-cycle monthly expiry (baseline L_base capacity recalibration). See [Dynamic Portfolio Greek Limits](../concepts/dynamic-portfolio-greek-limits.md).
- ✅ Should different Greeks have independent regime scaling? → Yes. Asymmetric rules: Γ/ν contract aggressively (M→0) in negative GEX / RDR >2.0; Δ expands (M>1.0) in the same regime to absorb noise without churn; Θ expands maximally (M→1.0) in coherent + high absolute GEX regime to harvest variance risk premium.

**Relevant vault concepts**: [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Regime Detection](../concepts/regime-detection.md), [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md)

---

## Q3: What communication structures minimize information loss for options-specific data?

**Why it matters**: The [TradingAgents framework](../entities/tradingagents-framework.md) found that structured documents outperform pure natural language for preserving information across agent handoffs (the "telephone effect"). Options data is highly numerical and structured — strikes, expirations, Greeks, PoP. Passing these as free text will degrade precision.

**Status**: Answered. All four sub-questions resolved as of 2026-05-19.

**Sub-questions**:
- ✅ What JSON schema should the Greek exposure report, vol surface summary, and GEX regime report follow? → [Greek Exposure Report Schema](../entities/greek-exposure-report-json-schema.md), [Vol Surface Summary Schema](../entities/vol-surface-summary-json-schema.md), [GEX Regime Report Schema](../entities/gex-regime-report-json-schema.md)
- ✅ Which information should be passed as structured data vs. narrative summary vs. both? → Deterministic data (Greeks, strikes, IV, regime enums) → structured fields. Qualitative interpretation → single explicitly-labelled `*_narrative` field per report. See [LLM Agent Data Handoffs](../concepts/llm-agent-data-handoffs-structured-communication.md).
- ✅ How should the structured data representation handle multi-leg positions? → `Position` definition in the Greek Exposure Report schema: `strategy_type` enum + `legs[]` array (max 4) with per-leg Greeks and `risk_metrics` block (max_loss, max_profit, pop, breakeven_prices, bpr, current_pl).
- ✅ What is the minimum sufficient context an LLM needs to reason effectively about an options portfolio state? → GEX regime block + vol regime block + portfolio_totals + active_breaches + active_directives + last 3 cycle summaries. ~2,000–3,000 tokens for a 5–10 position portfolio. See [LLM Agent Data Handoffs](../concepts/llm-agent-data-handoffs-structured-communication.md).

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

**Status**: ~45% answered. Sub-question 1 resolved by Q3 schema design. Sub-question 3 resolved — FlashAlpha dropped (see below). Sub-questions 2, 4, and 5 remain open.

**Sub-questions**:
- ✅ Should GEX Z-score computation and horizon spread estimation both be done in code, with the LLM only interpreting? → Yes — established by Q3 schema design. Both the GEX rules engine (pseudocode in [GEX Regime Report Schema](../entities/gex-regime-report-json-schema.md)) and `horizon_spread` ([Vol Surface Summary Schema](../entities/vol-surface-summary-json-schema.md)) are computed in code; LLMs receive structured JSON outputs and interpret, not compute.
- How much GEX context (index GEX, internal GEX index, top-5 weighted stock GEX, gamma flip level, Regime Divergence Ratio) is necessary for the LLM to produce reliable regime classifications?
- ✅ Can a deep-reasoning model (o1/o3) improve on FlashAlpha’s pre-calculated regime labels, or is FlashAlpha’s output sufficient as direct input? → **Moot — FlashAlpha dropped.** Since Tool 1 (GEX Regime Divergence Engine) already computes GEX Z-scores, the Internal GEX Index, and the RDR from raw ThetaData options chain data, regime classification (`coherent` / `artificial_stability` / `hidden_strength`, `microstructure_bias`, `new_positions_permitted`) is a rules-based output of the same pipeline at no additional cost. FlashAlpha’s black-box labels are eliminated. Optional one-time cross-validation during Tool 1 development only. See [Tooling Requirements](tooling-requirements-maopm.md).
- How should the GEX/Regime Analyst's output interact with the Volatility Analyst's horizon spread output — are these independent signals to be debated, or should a single fused Regime Analyst hold both?
- When GEX/microstructure signals and horizon spread signals conflict (e.g., GEX positive/stabilizing but horizon spread inverting toward crisis), which signal should take precedence in the strategy debate?

**Relevant vault concepts**: [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md), [Regime Detection](../concepts/regime-detection.md), [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md), [Agent Role Specialization](../concepts/agent-role-specialization-in-llm-systems.md)

**Relevant research**: [GEX Scanner Logic Flow](gex-scanner-logic-flow.md), [Optimizing Greek Calculations with Ray](optimizing-greek-calculations-with-ray.md), [Synthesis 2026-05-17](synthesis-2026-05-17.md) (Cluster 2)

**Relevant gap**: [option-implied-erp-horizon-spread.md](gap-analysis-2026-05-17.md) concept note not yet created (Gap 1.3)

---

## Q6: What is the appropriate portfolio scope for MAOPM Phase 1?

**Why it matters**: The system could manage a single underlying (e.g., SPY) or a multi-symbol portfolio. Complexity, data requirements, and Greek netting all scale with the number of underlyings.

**Structural constraint**: The vault's [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md) documents four strategies — Fragility Short, Dispersion Trade, Gamma Flip Mean Reversion, and Term Structure Catch-Up — all of which require per-constituent GEX data (individual stock gamma exposure). A single-SPY MAOPM cannot execute any of these strategies even when the RDR explicitly signals the opportunity (e.g., RDR < 0.5 → dispersion regime). Limiting Phase 1 to SPY-only forecloses the primary GEX-divergence strategy set. This argues for at least a constituent overlay (Mag 7 or S&P 100 subset) alongside the index position from Phase 1 onward.

**Sub-questions**:
- Should Phase 1 focus on a single liquid ETF (SPY, QQQ) or a basket of 5–10 individual stocks (similar to TradingAgents' AAPL/GOOGL/AMZN/NVDA/META)?
- How does the multi-symbol case change the Portfolio Manager's Greek management challenge? (Net Greeks across different underlyings require correlation assumptions)
- Is the [Magnificent 7](../entities/magnificent-7-stocks.md) basket a natural starting universe given existing vault coverage?

**Relevant vault concepts**: [Multi-Agent LLM Financial Trading](../concepts/multi-agent-llm-financial-trading.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md)

---

## Q7: How should the system handle position management vs. new position initiation?

**Why it matters**: A live options portfolio requires continuous management decisions (roll, close early, adjust strikes) in addition to new position decisions. These are fundamentally different tasks — management is reactive (existing positions approaching risk limits or DTE thresholds); initiation is proactive (deploying capital per strategy signal). The vault's [Expiration Management](../concepts/expiration-management.md) note documents time-critical requirements — 21 DTE forced-close rule, pin risk monitoring at 3:00 PM ET on expiration day, assignment risk escalation when |delta| > 0.70 — that are **incompatible with a standard analysis-cycle cadence**. These are not periodic events; they are triggered events requiring sub-minute response at certain DTE thresholds. A slow LLM debate loop cannot handle them. This pushes a fast-path management agent into Phase 2, not Phase 3 as currently planned.

**Status**: ~50% answered. Sub-questions 1 and 2 resolved by existing schema and concept note design. Sub-questions 3 and 4 remain open.

**Sub-questions**:
- ✅ Should management decisions use the same debate loop or a separate deterministic fast path? → Separate fast path. The `requires_fast_path` boolean in the [Greek Exposure Report Schema](../entities/greek-exposure-report-json-schema.md) `management_flags` block flags time-critical positions; when set, the rules engine executes directly without an LLM debate loop.
- ✅ What triggers a management review cycle vs. the standard analysis cycle? → Thresholds established in [Expiration Management](../concepts/expiration-management.md) and formalized as `management_flags` schema fields: `dte_alert` (DTE ≤ 21), `delta_escalation` (|delta| > 0.20 at DTE < 14), `pin_risk_active` → forced close (underlying within 0.5% of short strike at 3:00 PM ET on expiration day).
- How should the unified alert queue (merging the expiration management calendar and the event-driven options risk calendar) be implemented to avoid duplicate or conflicting alerts on the same position?
- How should the system prioritize management actions over new position initiation when capital is constrained?

**Relevant vault concepts**: [Expiration Management](../concepts/expiration-management.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Event-Driven Options Risk](../concepts/event-driven-options-risk.md)

**Relevant gap**: Gap 3.4 in [gap-analysis-2026-05-17](gap-analysis-2026-05-17.md) — event calendar and expiration calendar not yet integrated

---

## Q8: Can TradingAgents-style performance claims be replicated and exceeded in options?

**Why it matters**: [TradingAgents](../entities/tradingagents-framework.md) demonstrated 23–26.62% cumulative returns vs. 7.78% buy-and-hold over Q1 2024 (Sharpe 5.60–8.21 vs. 2.31–3.53 for baselines). Options strategies have different return and risk characteristics — the comparison baseline must be options-native (mechanical iron condors, systematic covered calls, VIX-regime switching).

**Status**: Not answered. Prerequisite gap identified: all three referenced vault files are equity-centric. `algorithmic-trading-strategies-baselines.md` covers MACD, SMA, Buy & Hold, ZMR, KDJ/RSI only. `financial-trading-evaluation-metrics.md` and `financial-trading-performance-metrics.md` cover CR, AR, Sharpe, MDD only. No options-native baselines (mechanical iron condors, XYLD, Tastytrade-style CSPs) and no options-specific performance metrics (theta-adjusted return, PoP vs. realized profit rate, IV premium capture rate) exist in the vault. These must be documented before Q8 is tractable. Phase 4 deferral is appropriate.

**Sub-questions**:
- What are the appropriate baseline options strategies for comparison? (Mechanical weekly iron condors on SPY? Tastytrade-style 45-DTE CSPs? Covered call ETFs like XYLD?)
- What Sharpe ratio is achievable with a well-implemented systematic short-vol strategy (no LLM)? Is the multi-agent overhead justified by the improvement?
- Over what time horizon and market conditions does LLM-driven strategy adaptation add the most value? (High-vol regimes? Regime transitions?)

**Relevant vault concepts**: [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md), [Algorithmic Trading Strategies Baselines](../concepts/algorithmic-trading-strategies-baselines.md), [Traditional Trading Strategies](../concepts/traditional-trading-strategies.md)

---

---

## Q9: How does the option-implied horizon spread complement GEX-based regime detection in the MAOPM architecture?

**Why it matters**: Wan Ni Lai (2022) demonstrates that the horizon spread — the difference between the option-implied equity risk premium at 180-day and 30-day horizons — achieves only 4.6% probability mass in the "indecisive" zone (0.1–0.9 posterior probability) vs. 34% for GARCH volatility and 16% for historical returns. It detected COVID-19 in December 2019 while returns and volatility only signaled in March 2020. This makes it a materially superior leading indicator for macro regime shifts. The GEX Z-score and Regime Divergence Ratio capture dealer microstructure (days-to-weeks horizon). The horizon spread captures macro regime transitions (weeks-to-months horizon). These are complementary, not competing, signals. How they are fused in the MAOPM agent architecture is unspecified.

**Status**: ~45% answered. Sub-question 2 resolved by Vol Surface Summary schema design. Sub-question 1 substantially answered (all four open gaps resolved by ThetaData documentation). Sub-questions 3, 4, and 5 remain open.

**Sub-questions**:
- 🟡 What is the minimum data infrastructure required to compute the horizon spread in near-real-time? — **Substantially answered** via [ThetaData subscription docs](https://docs.thetadata.us/Articles/Getting-Started/Subscriptions.html) and [`option_snapshot_greeks_second_order`](https://docs.thetadata.us/operations_python/option_snapshot_greeks_second_order.html):
  - **(a) Fixed expiry dates, not constant maturity**: The `expiration` parameter takes actual `YYYY-MM-DD` expiry dates or `*` for all chains. No constant-maturity interpolation is provided by ThetaData. To compute V_Q(30) and V_Q(180), the client must query the two expirations bracketing each target tenor and time-interpolate the BKM-integrated variance. The `thetadata.md` vault claim about "pre-filtered constant-maturity variance profiles" was incorrect and has been corrected.
  - **(b) Polling snapshot, not streaming**: `option_snapshot_greeks_second_order` is an on-demand REST endpoint — Greeks are not part of the streaming feed. Update cadence is determined by polling frequency (up to 8 req/sec on PRO tier). For a macro leading indicator like the horizon spread, polling every 5–15 minutes is architecturally sufficient.
  - **(c) Minimum tier: VALUE for raw quotes, PRO for pre-computed IV**: Real-time Quote snapshots (`option_snapshot_quote`) unlock at **VALUE tier** — sufficient for BKM integration since the formula operates directly on option prices (no IV solver needed). **PRO tier** adds real-time pre-computed `implied_vol` and 2nd-order Greeks per contract, eliminating client-side BSM numerical solving across hundreds of strikes per expiration chain.
  - **(d) V_Q(T) not pre-computed**: ThetaData returns per-contract `implied_vol`, bid, ask, and Greeks — never integrated model-independent variance. Full client-side pipeline: (1) snapshot the full chain for the two expirations bracketing 30d and 180d DTE; (2) compute OTM mid-prices; (3) apply BKM integration over the strike domain to get V_Q at each bracketing expiry; (4) time-interpolate to exactly 30d and 180d; (5) compute ΔIHS = ERP₁₈₀ − ERP₃₀.
- ✅ Should the horizon spread be computed by the Vol Analyst or a dedicated Regime Analyst? → Vol Analyst. The [Vol Surface Summary Schema](../entities/vol-surface-summary-json-schema.md) places `horizon_spread` as a code-computed field in the Volatility Analyst's report. It is delivered to downstream agents as a structured field — not a free-text interpretation.
- How should a horizon spread inversion (HS < 0, signaling short-term risk > long-term) affect the Long-Vol/Short-Vol Researcher debate — does it immediately shift the prior toward long-vol, or is it one input among several?
- What is the lag structure between horizon spread inversion and GEX regime transition? If horizon spread leads GEX by weeks, can MAOPM position early before GEX confirms?
- How do you handle the case where horizon spread signals a macro crisis regime while GEX/Regime Divergence Ratio still signals a coherent, stable microstructure regime?

**Relevant vault concepts**: [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md), [Regime Detection](../concepts/regime-detection.md), [Volatility Surface Dynamics](../concepts/volatility-surface-dynamics.md), [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md)

**Relevant source**: [Detecting Stock Market Regimes from Option Prices](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md)

**Relevant gap**: [option-implied-erp-horizon-spread.md](gap-analysis-2026-05-17.md) concept note needed (Gap 1.3); Lai source stub needs upgrade (Gap 3.2)

---

## Q10: Can TradingGPT's layered memory architecture improve MAOPM position management across DTE tiers?

**Why it matters**: [TradingGPT](../entities/tradinggpt.md) introduced short-term, medium-term, and long-term memory tiers specifically to overcome LLM context-window limits in multi-horizon trading tasks. The MAOPM manages positions across structurally distinct time horizons: 0DTE/intraday (extreme gamma, minute-by-minute delta hedging), 21–45 DTE (premium-selling core, periodic rolling decisions), and 90–180+ DTE LEAPS (structural, monthly reviews). These three horizons map precisely onto TradingGPT's three memory tiers. Without layered memory, a MAOPM agent reviewing a 0DTE hedge decision would need to carry full context about all 45-DTE positions and LEAPS simultaneously — context-window overflow or token cost explosion is the likely failure mode.

**Status**: ~25% answered. Sub-questions 3 and 4 resolved by the Recording Secretary / Decision Ledger architecture. Sub-questions 1, 2, and 5 remain open.

**Sub-questions**:
- What information belongs in each memory tier for MAOPM? (Short-term: intraday delta hedges, 0DTE alerts, breach events; Medium-term: open 21–45 DTE position Greeks, recent vol regime classifications, last debate outcomes; Long-term: structural regime state, LEAPS positions, performance history, strategy bias parameters)
- What is the eviction policy for each tier? (Short-term: rolling session window; Medium-term: position close or roll; Long-term: regime transition event)
- ✅ Does layered memory require persistent storage? → Yes. Established by the Recording Secretary / Decision Ledger design: the Decision Ledger (SQLite, append-only) is the authoritative persistent store for medium and long-term tier content across process restarts. See [Decision Ledger](../concepts/decision-ledger.md).
- ✅ Can layered memory be implemented as structured JSON rather than a vector embedding store? → Yes. Confirmed by Decision Ledger schema design: MAOPM data is numerical and structured; vector embeddings provide no advantage over structured JSON queries for Greeks, regime enums, and position state. See [Decision Ledger](../concepts/decision-ledger.md).
- How does the Portfolio Manager agent query cross-tier memory when making a position sizing decision that depends on both current Greeks (medium-term) and structural regime (long-term)?

**Relevant vault concepts**: [Expiration Management](../concepts/expiration-management.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md), [Multi-Agent Systems](../concepts/multi-agent-systems.md), [Zero Days to Expiration](../concepts/zero-days-to-expiration.md)

**Relevant entity**: [TradingGPT](../entities/tradinggpt.md) (source stub incomplete — see Gap 2.2 in [gap-analysis-2026-05-17](gap-analysis-2026-05-17.md))

---

## Q11: How should the Observer Track be designed to minimize overhead on the Agent State Track?

**Why it matters**: The Observer Track (Recording Secretary, Board Interface, Performance Observer) runs in parallel with every Track 1 cycle. If Seam A event emission introduces latency into the Track 1 critical path — particularly in EXECUTING, where sub-second order routing matters — the audit infrastructure becomes a liability. The design must keep Track 1 fully decoupled from Track 2's write performance.

**Status**: ~30% answered. The Recording Secretary architecture ([Recording Secretary Agent](../concepts/recording-secretary-agent.md)) establishes the Seam A event taxonomy and Seam B default content; all five operational design questions (sync/async, minimum event set, pre-computation timing, Performance Observer scheduling, Seam B budget) remain open.

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

**Status**: ~20% answered. The principle is established — the Decision Ledger is the authoritative rehydration source on restart (see [Recording Secretary Agent](../concepts/recording-secretary-agent.md)). The complete rehydration procedure, restart sequence ordering, IB TWS unavailability handling, and portfolio snapshot question remain open.

**Sub-questions**:
- What is the complete set of state that Track 1 needs at ANALYZING start after a process restart? (Candidate list: open positions + current Greeks from IB TWS; Active Directives from Decision Ledger; last regime classification from Decision Ledger; unresolved Greek breach events from Decision Ledger; last N cycle summaries from Decision Ledger.)
- Should MAOPM maintain a separate "portfolio snapshot" store (updated after every EXECUTING phase) distinct from the Decision Ledger, or can the portfolio state be fully reconstructed from the ledger's `fill` and `expiry-alert` entries?
- What is the restart sequence? Proposed order: (1) load Active Directives from ledger, (2) query IB TWS for live position state, (3) query IB TWS for current Greeks, (4) load last regime classification from ledger, (5) generate Seam B context block, (6) enter ANALYZING. Is this the correct order and are there dependencies? Note: Step 1 is confirmed — [Board Directive Protocol](../concepts/board-directive-protocol.md) specifies that `persistent` scope directives survive process restarts and are stored in the Decision Ledger with `status: active | expired | revoked`, making them fully reconstructable from the ledger on restart.
- How should MAOPM handle the case where IB TWS is unavailable on restart (e.g., outside market hours)? Should it enter a suspended state until market open or proceed with stale Greeks from the ledger?
- Does the Decision Ledger's SQLite recommendation (from [Decision Ledger](../concepts/decision-ledger.md)) support the concurrent read pattern needed during rehydration without locking?

**Relevant vault concepts**: [Decision Ledger](../concepts/decision-ledger.md), [Recording Secretary Agent](../concepts/recording-secretary-agent.md), [Board Directive Protocol](../concepts/board-directive-protocol.md), [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md)

**Relevant entity**: [Interactive Brokers API](../entities/interactive-brokers-api.md)

---

## Prioritization

| Question | Priority | Tractable Now? | Effort | Phase |
|---|---|---|---|---|
| ~~Q3 — Communication schemas~~ | ~~Critical~~ **Resolved** | ~~Yes~~ Done | ~~Medium~~ | ~~1~~ |
| **Q11 — Observer Track overhead and Seam A/B design** *(30% answered)* | **High** | Yes | Medium | **0** |
| **Q12 — State persistence and restart rehydration** *(20% answered)* | **High** | Yes | Medium | **0** |
| Q2 — Dynamic Greek limits + Regime Div. Ratio scaler *(85% answered)* | High | Yes | Medium | 2 |
| Q1 — LLM vs. rules-based split | High | Yes | Low–Medium | 1–2 |
| Q6 — Portfolio scope *(structural constraint: multi-symbol required for GEX divergence)* | Medium | Yes (decision, not research) | Low | 1 |
| Q7 — Management fast-path vs. initiation *(50% answered)* | **High** *(elevated)* | Yes | Medium | **2** |
| Q5 — Multi-signal regime fusion (GEX + horizon spread) *(35% answered)* | **High** *(elevated)* | Yes — Lai paper ingested | Medium | 2 |
| Q9 — Horizon spread in MAOPM architecture *(15% answered)* | High | Yes — Lai paper ingested | Medium | 2 |
| Q10 — TradingGPT layered memory → DTE tiers *(25% answered)* | Medium | Partial (source stub incomplete) | Medium | 2–3 |
| Q4 — Backtesting approach + historical GEX blocker | High | Partial (GEX data availability TBD) | High | 4 |
| Q8 — Performance baseline vs. options-native strategies *(vault has no options baselines)* | Low | No — prerequisite gap | High | 4 |

---
