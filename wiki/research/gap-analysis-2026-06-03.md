---
tags: ["gap-analysis", "knowledge-graph", "thetadata-api", "options-trading", "art-digital-culture", "naming-conventions"]
created: 2026-06-03
reviewed: false
source_origin: "level1-analysis"
---
# Gap Analysis: Personal Brain Vault — 2026-06-03

> Surgical identification of specific named gaps as of June 3, 2026. This analysis supersedes the ThetaData API portions of previous gap notes and adds three new gap categories not previously tracked: the ThetaData API reference-layer collapse, the art/digital culture cluster isolation, and the `tradingagents.md` naming mismatch. MAOPM tool-spec gaps from [gap-analysis-2026-05-20](gap-analysis-2026-05-20.md) that remain open are carried forward as Section 5 with status updates.

---

## Section 1: ThetaData API — Core Reference Notes Missing (153 Broken Links)

The ThetaData v3 API has been heavily documented at the endpoint level — approximately 80 endpoint notes exist across flat `concepts/` and `concepts/theta-data-v3-api/endpoints/`. However, the **cross-cutting reference concepts** that every endpoint cites are absent. This creates a structural collapse: each endpoint note has multiple broken "See also" links to shared concept files that do not exist.

---

### Gap 1.A — `concepts/symbols.md` (45 broken links)

**Referenced in**: Every ThetaData v3 option, stock, and index endpoint note. Appears as `[Symbols](../../concepts/symbols.md)` or `[Symbols](../concepts/symbols.md)` in parameter tables for the `symbol` field across all ~45 endpoint notes.

**What is missing**: A concept note defining the ThetaData symbol format — ticker string conventions (uppercase, root symbol only), the `*` wildcard behavior for bulk queries, the `opt_multi_symbol` vs. single-symbol distinction, and how ThetaData symbols differ from OCC symbology. The companion note [api-symbology-tastytrade.md](../concepts/api-symbology-tastytrade.md) covers Tastytrade's format; the equivalent for ThetaData does not exist.

**Impact**: The 45 endpoint notes are collectively the most-linked content in the vault. Their shared "See [Symbols]" reference is the single most broken link pattern, affecting every future reader navigating API documentation.

---

### Gap 1.B — `concepts/strike-prices.md` (31 broken links)

**Referenced in**: Every ThetaData v3 option endpoint with a `strike` parameter — option history (OHLC, Greeks, trades, quotes), option snapshot (Greeks, market value), option at-time (quote, trade), option list endpoints.

**What is missing**: Strike price representation in ThetaData's format (integer in thousandths of a dollar — e.g., `250000` = $250.00), valid strike step sizes, behavior when the requested strike doesn't exist, and the relationship to the `expiration` parameter for locating a specific contract. Without this, the `strike` parameter across 31 endpoint notes has no reference document and the format is undiscoverable from the vault alone.

**Impact**: Any developer using these endpoint notes to write code will silently use the wrong strike format. The `option-list-strikes-endpoint.md` note exists but does not define the representation standard.

---

### Gap 1.C — `concepts/time-intervals.md` (25 broken links)

**Referenced in**: All ThetaData history endpoints with an `interval` parameter — option-history-ohlc, option-history-quote, option-history-trade, option-history-greeks-*, stock-history-ohlc, stock-history-quote, index-history-ohlc, and related.

**What is missing**: The supported interval types (`100` for 100ms, `1000` for 1s, `60000` for 1m, etc.), the distinction between tick-level and bar-aggregation intervals, which intervals are available at which subscription tiers, and the relationship between interval granularity and data latency. The existing [api-parameters.md](../concepts/api-parameters.md) has an `#interval` anchor referenced alongside this note but the two are designed to be complementary — `api-parameters.md` gives the parameter syntax; `time-intervals.md` gives the valid values.

**Impact**: 25 endpoint notes reference a document that does not exist. Without it, the `interval` parameter is an opaque integer with no defined vocabulary.

---

### Gap 1.D — `concepts/trade-conditions.md` and `concepts/quote-conditions.md` (8 broken links each)

