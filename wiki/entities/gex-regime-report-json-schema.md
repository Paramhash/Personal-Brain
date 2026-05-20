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
        "index_gex_sign": {
          "type": "string",
          "enum": ["positive", "negative"],
          "description": "Sign of raw Index GEX. Negative = dealers structurally short index gamma; triggers Layer 1 hard cap independently of RDR sigmoid."
        },
        "regime_divergence_ratio": {
          "type": "number",
          "minimum": 0,
          "description": "|Index GEX| / \u03a3|Component GEX|. Always non-negative. Coherent band: 0.5\u20132.0. Raw signed values are NOT used here; sign is tracked separately in index_gex_sign."
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
    },

    "hmm_state": {
      "type": "object",
      "description": "Output of the Multivariate Gaussian HMM Latent Regime Engine. Computed nightly in batch; updated intraday using existing model parameters (no refit). Supplements the rules-based regime block — rules retain hard-cap authority (Layer 1 / Layer 2); HMM posterior drives the Layer 3 sigmoid scaler M(x).",
      "required": ["state_label", "state_semantics", "posterior_probs", "transition_row", "regime_persistence_expected_bars", "model_fit_date"],
      "properties": {
        "state_label": {
          "type": "integer",
          "minimum": 0,
          "description": "Viterbi-decoded current hidden state index S_t."
        },
        "state_semantics": {
          "type": "string",
          "enum": ["dealer_stabilized", "transitional", "gamma_accelerating"],
          "description": "Canonical post-fit label assigned by inspecting emission mean mu_k: lowest realized vol + positive GEX Z-score = dealer_stabilized; highest vol + negative GEX Z-score = gamma_accelerating."
        },
        "posterior_probs": {
          "type": "array",
          "description": "P(S_t = k | O_1:t) for each state k, computed by forward algorithm. Sums to 1.0. Used as continuous Greek-limit scaler: M(x) = P(dealer_stabilized) * M_max.",
          "items": { "type": "number", "minimum": 0, "maximum": 1 },
          "minItems": 3,
          "maxItems": 3
        },
        "transition_row": {
          "type": "array",
          "description": "A[state_label, :] — transition probabilities from current state to each next state. Enables early position management: if P(current -> gamma_accelerating) > 0.15, tighten limits proactively.",
          "items": { "type": "number", "minimum": 0, "maximum": 1 },
          "minItems": 3,
          "maxItems": 3
        },
        "regime_persistence_expected_bars": {
          "type": "number",
          "description": "Expected remaining duration in current state: E[T] = 1 / (1 - A[state_label, state_label]). In trading bars (daily)."
        },
        "model_fit_date": {
          "type": "string",
          "format": "date",
          "description": "Date of most recent nightly Baum-Welch refit. Intraday observations use the fitted model from this date without refitting."
        }
      }
    }
  }
}
```

## Regime Classification Logic (Rules Engine)

The following is computed in code before the LLM receives the report:

```
# Step 1: Compute absolute-value RDR to preserve sigmoid validity
# Raw signed GEX values must NOT be passed into the sigmoid function directly.
# Index GEX sign is tracked separately and triggers the Layer 1 hard cap.
index_gex_sign = "negative" if index_gex < 0 else "positive"
ratio = abs(index_gex) / sum(abs(g) for g in component_gex_values)

# Step 2: Layer 1 binary override — negative Index GEX
# Dealers structurally short index gamma: hard cap on Γ and ν regardless of ratio.
if index_gex_sign == "negative":
    layer1_hard_cap_active = True  # Handled by GEX filter; RDR sigmoid still runs in parallel

# Step 3: RDR sigmoid classification (runs on absolute ratio)
if ratio > 2.0:
    divergence_regime_classification = "artificial_stability"
    microstructure_bias = "suspend_premium_selling"
    new_positions_permitted = False
elif ratio < 0.5:
    # Hidden Strength — Dispersion Warning:
    # Single-stock vol is expanding relative to index. Index options underprice real basket
    # volatility. Selling index premium (SPX/SPY iron condors) is structurally dangerous
    # even if index surface appears calm. Suspend index premium-selling.
    divergence_regime_classification = "hidden_strength"
    microstructure_bias = "suspend_premium_selling"
    new_positions_permitted = False
else:  # 0.5 ≤ ratio ≤ 2.0
    divergence_regime_classification = "coherent"
    new_positions_permitted = True
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

# Step 4: HMM Layer 3 continuous scaler (supplements rules; does not override hard caps)
# Nightly refit (Baum-Welch on rolling 252-day window) produces A, mu_k, Sigma_k.
# Intraday: forward-pass on today's X_t = [log_return, parkinson_vol, vrp_trend, gex_z_score, iv_hv_skew, horizon_spread_delta]
state_label = viterbi_decode(X_t)                      # S_t ∈ {0, 1, 2}
posterior_probs = forward_algorithm(X_t)               # P(S_t = k | O_1:t)
# state_semantics assigned by post-fit canonical labeling (ascending realized vol of mu_k)
# Greek limit scaler: M(x) = P(dealer_stabilized) * M_max (replaces hard RDR threshold → sigmoid lookup)
# Early management trigger: if transition_row[state_label][gamma_accelerating] > 0.15 → proactive limit tightening
```

This classification is the LLM's prior. It may argue for deviation from `microstructure_bias` in the strategy debate, but must explicitly justify the override.

## Related

- [Vol Surface Summary JSON Schema](vol-surface-summary-json-schema.md)
- [Greek Exposure Report JSON Schema](greek-exposure-report-json-schema.md)
- [LLM Agent Data Handoffs — Structured Communication](../concepts/llm-agent-data-handoffs-structured-communication.md)
- [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md)
- [Regime Divergence Ratio](../concepts/regime-divergence-ratio.md)
- [Regime Detection](../concepts/regime-detection.md)
- [HMM in Finance — Latent Regime Engine](../concepts/hidden-markov-model-hmm-in-finance.md)
- [HMM Approaches in Options Pricing and Agent Architecture](../research/hmm-estimates-of-probability-from-option-prices.md)
