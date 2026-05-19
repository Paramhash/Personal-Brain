---
tags: ["llm-agents", "data-communication", "information-loss", "structured-data", "financial-data"]
created: 2023-10-27
reviewed: false
source_origin: "gemini-code-1779179713612.py"
---
# Communication Structures for LLM Agent Handoffs: Deterministic vs. Probabilistic Data

To effectively manage information flow and prevent the "telephone effect" in multi-agent LLM systems, especially when dealing with sensitive or quantitative data, it is crucial to establish a strict boundary between **deterministic data** and **probabilistic interpretation**.

## The Problem of Information Loss

When LLM agents pass free-text narratives containing critical metrics, highly sensitive information such as Gamma signs, strike boundaries, and decimal precision can inevitably degrade or be misinterpreted. This leads to information loss and potential errors in subsequent agent processing or decision-making.

## The Solution: Structured Schemas for Deterministic Data

To minimize this loss, deterministic data — facts, figures, and precise measurements — must be communicated using structured schemas. This approach ensures:
*   **Strict Validation:** Data conforms to predefined types and formats.
*   **Standardized Units:** All metrics are expressed in consistent units (e.g., Greeks standardized to 100-share contract equivalents or raw per-share basis).
*   **Clarity and Precision:** Ambiguity is removed, preserving the exact values and signs of sensitive metrics.

Probabilistic interpretation, on the other hand, refers to the narrative, analysis, or reasoning an LLM agent provides based on the deterministic data. This should be kept separate from the raw, structured data to prevent contamination and ensure the underlying facts remain pristine.

## Structured vs. Narrative: Decision Rule

| Data type | Transmission format | Rationale |
|---|---|---|
| Greeks, strikes, expirations, PoP, IV | Structured schema (JSON) | Exact values; any paraphrase loses precision |
| Regime classification, strategy bias | Enumerated field in schema | Must be machine-readable for downstream rules |
| Qualitative skew interpretation, contextual rationale | Narrative field, explicitly labelled | LLM reasoning; downstream agents must not re-extract numbers from it |
| Debate outcomes, override justifications | Structured entry + narrative rationale | Decision ledger requires both audit trail and reasoning |

The hybrid pattern — structured fields for all deterministic data, a single labelled narrative field per report — is the recommended default. Agents must never infer numeric values from narrative fields.

## Minimum Sufficient Context for LLM Portfolio Reasoning

This addresses Q3 sub-question 4: *What is the minimum context an LLM needs to reason effectively about an options portfolio state?*

**The core principle**: LLMs should receive analyst-synthesized reports, not raw data feeds. The analyst layer (Volatility Analyst, GEX/Regime Analyst, Greeks Analyst) is responsible for reducing raw market data to a structured summary. The LLM debate participants receive those summaries.

**Minimum context set for a strategy initiation decision**:

1. `GEXRegimeReport.regime` block (classification, gamma_environment, microstructure_bias, new_positions_permitted) — ~5 fields
2. `VolSurfaceSummary.iv_metrics` + `vol_regime.classification` + `term_structure.horizon_spread` — ~8 fields
3. `GreekExposureReport.portfolio_totals` + `limit_status.active_breaches` — ~9 fields
4. `GreekExposureReport.positions[].management_flags` for any position with `requires_fast_path = true` — position count dependent
5. Active Board Directives (from Decision Ledger) — directive count dependent
6. Last N cycle summaries from Decision Ledger (recommended N = 3) — for regime continuity context

**What to exclude from LLM context** (available on-demand query only):

- Full per-leg market data (bid/ask/mid) — not needed for strategy debate
- Full `top_weighted_stocks` array — include only if a divergence regime is active
- Full `term_structure.tenors` array — the named scalar fields (`atm_iv_30d`, `atm_iv_180d`, `horizon_spread`) are sufficient
- Position-level Greeks for positions not flagged by `management_flags` — portfolio_totals is sufficient

**Token budget guidance**: The minimum context set above fits comfortably within 2,000–3,000 tokens for a 5–10 position portfolio, leaving ample budget for agent system prompts, debate history, and output. Full raw position data for 20+ positions would require selective inclusion or a retrieval pattern (query by position_id on demand).

## Example Application

Options data schemas implementing this principle:

- [Greek Exposure Report JSON Schema](../entities/greek-exposure-report-json-schema.md) — portfolio Greeks, per-position multi-leg structure, management flags
- [Vol Surface Summary JSON Schema](../entities/vol-surface-summary-json-schema.md) — IV metrics, term structure, horizon spread, skew, vol regime
- [GEX Regime Report JSON Schema](../entities/gex-regime-report-json-schema.md) — GEX metrics, divergence ratio, gamma flip, regime classification