**Referenced in**: `option-at-time-trade-endpoint.md`, `option-at-time-quote-endpoint.md`, `index-history-eod-endpoint.md`, and related endpoints that return `condition` fields in their response schemas.

**What is missing**: Exchange condition codes — the numeric or string codes appended to trade and quote records by exchanges to indicate special circumstances (e.g., out-of-sequence, form-T, intermarket sweep). Both notes are linked as "See also" from endpoint response field tables. Without them, the `condition` field in any endpoint response is uninterpretable.

**Impact**: Smaller than Gaps 1.A–1.C but affects correctness: a strategy filtering on "clean" trades will misread condition-coded records without this reference.

---

### Gap 1.E — `concepts/subscription-tiers.md` (6 broken links)

**Referenced in**: [index-data.md](../concepts/index-data.md) ("often used for higher [Subscription Tiers]") and [data-feeds.md](../concepts/data-feeds.md) ("for real-time stock snapshot data in Theta Data v3 for higher [Subscription Tiers]").

**What is missing**: The ThetaData VALUE / SMART / HIST subscription tier distinctions — which endpoints require each tier, which data products (real-time snapshots vs. historical OHLC) are gated behind higher tiers, and the cost differential. This is operationally critical: the HMM feature vector for Tool 4 requires intraday Greeks data, which is subscription-tier-gated.

---

### Gap 1.F — `concepts/stock-data.md` (3 broken links)

**Referenced in**: [theta-data-v3.md](../entities/theta-data-v3.md) ("See [Stock Data](../concepts/stock-data.md)"), [utp-cta-feeds.md](../entities/utp-cta-feeds.md), [nasdaq-basic.md](../entities/nasdaq-basic.md).

**What is missing**: An overview concept note for ThetaData stock data — analogous to the existing [option-data.md](../concepts/option-data.md) and [index-data.md](../concepts/index-data.md) — that enumerates the stock history and snapshot endpoints, their return types, and the data sources (UTP/CTA feeds).

---

### Gap 1.G — Missing snapshot endpoint notes (2–3 broken links each)

Four option snapshot endpoint notes exist in `theta-data-v3-api/endpoints/` under shorter filenames but are being linked from concept notes using the `-endpoint` suffix convention used in flat `concepts/`:

| Links expect (missing) | File that exists (different path/name) |
|---|---|
| `concepts/option-snapshot-ohlc-endpoint.md` | `concepts/theta-data-v3-api/endpoints/option-snapshot-ohlc.md` |
| `concepts/option-snapshot-trade-endpoint.md` | `concepts/theta-data-v3-api/endpoints/option-snapshot-trade.md` |
| `concepts/option-snapshot-quote-endpoint.md` | `concepts/theta-data-v3-api/endpoints/option-snapshot-quote.md` |
| `concepts/option-snapshot-open-interest-endpoint.md` | `concepts/theta-data-v3-api/endpoints/option-snapshot-open-interest.md` |
| `concepts/stock-history-quote-endpoint.md` | `concepts/theta-data-v3-api/endpoints/stock-history-quote.md` |
| `concepts/stock-history-trade-endpoint.md` | `concepts/theta-data-v3-api/endpoints/stock-history-trade.md` |

**Resolution**: Either add redirect stubs at the expected flat-concepts paths, or update the 10 inbound links to point to the correct subdirectory paths. Creating stubs is safer and preserves the link graph; updating 10 links risks diverging from the flat-concepts convention used across 80+ endpoint notes.

---

## Section 2: Entity Naming Mismatch — `tradingagents.md` (29 broken links)

**Location of mismatch**: 14 concept notes link to `../entities/tradingagents.md`. The actual entity file is `wiki/entities/tradingagents-framework.md`.

**Affected files**:
- `financial-trading-evaluation-metrics.md`, `financial-trading-firm-structure.md`, `fund-manager-agent.md`, `fundamental-analyst-agent.md`, `llms-in-finance.md`, `news-analyst-agent.md`, `react-prompting-framework.md`, `researcher-agent.md`, `risk-management-team-agent.md`, `sentiment-analyst-agent.md`, `structured-communication-protocol.md`, `technical-analyst-agent.md`, `trader-agent.md`, `traditional-trading-strategies.md`

