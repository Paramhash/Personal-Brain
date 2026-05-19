---
tags: ["json-schema", "options-trading", "implied-volatility", "volatility-surface", "llm-agents", "data-standardization"]
created: 2026-05-19
reviewed: false
source_origin: "q3-research-agenda"
---
# Vol Surface Summary JSON Schema

This schema defines the structured payload passed from the Volatility Analyst agent to the strategy debate participants. It separates deterministic IV measurements (structured data) from the vol regime narrative (LLM interpretation), per the [LLM Agent Data Handoffs](../concepts/llm-agent-data-handoffs-structured-communication.md) principle.

## Design Decisions

**What is structured**: All numeric IV measurements, term structure shape classification, skew metrics, IVR/IVP — these must not be paraphrased in free text.

**What is narrative**: The `vol_regime_narrative` field is the only free-text field. It carries the Volatility Analyst's qualitative interpretation (e.g., "the skew shape suggests fear rather than structural demand") and is explicitly labelled as such so downstream agents do not treat it as a source of ground-truth numbers.

**Tenors**: 30-day and 180-day ATM IV are required because they underlie the [horizon spread](../concepts/Option-Implied-Regimes.md) regime signal (Lai 2022). Additional tenors are optional.

## Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "VolSurfaceSummary",
  "type": "object",
  "required": ["timestamp", "cycle_id", "underlying_symbol", "underlying_price", "iv_metrics", "term_structure", "skew", "vol_regime"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "cycle_id": { "type": "string", "description": "MAOPM cycle identifier for audit linkage" },
    "underlying_symbol": { "type": "string" },
    "underlying_price": { "type": "number" },

    "iv_metrics": {
      "type": "object",
      "required": ["ivr", "ivp", "atm_iv_30d", "atm_iv_180d"],
      "properties": {
        "ivr": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "IV Rank: (current IV − 52-wk low) / (52-wk high − 52-wk low) × 100"
        },
        "ivp": {
          "type": "number",
          "minimum": 0,
          "maximum": 100,
          "description": "IV Percentile: % of days in past year where IV < current IV"
        },
        "atm_iv_30d": {
          "type": "number",
          "description": "ATM implied volatility at 30-day constant maturity (decimal, e.g. 0.18 = 18%)"
        },
        "atm_iv_60d": { "type": "number" },
        "atm_iv_180d": {
          "type": "number",
          "description": "ATM implied volatility at 180-day constant maturity; required for horizon spread"
        },
        "vix_spot": {
          "type": "number",
          "description": "VIX index level at report time; included for cross-reference only"
        }
      }
    },

    "term_structure": {
      "type": "object",
      "required": ["shape", "tenors"],
      "properties": {
        "shape": {
          "type": "string",
          "enum": ["contango", "backwardation", "flat"],
          "description": "contango = near-term IV < far-term IV (normal); backwardation = near-term IV > far-term IV (stressed)"
        },
        "slope_30_180": {
          "type": "number",
          "description": "atm_iv_180d − atm_iv_30d; positive = contango, negative = backwardation"
        },
        "horizon_spread": {
          "type": "number",
          "description": "Option-implied ERP at 180d minus ERP at 30d (Lai 2022). Negative = crisis regime signal. Computed in code, not by LLM."
        },
        "tenors": {
          "type": "array",
          "description": "Full term structure for reference; agents should use named fields above for decisions",
          "items": {
            "type": "object",
            "required": ["tenor_days", "atm_iv"],
            "properties": {
              "tenor_days": { "type": "integer" },
              "atm_iv": { "type": "number" }
            }
          }
        }
      }
    },

    "skew": {
      "type": "object",
      "required": ["put_skew_25d", "call_skew_25d"],
      "description": "Skew measured at 25-delta; positive put_skew = IV of 25d put > ATM IV (typical; demand for downside hedges)",
      "properties": {
        "put_skew_25d": {
          "type": "number",
          "description": "IV(25-delta put) − atm_iv_30d; basis points, e.g. 0.05 = 5 vol points"
        },
        "call_skew_25d": {
          "type": "number",
          "description": "IV(25-delta call) − atm_iv_30d; negative = normal (calls cheaper than puts)"
        },
        "skew_ratio": {
          "type": "number",
          "description": "put_skew_25d / call_skew_25d; > 1.5 signals elevated downside fear vs. upside demand"
        },
        "skew_interpretation_signal": {
          "type": "string",
          "enum": ["fear_driven", "structural_demand", "neutral", "call_skew_dominant"],
          "description": "Rules-based classification of skew shape; set by code, not LLM"
        }
      }
    },

    "vol_regime": {
      "type": "object",
      "required": ["classification", "vol_regime_narrative"],
      "properties": {
        "classification": {
          "type": "string",
          "enum": ["low_vol_stable", "elevated_vol_rangebound", "vol_expansion", "vol_crush_post_event", "crisis"],
          "description": "Rules-based regime label derived from IVR, term structure shape, and horizon spread"
        },
        "strategy_bias": {
          "type": "string",
          "enum": ["strong_short_vol", "short_vol", "neutral", "long_vol", "strong_long_vol"],
          "description": "Mechanical bias implied by classification; the LLM may override with a reasoned argument"
        },
        "vol_regime_narrative": {
          "type": "string",
          "description": "NARRATIVE FIELD — Volatility Analyst's qualitative interpretation. Downstream agents must not extract numbers from this field."
        }
      }
    }
  }
}
```

## Field Guidance for Downstream Agents

| Decision | Fields to Use | Do Not Use |
|---|---|---|
| Short-vol vs. long-vol bias | `vol_regime.classification`, `iv_metrics.ivr`, `iv_metrics.ivp` | `vol_regime_narrative` for numbers |
| Macro crisis leading indicator | `term_structure.horizon_spread` | None — must use the computed value |
| Skew interpretation debate | `skew.skew_interpretation_signal` as prior; `vol_regime_narrative` for qualitative argument | Raw strike IV values |
| Strategy debate input | `vol_regime.strategy_bias` as the Volatility Analyst's opening position | — |

## Related

- [GEX Regime Report JSON Schema](gex-regime-report-json-schema.md)
- [Greek Exposure Report JSON Schema](greek-exposure-report-json-schema.md)
- [LLM Agent Data Handoffs — Structured Communication](../concepts/llm-agent-data-handoffs-structured-communication.md)
- [Option-Implied Regimes](../concepts/Option-Implied-Regimes.md)
- [Implied Volatility](../concepts/implied-volatility.md)
