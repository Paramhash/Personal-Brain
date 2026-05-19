---
tags: [python, code, financial-engineering, risk-management]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# `regime_risk_scaling.py`

This Python module implements a **Regime Risk Scaling Engine** designed for dynamic adjustment of portfolio-level Greek limits. It utilizes a sophisticated Bi-Symmetric Sigmoid Decay Function to provide continuous, non-linear scaling of risk exposures based on prevailing market conditions.

The module integrates absolute filters for critical market metrics such as Gamma Exposure (GEX) and Volatility of Volatility (VVIX), alongside asymmetric Greek scaling rules to adapt to different market regimes.

## Key Components:
*   **[[../entities/regimeriskscaler-class.md|RegimeRiskScaler Class]]**: The core implementation of the engine.
*   **[[../concepts/bi-symmetric-sigmoid-decay-function.md|Bi-Symmetric Sigmoid Decay Function]]**: Used for continuous risk multiplier calculation.
*   **[[../concepts/gex.md|GEX]] Filters**: Absolute thresholds for aggregate dealer gamma exposure.
*   **[[../concepts/vvix.md|VVIX]] Thresholds**: Absolute thresholds for volatility of volatility.
*   **Asymmetric Greek Scaling**: Rules that adjust different [[../concepts/options-greeks.md|Greeks]] (Delta, Gamma, Vega, Theta) differently based on the detected market regime.

This module provides a robust framework for managing portfolio risk dynamically, moving beyond static limits to respond intelligently to evolving market structures and stress events.