**What is missing**: This is not a missing concept — the content exists in `tradingagents-framework.md`. The gap is a systematic naming mismatch in 29 link instances across 14 files. A reader following any of these links gets a broken reference to the most central entity in the MAOPM research cluster.

**Resolution options**: (a) Rename `tradingagents-framework.md` to `tradingagents.md` and update the 2 inbound links that already correctly use `tradingagents-framework.md` naming, or (b) create a stub `tradingagents.md` that redirects. Option (a) is cleaner; only [Current Research Initiatives](Current%20Research%20Initiatives.md) and [synthesis-2026-05-17](synthesis-2026-05-17.md) use the framework name.

---

## Section 3: Art/Digital Culture Cluster — Zero Research Output

Since the May 20 gap analysis, a substantial second thematic cluster has grown in the vault — Southeast Asian contemporary art, Singapore's digital nation-building, and media archaeology — with no research output connecting it.

**Ingested concepts** (13 notes, all self-contained):
[contemporary-art-singapore.md](../concepts/contemporary-art-singapore.md), [contemporary-southeast-asian-art-after-1990.md](../concepts/contemporary-southeast-asian-art-after-1990.md), [cyberarts.md](../concepts/cyberarts.md), [internet-art.md](../concepts/internet-art.md), [media-archaeology.md](../concepts/media-archaeology.md), [modernism-in-art.md](../concepts/modernism-in-art.md), [new-media-art.md](../concepts/new-media-art.md), [strategic-amnesia-digital-culture.md](../concepts/strategic-amnesia-digital-culture.md), [reworlding-art-history.md](../concepts/reworlding-art-history.md), [intelligent-island.md](../concepts/intelligent-island.md), [it2000-masterplan.md](../concepts/it2000-masterplan.md), [singapore-one.md](../concepts/singapore-one.md), [smart-nation.md](../concepts/smart-nation.md)

**Ingested entities** (~25 art-world figures and institutions including [lin-hsin-hsin.md](../entities/lin-hsin-hsin.md), [michelle-antoinette.md](../entities/michelle-antoinette.md), [gunalan-nadarajan.md](../entities/gunalan-nadarajan.md), [tsunamiinet.md](../entities/tsunamiinet.md), [cyberarts-exhibition-2001.md](../entities/cyberarts-exhibition-2001.md), [documenta11.md](../entities/documenta11.md), [kiasma-nykytaiteen-museo.md](../entities/kiasma-nykytaiteen-museo.md))

**Ingested sources** (8 academic works including [antoinette-2014-reworlding-art-history.md](../sources/antoinette-2014-reworlding-art-history.md), [yamin-mitchell-excavating-amnesia-2023.md](../sources/yamin-mitchell-excavating-amnesia-2023.md), [southeast-of-now-journal.md](../sources/southeast-of-now-journal.md), [third-text-journal.md](../sources/third-text-journal.md), [routledge-encyclopedia-of-modernism.md](../sources/routledge-encyclopedia-of-modernism.md))

### Gap 3.A — No synthesis note for the art cluster

The cluster's internal logic is not documented anywhere. The thematic through-line — how Singapore's state-driven digitization programs (IT2000 Masterplan → Singapore ONE → CyberArts → Smart Nation) shaped the conditions for digital and net art practice among Southeast Asian artists — is visible across the concept notes individually but never made explicit. The relationship between state policy and artistic counter-response (e.g., the CyberArts exhibition as state endorsement of digital art vs. the strategic-amnesia critique of the same digital culture) is the kind of non-obvious connection Level 1 analysis is designed to surface.

### Gap 3.B — No research agenda for the art cluster

The vault's art sources span art history, postcolonial theory, and media studies. There is no research agenda specifying what questions these sources make tractable. Example unanswered questions visible from the material: How does Antoinette's "reworlding" methodology differ from Piyadasa and Sulaiman's "rethinking" project? What is the relationship between Galloway's [black box theory](../concepts/black-box-galloway.md) and the opacity of Singapore's IT2000 policy planning? Does the CyberArts exhibition represent genuinely local digital art practice or a curated internationalist aesthetic?

