---
tags: ["json-schema", "gamma-exposure", "gex", "regime-detection", "llm-agents", "data-standardization"]
created: 2026-05-19
reviewed: false
source_origin: "q3-research-agenda"
---
# GEX Regime Report JSON Schema

This schema defines the structured payload produced by the GEX/Regime Analyst agent and passed to the strategy debate participants. All gamma exposure values and regime classifications are computed in code (Python/Ray); the LLM receives the synthesized output and provides the `regime_narrative` interpretation only.

## Design Decisions

**Compute in code, interpret in LLM**: GEX Z-scores, the Internal GEX Index, and the Regime Divergence Ratio are deterministic calculations. They are computed upstream by the GEX scanner and emitted as structured fields. The LLM's role is to interpret the regime classification in context, not to derive it.

**`above_gamma_flip` is boolean, not narrative**: Agents that act on gamma flip crossing (e.g., switching from premium-selling to protective positioning) must not infer this from a text description. The field is explicit.

**Divergence regime takes precedence**: When `regime_divergence_ratio` is outside the coherent band (< 0.5 or > 2.0), the `divergence_regime_classification` overrides the coherent sub-regime. Agents must check `divergence_regime_classification` first.

## Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GEXRegimeReport",
  "type": "object",
  "required": ["timestamp", "cycle_id", "underlying_symbol", "underlying_price", "gex_metrics", "regime"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time" },
    "cycle_id": { "type": "string", "description": "MAOPM cycle identifier for audit linkage" },
    "underlying_symbol": { "type": "string", "description": "Primary index or ETF (e.g. 'SPX', 'SPY')" },
    "underlying_price": { "type": "number" },

    "gex_metrics": {
      "type": "object",
      "required": ["index_gex", "internal_gex_index", "regime_divergence_ratio", "gamma_flip_level"],
      "properties": {
        "index_gex": {
          "type": "number",
          "description": "Aggregate GEX of the index (SPX/SPY); positive = dealers net long gamma"
        },
        "index_gex_z_score": {
          "type": "number",
          "description": "Index GEX normalized to 30-day rolling mean/stdev"
        },
        "internal_gex_index": {
          "type": "number",
          "description": "Average GEX Z-score across all 500 S&P 500 constituents; measures internal gamma health"
        },
        "regime_divergence_ratio": {
          "type": "number",
          "description": "Index GEX / sum(component GEX). Coherent band: 0.5–2.0. See Regime Divergence Ratio concept."
        },
        "gamma_flip_level": {
          "type": "number",
          "description": "Price level at which dealer gamma exposure crosses from positive to negative"
        },
        "above_gamma_flip": {
          "type": "boolean",
          "description": "True if underlying_price > gamma_flip_level; drives mean-reversion vs. acceleration regime"
        },
        "gamma_flip_distance_pct": {
          "type": "number",
          "description": "(underlying_price − gamma_flip_level) / underlying_price; negative = below flip"
        }
      }
    },

    "top_weighted_stocks": {
      "type": "array",
      "description": "Top 5–10 index constituents by weight; disproportionate GEX influence tracked here",
      "items": {
        "type": "object",
        "required": ["symbol", "index_weight_pct", "gex", "gex_z_score"],
        "properties": {
          "symbol": { "type": "string" },
          "index_weight_pct": { "type": "number" },
          "gex": { "type": "number" },
          "gex_z_score": { "type": "number", "description": "How far current GEX is from 30-day mean in std devs" },
          "gex_signal": {
            "type": "string",
            "enum": ["strongly_positive", "positive", "neutral", "negative", "strongly_negative"],
            "description": "Rules-based classification of this stock's GEX Z-score"
          }
        }
      }
    },

    "regime": {
      "type": "object",
      "required": ["divergence_regime_classification", "microstructure_bias", "regime_narrative"],
      "properties": {
        "divergence_regime_classification": {
          "type": "string",
          "enum": ["artificial_stability", "coherent", "hidden_strength"],
          "description": "Primary classification based on regime_divergence_ratio. Check this first."
        },
        "coherent_subregime": {
          "type": ["string", "null"],
          "enum": ["component_led_strength", "systemic_equilibrium", "index_led_stability", null],
          "description": "Sub-regime when divergence_regime_classification = 'coherent'. Null otherwise."
        },
        "gamma_environment": {
          "type": "string",
          "enum": ["mean_reverting", "accelerating"],
          "description": "mean_reverting when above_gamma_flip=true (dealers long gamma); accelerating when below (dealers short gamma)"
        },
        "microstructure_bias": {
          "type": "string",
          "enum": ["strong_short_vol", "short_vol", "neutral", "suspend_premium_selling", "divergence_strategy"],
          "description": "Mechanical strategy bias from GEX regime alone. 'suspend_premium_selling' when ratio outside coherent band."
        },
        "new_positions_permitted": {
          "type": "boolean",
          "description": "False when divergence_regime_classification != 'coherent'; fast-path block on new premium-selling trades"
        },
        "regime_narrative": {
          "type": "string",
          "description": "NARRATIVE FIELD — GEX/Regime Analyst's qualitative interpretation of the regime. Downstream agents must not extract numbers from this field."
        }
      }
    }
  }
}
```

## Regime Classification Logic (Rules Engine)

The following is computed in code before the LLM receives the report:

```
if ratio > 2.0:
    divergence_regime_classification = "artificial_stability"
    microstructure_bias = "suspend_premium_selling"
    new_positions_permitted = false
elif ratio < 0.5:
    divergence_regime_classification = "hidden_strength"
    microstructure_bias = "suspend_premium_selling"
    new_positions_permitted = false
else:  # 0.5 ≤ ratio ≤ 2.0
    divergence_regime_classification = "coherent"
    new_positions_permitted = true
    if ratio < 0.9:
        coherent_subregime = "component_led_strength"
        microstructure_bias = "neutral"
    elif ratio <= 1.1:
        coherent_subregime = "systemic_equilibrium"
        microstructure_bias = "short_vol" if above_gamma_flip else "neutral"
    else:  # 1.1 to 2.0
        coherent_subregime = "index_led_stability"
        microstructure_bias = "strong_short_vol"

gamma_environment = "mean_reverting" if above_gamma_flip else "accelerating"
```

This classification is the LLM's prior. It may argue for deviation from `microstructure_bias` in the strategy debate, but must explicitly justify the override.

## Related

- [Vol Surface Summary JSON Schema](vol-surface-summary-json-schema.md)
- [Greek Exposure Report JSON Schema](greek-exposure-report-json-schema.md)
- [LLM Agent Data Handoffs — Structured Communication](../concepts/llm-agent-data-handoffs-structured-communication.md)
- [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md)
- [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md)
- [Regime Detection](../concepts/regime-detection.md)