---
**Original Payload:**
```python
"""
Regime Risk Scaling Engine
===========================
This module implements the structural architecture for dynamic portfolio-level
Greek limits using a Bi-Symmetric Sigmoid Decay Function, integrating absolute 
GEX filters and asymmetric Greek scaling rules.
"""

import numpy as np
from typing import Dict, Any

class RegimeRiskScaler:
    def __init__(self, 
                 theta_lower: float = 0.5, 
                 theta_upper: float = 2.0, 
                 k_lower: float = 12.0, 
                 k_upper: float = 8.0,
                 gex_critical: float = -100_000_000, # Metric in dollars per 1% move
                 vvix_threshold: float = 120.0):
        """
        Initializes the dynamic risk engine with structural limits and decay thresholds.
        
        Parameters:
            theta_lower (float): Lower boundary of the coherent RDR regime.
            theta_upper (float): Upper boundary of the coherent RDR regime.
            k_lower (float): Speed of risk reduction approaching lower boundary.
            k_upper (float): Speed of risk reduction approaching upper boundary.
            gex_critical (float): Absolute negative GEX capacity before hard override.
            vvix_threshold (float): Absolute Vol-of-Vol threshold indicating structural panic.
        """
        self.theta_lower = theta_lower
        self.theta_upper = theta_upper
        self.k_lower = k_lower
        self.k_upper = k_upper
        self.gex_critical = gex_critical
        self.vvix_threshold = vvix_threshold

    def calculate_rdr_multiplier(self, rdr: float) -> float:
        """
        Computes the continuous non-linear multiplier using a Bi-Symmetric Sigmoid function.
        Handles tail behaviors asymptotically approaching zero risk capacity.
        """
        # Logistic component for the lower bound
        sigmoid_l = 1.0 / (1.0 + np.exp(-self.k_lower * (rdr - self.theta_lower)))
        # Logistic component for the upper bound
        sigmoid_u = 1.0 / (1.0 + np.exp(-self.k_upper * (rdr - self.theta_upper)))
        
        # Combined multiplier curve bound strictly between 0.0 and 1.0
        multiplier = sigmoid_l - sigmoid_u
        return float(np.clip(multiplier, 0.0, 1.0))

    def scale_portfolio_limits(self, 
                               base_limits: Dict[str, float], 
                               rdr: float, 
                               current_gex: float, 
                               current_vvix: float) -> Dict[str, Any]:
        """
        Processes real-time market metrics against the structural hierarchy to output
        scaled portfolio limits for core Greeks.
        
        Parameters:
            base_limits (Dict): Baseline maximum Greek dollar exposures {'delta', 'gamma', 'vega', 'theta'}
            rdr (float): Current Regime Divergence Ratio.
            current_gex (float): Current aggregate Net Dealer Gamma exposure in USD.
            current_vvix (float): Current level of Vol-of-Vol index.
            
        Returns:
            Dict: Adjusted limits and corresponding operational status.
        """
        # 1. Compute baseline continuous multiplier from RDR
        m_rdr = self.calculate_rdr_multiplier(rdr)
        
        # Initialize output structures
        scaled_limits = {}
        operational_mode = "STANDARD_COHERENT"
        
        # 2. Check for absolute structural overrides (Layer 1 & 2)
        gex_override_active = current_gex < self.gex_critical
        vvix_override_active = current_vvix > self.vvix_threshold
        
        # 3. Asymmetric Greek Scaling Application
        if vvix_override_active or rdr > self.theta_upper:
            operational_mode = "DIVERGENCE_STRATEGY_MODE"
        elif gex_override_active:
            operational_mode = "NEGATIVE_GEX_RISK_REDUCTION"
            
        for greek, base_limit in base_limits.items():
            if operational_mode == "DIVERGENCE_STRATEGY_MODE":
                # Severe environment: Crush short volatility/gamma risk, expand delta buffers
                if greek in ['vega', 'gamma']:
                    scaled_limits[greek] = base_limit * 0.05  # 95% reduction, new premium blocked
                elif greek == 'delta':
                    scaled_limits[greek] = base_limit * 1.75  # Widen delta limit to prevent over-hedging churn
                else:
                    scaled_limits[greek] = base_limit * m_rdr
                    
            elif operational_mode == "NEGATIVE_GEX_RISK_REDUCTION":
                # Dealer short-gamma environment: contract path-dependent risk
                if greek == 'gamma':
                    scaled_limits[greek] = base_limit * 0.25
                elif greek == 'vega':
                    scaled_limits[greek] = base_limit * 0.50
                elif greek == 'delta':
                    scaled_limits[greek] = base_limit * 1.50  # Widen to absorb localized spot gaps
                else:
                    scaled_limits[greek] = base_limit * m_rdr
                    
            else:
                # Coherent Regime: Standard non-linear scaling across the core band
                if greek in ['gamma', 'vega', 'theta']:
                    scaled_limits[greek] = base_limit * m_rdr
                elif greek == 'delta':
                    # In hyper-stable regimes (RDR middle), delta limits can tighten smoothly
                    scaled_limits[greek] = base_limit * max(m_rdr, 0.85)

        return {
            "operational_mode": operational_mode,
            "rdr_multiplier_applied": round(m_rdr, 4),
            "scaled_greek_limits": scaled_limits,
            "premium_selling_allowed": operational_mode == "STANDARD_COHERENT"
        }

# --- Verification & Example Execution Run ---
if __name__ == "__main__":
    # Define baseline Greek dollar value tolerances
    portfolio_base_risk = {
        "delta": 500_000.0,  # Max dollar delta limit
        "gamma": 50_000.0,   # Max dollar gamma limit
        "vega":  25_000.0,   # Max dollar vega limit
        "theta": 40_000.0    # Max dollar theta limit
    }
    
    scaler = RegimeRiskScaler()
    
    print("=== SCENARIO 1: COHERENT STABLE MARKET (RDR = 1.1, High Positive GEX) ===")
    metrics_stable = scaler.scale_portfolio_limits(portfolio_base_risk, rdr=1.1, current_gex=200_000_000, current_vvix=85.0)
    print(f"Mode: {metrics_stable['operational_mode']} | Multiplier: {metrics_stable['rdr_multiplier_applied']}")
    print(f"Limits: {metrics_stable['scaled_greek_limits']}\n")

    print("=== SCENARIO 2: COHERENT EDGE TAPER (RDR = 1.8, GEX Mildly Neutral) ===")
    metrics_edge = scaler.scale_portfolio_limits(portfolio_base_risk, rdr=1.8, current_gex=10_000_000, current_vvix=98.0)
    print(f"Mode: {metrics_edge['operational_mode']} | Multiplier: {metrics_edge['rdr_multiplier_applied']}")
    print(f"Limits: {metrics_edge['scaled_greek_limits']}\n")

    print("=== SCENARIO 3: TAIL DIVERGENCE / VOL EXPANSION (RDR = 2.4, Deep Negative GEX) ===")
    metrics_crisis = scaler.scale_portfolio_limits(portfolio_base_risk, rdr=2.4, current_gex=-150_000_000, current_vvix=135.0)
    print(f"Mode: {metrics_crisis['operational_mode']} | Multiplier: {metrics_crisis['rdr_multiplier_applied']}")
    print(f"Limits: {metrics_crisis['scaled_greek_limits']}\n")