### Gap 3.C — Cross-cluster isolation

The art cluster has zero inbound links from any research note, and the MAOPM/options cluster has zero links to art concepts. Whether this isolation is intentional (two independent research tracks) or an artifact of separate ingestion sessions is undocumented. At minimum, a brief note in [Current Research Initiatives](Current%20Research%20Initiatives.md) should register the art cluster as a named second initiative with its own scope statement.

---

## Section 4: Naming Convention Violations — 29 Snake_case Files in concepts/

The convention violation first flagged in [gap-analysis-2026-05-20](gap-analysis-2026-05-20.md) (Section 3) has not been remediated and has expanded. There are now 29 snake_case files in `concepts/` (up from ~8 identified in May):

```
aic_bic_information_criteria.md      conditional_value_at_risk.md
data_leakage_in_backtesting.md       delta_hedging.md
equity_risk_premium.md               gamma_exposure_gex.md
hidden_markov_model.md               horizon_spread_financial.md
implied_volatility.md                intraday_gex_schedule.md
liquidity_modeling_in_options.md     local_cache_layer.md
option_implied_equity_risk_premium.md   option_overlays.md
options_portfolio_optimization.md    overfitting_in_quantitative_models.md
process_based_parallelism.md         realized_volatility.md
regime_switching_models.md           risk_neutral_variance.md
root_mean_square_forecast_error.md   selection_bias_in_quantitative_models.md
stochastic_volatility_models.md      stock_market_regimes.md
systematic_options_strategies.md     tail_risk_modeling.md
transaction_costs_in_options.md      vectorized_greek_calculation.md
volatility_risk_premium.md
```

**Gap 4.A — Content-duplicate pairs within the violations**: Several of these coexist with properly-named kebab-case files containing overlapping or identical content:

| Snake_case (violation) | Kebab-case (authoritative) |
|---|---|
| `aic_bic_information_criteria.md` | No kebab-case equivalent; content unique but naming wrong |
| `gamma_exposure_gex.md` | `gamma-exposure-gex.md` + `gex.md` + `gamma-exposure.md` (4 GEX entries total) |
| `hidden_markov_model.md` | `hidden-markov-model.md` (direct duplicate at different path) |
| `implied_volatility.md` | `implied-volatility.md` |
| `realized_volatility.md` | `realized-volatility.md` |
| `volatility_risk_premium.md` | `volatility-risk-premium-vrp.md` + `volatility-risk-premium.md` |
| `stock_market_regimes.md` | `market-regimes.md` (possibly) |

**Specific note**: `aic_bic_information_criteria.md` was created to resolve Gap 1.D from the May 20 analysis, but was named with underscores. The gap is substantively closed (the content exists) but the naming violation means any notes linking to `aic-bic-model-selection.md` (the name used in the May 20 gap description) or `aic_bic_information_criteria.md` will have mismatched paths.

---

## Section 5: Carried Open Gaps from May 20 (Status Updates)

### Gap 1.A (May 20) — `baum-welch-algorithm.md`
**Status: CLOSED** ✓ — File exists at [baum-welch-algorithm.md](../concepts/baum-welch-algorithm.md).

### Gap 1.B (May 20) — `parkinson-volatility-estimator.md`
**Status: CLOSED** ✓ — File exists at [parkinson-volatility-estimator.md](../concepts/parkinson-volatility-estimator.md).

### Gap 1.C (May 20) — Tool 3 `hmm-latent-regime-engine-implementation.md`
**Status: PARTIALLY OPEN** — The architecture has evolved: Tool 4 (Near-Expiry HMM for 7DTE→1DTE) is now the primary MVP tool and has a concept note ([near-expiry-hmm-options-dynamics.md](../concepts/near-expiry-hmm-options-dynamics.md)) and tooling spec entry. Tool 3 (Macro HMM Latent Regime Engine) is documented in [tooling-requirements-maopm.md](tooling-requirements-maopm.md) with a build spec, but the concept note for the macro HMM architecture (the nightly Baum-Welch refit on 252-day rolling window, forward-pass inference at 5-min cadence, AIC/BIC K-selection monthly) remains absent from `concepts/`. The tooling document is the only location for this specification.

