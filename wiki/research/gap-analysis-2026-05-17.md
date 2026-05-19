---
tags: ["gap-analysis", "multi-agent-systems", "options-trading", "llm", "knowledge-graph"]
created: 2026-05-17
reviewed: false
source_origin: "level1-analysis"
---
# Gap Analysis: Personal Brain Vault — 2026-05-17

> Surgical identification of specific named gaps in the vault as of this date. For each gap: what is missing, where it is implicitly referenced, and why it matters for the [MAOPM initiative](current%20research%20initiatives.md). This supersedes [gap-analysis-2026-05-16](gap-analysis-2026-05-16.md), which reflects a pre-Lai-paper vault state.

---

## Section 1: Missing Concept Notes

Concepts that appear by reference in ≥2 vault files but have no dedicated concept note.

---

### Gap 1.1 — `options-pricing-models.md`
**Referenced in**: [Implied Volatility](../concepts/implied-volatility.md) (IV is "derived from market prices of options"); [Volatility Surfaces](../concepts/volatility-surfaces.md) (IV surface used for "option valuation"); [Options Risk Metrics](../concepts/options-risk-metrics.md) (PoP approximated as `1 - delta`); [Dispersion Trade Strategy](../concepts/dispersion-trade-strategy.md) (requires IV at index vs. component level)

**What is missing**: Black-Scholes-Merton model (assumptions, closed-form for Δ/Γ/ν/Θ, limitations), local vol (Dupire), stochastic vol (Heston, SABR). The vault uses IV extensively but never documents how IV is derived from market prices or why the model matters for Greek accuracy.

**Why it matters for MAOPM**: The Greeks Analyst agent receives per-contract Greeks from ThetaData. Knowing the pricing model behind those Greeks (Black-Scholes vs. model-free) is prerequisite to understanding their reliability — especially for far-OTM strikes where model choice diverges. Also prerequisite for understanding *implied correlation*, the core mechanism of the Dispersion Trade.

---

### Gap 1.2 — `implied-correlation.md`
**Referenced in**: [Dispersion Trade Strategy](../concepts/dispersion-trade-strategy.md) (sells index vol, buys component vol — this exploits a correlation premium); [GEX Divergence Strategies](../concepts/gex-divergence-strategies.md) (dispersion named as key strategy type)

