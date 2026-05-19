---
tags: ["json-schema", "options-trading", "financial-data", "llm-agents", "data-standardization"]
created: 2023-10-27
reviewed: false
source_origin: "gemini-code-1779179713612.py"
---
# Greek Exposure Report JSON Schema

This JSON schema defines a standardized structure for reporting options Greek exposures, designed to facilitate deterministic data transfer between LLM agents or systems. Its purpose is to ensure that critical financial metrics related to options portfolios are communicated precisely, preventing information loss and misinterpretation.

## Key Features

*   **Explicit Typing:** All fields have defined data types (e.g., `string`, `number`, `date-time`).
*   **Required Fields:** Essential data points are marked as mandatory.
*   **Standardized Units:** The schema implicitly encourages the use of standardized units for Greeks (e.g., per 100-share contract or per-share basis, as consistently applied).

## Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "GreekExposureReport",
  "type": "object",
  "required": ["timestamp", "cycle_id", "underlying_symbol", "underlying_price", "portfolio_totals", "positions"],
  "properties": {
    "timestamp": { "type": "string", "format": "date-time", "description": "UTC timestamp of report generation" },
    "cycle_id": { "type": "string", "description": "MAOPM analysis cycle identifier for audit linkage" },
    "underlying_symbol": { "type": "string" },
    "underlying_price": { "type": "number", "description": "Spot price at time of report" },
    "portfolio_totals": {
      "type": "object",
      "required": ["net_delta_dollars", "net_gamma", "net_vega", "net_theta", "beta_weighted_delta", "aggregate_max_loss", "aggregate_bpr", "theta_to_vega_ratio"],
      "properties": {
        "net_delta_dollars": { "type": "number", "description": "Dollar P&L change per $1 move in underlying" },
        "net_gamma": { "type": "number", "description": "Rate of delta change per $1 move" },
        "net_vega": { "type": "number", "description": "Dollar P&L change per 1% IV change" },
        "net_theta": { "type": "number", "description": "Daily P&L from time decay (positive = premium seller)" },
        "beta_weighted_delta": { "type": "number", "description": "Delta normalized to SPY-equivalent exposure" },
        "aggregate_max_loss": { "type": "number", "description": "Sum of per-position max losses (dollars)" },
        "aggregate_bpr": { "type": "number", "description": "Total buying power reduction deployed (dollars)" },
        "theta_to_vega_ratio": { "type": "number", "description": "Daily theta / net vega; efficiency of premium collection" }
      }
    },
    "limit_status": {
      "type": "object",
      "description": "Current Greek values vs. hard limits; drives breach alerts",
      "properties": {
        "delta_within_limit": { "type": "boolean" },
        "vega_within_limit": { "type": "boolean" },
        "bpr_utilization_pct": { "type": "number", "description": "Aggregate BPR as % of net liquidation value" },
        "max_loss_utilization_pct": { "type": "number", "description": "Aggregate max loss as % of portfolio value" },
        "active_breaches": {
          "type": "array",
          "items": {
            "type": "object",
            "required": ["greek", "current_value", "limit_value", "severity"],
            "properties": {
              "greek": { "type": "string", "enum": ["delta", "gamma", "vega", "theta", "bpr", "max_loss"] },
              "current_value": { "type": "number" },
              "limit_value": { "type": "number" },
              "severity": { "type": "string", "enum": ["warning", "hard_breach"] }
            }
          }
        }
      }
    },
    "positions": {
      "type": "array",
      "items": { "$ref": "#/definitions/Position" }
    }
  },
  "definitions": {
    "Leg": {
      "type": "object",
      "required": ["leg_id", "symbol", "expiration", "strike", "option_type", "position_type", "contracts", "greeks", "market"],
      "properties": {
        "leg_id": { "type": "string", "description": "e.g. 'long_put', 'short_call_upper'" },
        "symbol": { "type": "string", "description": "OCC option symbol" },
        "expiration": { "type": "string", "format": "date" },
        "strike": { "type": "number" },
        "option_type": { "type": "string", "enum": ["call", "put"] },
        "position_type": { "type": "string", "enum": ["long", "short"] },
        "contracts": { "type": "integer", "minimum": 1 },
        "dte": { "type": "integer", "description": "Days to expiration at report time" },
        "greeks": {
          "type": "object",
          "required": ["delta", "gamma", "vega", "theta"],
          "description": "Per-contract Greeks; multiply by contracts × 100 for dollar exposure",
          "properties": {
            "delta": { "type": "number" },
            "gamma": { "type": "number" },
            "vega": { "type": "number", "description": "Dollar change per 1% IV move per contract" },
            "theta": { "type": "number", "description": "Dollar decay per day per contract" },
            "rho": { "type": "number" }
          }
        },
        "market": {
          "type": "object",
          "required": ["bid", "ask", "mid", "iv"],
          "properties": {
            "bid": { "type": "number" },
            "ask": { "type": "number" },
            "mid": { "type": "number" },
            "iv": { "type": "number", "description": "Implied volatility (decimal, e.g. 0.25 = 25%)" }
          }
        }
      }
    },
    "Position": {
      "type": "object",
      "required": ["position_id", "strategy_type", "underlying_symbol", "opened_date", "legs", "net_greeks", "risk_metrics"],
      "properties": {
        "position_id": { "type": "string", "description": "Unique position identifier; links to Decision Ledger entry" },
        "strategy_type": {
          "type": "string",
          "enum": ["long_call", "long_put", "short_call", "short_put", "bull_put_spread", "bear_call_spread", "iron_condor", "iron_butterfly", "straddle", "strangle", "covered_call", "cash_secured_put", "calendar_spread", "diagonal_spread"],
          "description": "Determines expected number of legs and payoff interpretation"
        },
        "underlying_symbol": { "type": "string" },
        "opened_date": { "type": "string", "format": "date" },
        "target_dte_open": { "type": "integer", "description": "DTE when position was opened (e.g. 45)" },
        "legs": {
          "type": "array",
          "minItems": 1,
          "maxItems": 4,
          "items": { "$ref": "#/definitions/Leg" },
          "description": "Ordered legs; e.g. iron condor = [short_put, long_put, short_call, long_call]"
        },
        "net_greeks": {
          "type": "object",
          "required": ["net_delta", "net_gamma", "net_vega", "net_theta"],
          "description": "Sum of (per-leg Greek × contracts × 100 × position_sign) across all legs",
          "properties": {
            "net_delta": { "type": "number" },
            "net_gamma": { "type": "number" },
            "net_vega": { "type": "number" },
            "net_theta": { "type": "number" }
          }
        },
        "risk_metrics": {
          "type": "object",
          "required": ["max_profit", "max_loss", "pop", "breakeven_prices", "bpr", "current_pl"],
          "properties": {
            "max_profit": { "type": "number", "description": "Total premium received (credit spreads) or theoretical max (debit spreads), dollars" },
            "max_loss": { "type": "number", "description": "Worst-case loss at expiration, dollars (positive = loss amount)" },
            "pop": { "type": "number", "description": "Probability of profit (0.0–1.0); derived from implied distribution" },
            "breakeven_prices": {
              "type": "array",
              "items": { "type": "number" },
              "description": "Underlying prices at which P&L = 0 at expiration; iron condor has 2 breakevens"
            },
            "bpr": { "type": "number", "description": "Buying power reduction / margin required, dollars" },
            "current_pl": { "type": "number", "description": "Unrealized P&L at report time (positive = profit), dollars" },
            "pl_pct_of_max_profit": { "type": "number", "description": "current_pl / max_profit; used for early-close rules (e.g. close at 50%)" }
          }
        },
        "management_flags": {
          "type": "object",
          "description": "Triggered flags for the position management fast-path; populated by rules engine, not LLM",
          "properties": {
            "dte_alert": { "type": "boolean", "description": "True if minimum leg DTE ≤ 21" },
            "delta_escalation": { "type": "boolean", "description": "True if |net_delta| > 0.20 at DTE < 14" },
            "pin_risk_active": { "type": "boolean", "description": "True if underlying within 0.5% of any short strike within 60 min of expiration" },
            "profit_target_reached": { "type": "boolean", "description": "True if pl_pct_of_max_profit ≥ 0.50" },
            "requires_fast_path": { "type": "boolean", "description": "True if any flag above is true; bypasses LLM debate loop" }
          }
        }
      }
    }
  }
}
```

## Relation to LLM Agent Communication

This schema serves as a concrete example of how to implement [structured communication for LLM agent handoffs](../concepts/llm-agent-data-handoffs-structured-communication.md). By enforcing a clear, machine-readable format for deterministic data, it prevents the degradation of sensitive financial metrics that can occur when agents rely solely on free-text narratives.