### Gap 1.D (May 20) — `aic-bic-model-selection.md`
**Status: CLOSED (content) / OPEN (naming)** — Content exists in `aic_bic_information_criteria.md` but violates kebab-case convention (see Section 4 above).

### Gap 1.E (May 20) — `option-implied-erp-horizon-spread.md`
**Status: OPEN** — `option-implied-horizon-spread.md` exists as a general concept but still does not capture the specific Lai (2022) two-maturity-differential structure, regime detection performance statistics (4.6% vs. 34% indecisive-zone rate), or its role as an HMM emission input. The MAOPM feature vector depends on `horizon_spread_delta = ERP_180 − ERP_30` but no concept note documents how this is computed from option prices using BKM variance.

### Gap 2.A (May 20) — Broken link from HMM research note to `how-to-obtain-hmm-estimates-from-option-prices.md`
**Status: OPEN** — Still not linked.

### Gap 2.B (May 20) — `hidden-markov-models-for-options-trading.md` not linked to MAOPM notes
**Status: OPEN** — The strategy-selection logic for the three-state regime table remains unconnected to the MAOPM architecture.

### Gap 2.C (May 20) — Broken links in `usefulness-of-hidden-markov-models-for-short-dated-options-trading.md`
**Status: OPEN** — Still contains dead links to non-existent `options-trading.md` and `hidden-markov-models.md`.

### Gap 2.D (May 20) — `hidden-markov-model-hmm.md` redundancy
**Status: OPEN** — Redundant file remains.

### Gap 4.A (May 20) — Tool 3 not in tooling-requirements-maopm.md
**Status: CLOSED** — [tooling-requirements-maopm.md](tooling-requirements-maopm.md) now includes Tool 3 (Macro HMM) and Tool 4 (Near-Expiry HMM) with build specifications and output schemas.

### `tradingagents-analyst-team.md` (flagged in sentiment-analyst, news-analyst notes)
**Status: OPEN** — Still explicitly called out in two agent concept notes as "Implicit concept, could be created if needed." It has never been created. The TradingAgents Analyst Team structure (Fundamental, Sentiment, News, Technical analysts operating in parallel) is documented in those individual agent notes but has no aggregating concept note.

---

## Priority Ranking

| Priority | Gap | Action | Broken Links |
|---|---|---|---|
| 1 | Gap 1.A: `symbols.md` | Create concept note | 45 |
| 2 | Gap 2 (Section 2): `tradingagents.md` mismatch | Rename entity or create stub | 29 |
| 3 | Gap 1.B: `strike-prices.md` | Create concept note | 31 |
| 4 | Gap 1.C: `time-intervals.md` | Create concept note | 25 |
| 5 | Gap 1.D+F: `trade-conditions.md`, `quote-conditions.md` | Create two concept notes | 16 |
| 6 | Gap 1.E: `subscription-tiers.md` | Create concept note | 6 |
| 7 | Gap 1.F: `stock-data.md` | Create concept note | 3 |
| 8 | Gap 3.A: Art cluster synthesis | Create `synthesis-art-digital-culture-2026-06-03.md` | 0 (no links yet) |
| 9 | Gap 1.G: Snapshot endpoint stubs | Create 6 stub redirects | 10 |
| 10 | Gap 4: Naming violations | Rename 29 files, consolidate duplicates | — |
| 11 | Gap 1.C (May): Macro HMM concept note | Create `hmm-macro-regime-engine.md` | 0 (undiscoverable) |
| 12 | Gap 1.E (May): `option-implied-erp-horizon-spread.md` | Create specific Lai (2022) concept note | 9 existing refs |

---

*This analysis supersedes Section 1 of [gap-analysis-2026-05-20](gap-analysis-2026-05-20.md) for ThetaData gaps. All MAOPM gaps not explicitly marked CLOSED above remain open.*