**What is missing**: Implied correlation (the market's forward-looking estimate of average pairwise correlation among index constituents), the correlation premium (implied correlation systematically exceeds realized correlation — the profit source of dispersion trades), and the correlation skew.

**Why it matters for MAOPM**: Dispersion trades are in the strategy universe (Cluster 3 of the synthesis). Without a concept note on implied correlation, the rationale for the trade — and the specific risk (correlation convergence) — cannot be reasoned about by the Long-Vol/Short-Vol Researcher agents.

---

### Gap 1.3 — `option-implied-erp-horizon-spread.md`
**Referenced in**: [Detecting Stock Market Regimes from Option Prices (Lai, 2022)](../sources/detecting_stock_market_regimes_lai_2022.md); [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md) (cites option-implied metrics but does not name the horizon spread); [Stock Market Regimes](../concepts/Stock%20Market%20Regimes.md) (regime detection methods); [Regime Detection](../concepts/regime-detection.md) (market-implied methods listed)

**What is missing**: A dedicated concept note extracting Lai (2022)'s horizon spread metric: $HS_t = \text{ERP}_{180d,t} - \text{ERP}_{30d,t}$, estimated nonparametrically from put and call prices. Key facts to capture: (1) turns negative during crises (short-term risk premium exceeds long-term); (2) detected COVID-19 regime shift in Dec 2019, three months before GARCH or return-based models; (3) achieves 4.6% indecisive-zone probability vs. 34% for volatility-based detection.

**Why it matters for MAOPM**: The Vol Analyst role currently specifies IVR/IVP monitoring and vol surface shape. Horizon spread is strictly superior as a leading macro regime indicator. Without a concept note, it cannot be formally linked into the agent design or the Long-Vol/Short-Vol debate inputs. This is the single highest-value paper in the vault and it is currently orphaned from the agent architecture.

**Status**: The duplicate source stub has been removed. Canonical source is now [Detecting Stock Market Regimes from Option Prices (Lai, 2022)](../sources/detecting_stock_market_regimes_lai_2022.md). The raw asset at `raw/assets/Detecting stock market regimes from option prices.md` remains available.

---

### Gap 1.4 — `options-backtesting-methodology.md`
**Referenced in**: [Research Agenda Q4](research-agenda-options-maopm.md) (asks how to backtest with realistic fills); [current research initiatives](current%20research%20initiatives.md) ("backtesting with realistic bid/ask" listed in scope); [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md) (metrics defined for equities only)

**What is missing**: Options-specific backtesting challenges — path-dependency (options expire; equity close-price backtesting has no analog), IV surface reconstruction for historical dates, bid/ask spread simulation (mid? natural? improvement?), pin risk and assignment simulation at expiration, slippage modeling for multi-leg orders. Also missing: historical GEX data availability — ThetaData provides historical per-contract Greeks; 30-day rolling GEX Z-scores therefore require minimum 30 trading days of burn-in per symbol. This is a concrete data availability constraint that does not appear anywhere in the vault.

**Why it matters for MAOPM**: Q4 of the research agenda is a Phase 4 task but the methodology decisions (which provider, what simulation assumptions) need to be locked before the live system is designed, because they determine what data the system must log during paper trading.

---

### Gap 1.5 — `vol-crush-exploitation.md`
**Referenced in**: [Event-Driven Options Risk](../concepts/event-driven-options-risk.md) (vol crush described as a risk to long-vol holders and a trap); [Implied Volatility](../concepts/implied-volatility.md) ("vol crush" defined); [Options Strategies](../concepts/options-strategies.md) (short-vol strategies listed but not linked to event context)

**What is missing**: Systematic vol crush exploitation as a distinct strategy class — selling premium into pre-event IV expansion, targeting a specific expected-move multiple (e.g., sell when IV implies >1.5× the stock's average post-earnings move), and closing positions the morning after the event. Risk parameters (naked vs. spread, position sizing for gap risk), execution constraints (must open before close of trading day before event), and historical performance vs. standard short-vol are not documented.

**Why it matters for MAOPM**: The event calendar ([Event-Driven Options Risk](../concepts/event-driven-options-risk.md)) is already integrated into the architecture for *risk avoidance*. Vol crush exploitation uses the same calendar for *opportunistic positioning*. Without the concept note, the Short-Vol Researcher has no formalized rationale for recommending event-based premium selling.

---

### Gap 1.6 — `llm-model-routing.md`
**Referenced in**: [TradingAgents Framework](../entities/tradingagents-framework.md) (gpt-4o-mini for retrieval, o1-preview for deep reasoning); [current research initiatives](current%20research%20initiatives.md) (gpt-4o-mini quick tasks, o1/o3 deep reasoning, specialist models for sentiment); [Agent Role Specialization](../concepts/agent-role-specialization-in-llm-systems.md) (specialized roles implied to use different LLMs)

**What is missing**: A systematic framework mapping task type → LLM class. The implicit rule is: structured data retrieval / report generation → smaller/faster model; dialectical debate / multi-step reasoning with uncertainty → larger/slower reasoning model. This tradeoff needs to be explicit: latency, cost, and quality interact differently per task. For MAOPM specifically — does the Greek exposure report generation need o1, or is gpt-4o-mini sufficient? Does the Long-Vol/Short-Vol debate need o3, or does gpt-4o achieve comparable argument quality?

**Why it matters for MAOPM**: LLM API cost scales with call count × model size × token volume. TradingAgents makes 11+ LLM calls + 20+ tool calls per trading cycle. MAOPM's multi-signal, multi-agent loop will exceed this. Without a routing framework, inference cost is uncontrolled.

---

### Gap 1.7 — `agent-state-synchronization.md`
**Referenced in**: [TradingAgents Framework](../entities/tradingagents-framework.md) ("global agent state" mentioned but not detailed); [Structured Communication Protocol](../concepts/structured-communication-protocol.md) (structured documents passed between agents); [current research initiatives](current%20research%20initiatives.md) (structured JSON schemas specified but storage mechanism not named)

**What is missing**: The mechanics of shared state in multi-agent systems — in-memory dict, message broker (Redis/RabbitMQ), structured document store, or per-agent context passing. In TradingAgents, the global state appears to be an in-memory dictionary. For MAOPM, which runs on a continuous monitoring loop with an interrupt path, in-memory state fails on process restart. Options portfolio state (open positions, current Greeks, last vol regime classification) must be persistent.

**Why it matters for MAOPM**: State persistence is an implementation prerequisite for M1 (Foundation milestone) but is not mentioned in any architecture note.

---

### Gap 1.8 — Options-Native Performance Baselines (concept)
**Referenced in**: [Research Agenda Q8](research-agenda-options-maopm.md) (asks for comparison baselines); [Financial Trading Evaluation Metrics](../concepts/financial-trading-evaluation-metrics.md) (equity metrics only); [Algorithmic Trading Strategies Baselines](../concepts/algorithmic-trading-strategies-baselines.md) (equity baselines only: B&H, MACD, SMA, KDJ+RSI, ZMR)

**What is missing**: A concept note on options-native baseline strategies — mechanical weekly iron condors on SPY (Tastytrade-style, 45 DTE, roll at 21 DTE), systematic cash-secured puts (45 DTE, IVR > 50), covered-call ETF replication (XYLD methodology), VIX-regime switching (sell SPY straddles when VIX > 20, hold cash when VIX < 15). These are the correct comparison class for MAOPM's performance claims.

---

## Section 2: Entity Stubs / Placeholders

### Gap 2.1 — `gex-divergence-dashboard.md` (entity file empty)
**Status**: Entity file exists at `wiki/entities/gex-divergence-dashboard.md`. Content: empty (zero bytes of substantive content).

**What is needed**: Visualization tool specification — what metrics it displays (GEX Z-score heatmap per stock, Internal GEX Index time series, Regime Divergence Ratio), technology stack (Plotly/Dash? Streamlit? Node.js?), refresh cadence, alert thresholds that feed the MAOPM interrupt path. The [GEX Scanner Logic Flow](gex-scanner-logic-flow.md) documents the computation but not the display layer.

**Cross-ref needed**: Should link to [Optimizing Greek Calculations with Ray](optimizing-greek-calculations-with-ray.md), [GEX Scanner Logic Flow](gex-scanner-logic-flow.md), [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md).

---

### Gap 2.2 — `arxiv-2309.03736-tradinggpt.md` (source stub)
**Status**: Source file at `wiki/sources/arxiv-2309.03736-tradinggpt.md` is a stub. No quantitative results, no memory tier implementation details, no experimental setup.

**What is needed**: Full paper review — (1) performance results vs. baselines; (2) concrete memory tier specification (what goes in short-term vs. medium-term vs. long-term memory, and by what eviction policy?); (3) how distinct character personas affect debate outcomes. The layered memory architecture has a direct structural mapping to DTE tier management (see [synthesis note](synthesis-2026-05-17.md)) that cannot be formalized without the implementation details.

---

## Section 3: Structural / Connectivity Issues

### Gap 3.1 — `Master Concept Map.md` is empty
**File**: `wiki/concepts/Master Concept Map.md` — zero substantive content.

**Why it matters**: Referenced in `index.md` as a primary navigation entry point. Currently a dead link. Should be rebuilt as a structured overview of the five conceptual clusters from [synthesis-2026-05-17](synthesis-2026-05-17.md) once that note stabilizes.

---

### Gap 3.2 — Lai (2022) paper orphaned from wiki graph
**Full paper**: `raw/assets/Detecting stock market regimes from option prices.md` — complete, high-quality content (HMM methodology, quantitative results, COVID detection evidence).

**Canonical wiki source**: [Detecting Stock Market Regimes from Option Prices (Lai, 2022)](../sources/detecting_stock_market_regimes_lai_2022.md) — duplicate stub removed; this is now the single source-of-truth in the wiki.

**Remaining fix required**: (1) Create the horizon spread concept note (Gap 1.3); (2) link from [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md) and [Regime Detection](../concepts/regime-detection.md).

---

### Gap 3.3 — Near-duplicate concept pairs
Two pairs of concept files with substantially overlapping content that inflate coverage appearance:

| Pair | Overlap | Recommended action |
|---|---|---|
| `llms-in-finance.md` vs. `llms-in-financial-trading.md` | Both cover LLM-as-trader, LLM-as-alpha-miner; near-identical structure | Merge into `llms-in-finance.md`; redirect references |
| `financial-trading-performance-metrics.md` vs. `financial-trading-evaluation-metrics.md` | Identical metric definitions (CR, AR, Sharpe, MDD); same formulas | Merge; the evaluation version has slightly more detail; keep it |

---

### Gap 3.4 — Cross-cluster disconnections (missing links)

The following concept-to-concept relationships exist logically but have no explicit link in either file:

| From | To | Missing connection |
|---|---|---|
| [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md) | [Portfolio Greeks Management](../concepts/portfolio-greeks-management.md) | Ratio's coherent/divergent band should directly scale the Greek limits defined there |
| [TradingGPT](../entities/tradinggpt.md) | [Expiration Management](../concepts/expiration-management.md) | Layered memory tiers map to 0DTE/21–45DTE/LEAPS DTE tiers |
| [Event-Driven Options Risk](../concepts/event-driven-options-risk.md) | [Expiration Management](../concepts/expiration-management.md) | Both maintain event/expiration calendars feeding the same MAOPM alert queue |
| [Detecting Stock Market Regimes](../sources/Detecting%20stock%20market%20regimes%20from%20option%20prices.md) source | [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md) | Primary empirical grounding for option-implied regime detection; should be the source reference |
| [GEX Scanner Logic Flow](gex-scanner-logic-flow.md) | [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md) | Scanner computes GEX Z-scores per stock; ratio uses aggregate GEX — these are sequential steps in same pipeline |

---

## Section 4: Source Diversity

The vault currently has 3 source notes covering 2 unique papers (TradingAgents, TradingGPT stub) + 1 methodology paper (Lai 2022). The following cited works have no source notes:

| Work | Cited in | Priority |
|---|---|---|
| FinMem (memory-augmented LLM trader) | [LLMs in Finance](../concepts/llms-in-finance.md) | Medium |
| FinAgent (multimodal LLM agent) | [LLMs in Finance](../concepts/llms-in-finance.md) | Medium |
| QuantAgent / AlphaGPT (alpha mining) | [LLMs in Finance](../concepts/llms-in-finance.md) | Low |
| ReAct original paper (arXiv:2210.03629) | [ReAct Prompting Framework](../concepts/react-prompting-framework.md), source stub exists | Complete the stub |
| Tastytrade research on 45-DTE premium selling | [Options Strategies](../concepts/options-strategies.md) (implied) | High (for backtesting baselines) |
| HMM literature (Baum-Welch, regime modeling) | [Regime Detection](../concepts/regime-detection.md), [Lai 2022] | Medium |

---

## Ingestion Priority Order

| Priority | Item | Type |
|---|---|---|
| **P1** | `option-implied-erp-horizon-spread.md` | New concept (extract from Lai 2022) |
| **P1** | Upgrade Lai (2022) source stub to full note | Source note update |
| **P2** | `implied-correlation.md` | New concept |
| **P2** | `options-pricing-models.md` | New concept |
| **P2** | `gex-divergence-dashboard.md` entity content | Entity update |
| **P2** | Complete TradingGPT source stub | Source note update |
| **P3** | `options-backtesting-methodology.md` | New concept |
| **P3** | `vol-crush-exploitation.md` | New concept |
| **P3** | `llm-model-routing.md` | New concept |
| **P3** | `agent-state-synchronization.md` | New concept |
| **P3** | Options-native baselines concept | New concept |
| **P4** | Merge near-duplicate concept pairs | Refactor |
| **P4** | Add missing cross-links (Gap 3.4 table) | Link additions |
| **P4** | Populate `Master Concept Map.md` | Navigation update |
