---
tags: [python, class, financial-software, risk-management-tool]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# RegimeRiskScaler Class

The `RegimeRiskScaler` class is a Python implementation of the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]]. It provides the core functionality for dynamically adjusting portfolio-level [[../concepts/portfolio-greek-limits.md|Greek limits]] based on real-time market conditions and predefined risk parameters.

## Purpose
This class encapsulates the logic for:
*   Defining structural limits and decay thresholds for risk scaling.
*   Calculating a continuous non-linear risk multiplier using a [[../concepts/bi-symmetric-sigmoid-decay-function.md|Bi-Symmetric Sigmoid function]].
*   Processing market metrics ([[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio (RDR)]], [[../concepts/gex.md|Gamma Exposure (GEX)]], [[../concepts/vvix.md|Vol-of-Vol Index (VVIX)]]) to determine the appropriate operational mode and scaled limits.
*   Applying asymmetric scaling rules to different [[../concepts/options-greeks.md|Options Greeks]].

## Methods

### `__init__(self, theta_lower: float = 0.5, theta_upper: float = 2.0, k_lower: float = 12.0, k_upper: float = 8.0, gex_critical: float = -100_000_000, vvix_threshold: float = 120.0)`
Initializes the dynamic risk engine with its structural limits and decay thresholds.

*   **Parameters**:
    *   `theta_lower` (float): Lower boundary of the coherent [[../concepts/regime-divergence-ratio.md|RDR]] regime.
    *   `theta_upper` (float): Upper boundary of the coherent [[../concepts/regime-divergence-ratio.md|RDR]] regime.
    *   `k_lower` (float): Speed of risk reduction approaching the lower boundary in the sigmoid function.
    *   `k_upper` (float): Speed of risk reduction approaching the upper boundary in the sigmoid function.
    *   `gex_critical` (float): Absolute negative [[../concepts/gex.md|GEX]] capacity (in USD per 1% move) before a hard override is triggered.
    *   `vvix_threshold` (float): Absolute [[../concepts/vvix.md|Vol-of-Vol]] threshold indicating structural market panic.

### `calculate_rdr_multiplier(self, rdr: float) -> float`
Computes the continuous non-linear multiplier using the [[../concepts/bi-symmetric-sigmoid-decay-function.md|Bi-Symmetric Sigmoid function]]. This multiplier forms the baseline for scaling risk limits.

*   **Parameters**:
    *   `rdr` (float): The current [[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio]].
*   **Returns**:
    *   `float`: A multiplier between 0.0 and 1.0, representing the allowed risk capacity.

### `scale_portfolio_limits(self, base_limits: Dict[str, float], rdr: float, current_gex: float, current_vvix: float) -> Dict[str, Any]`
Processes real-time market metrics against the structural hierarchy to output scaled [[../concepts/portfolio-greek-limits.md|portfolio limits]] for core [[../concepts/options-greeks.md|Greeks]].

*   **Parameters**:
    *   `base_limits` (Dict[str, float]): A dictionary of baseline maximum Greek dollar exposures (e.g., `{'delta': 500000.0, 'gamma': 50000.0}`).
    *   `rdr` (float): Current [[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio]].
    *   `current_gex` (float): Current aggregate Net Dealer [[../concepts/gex.md|Gamma Exposure]] in USD.
    *   `current_vvix` (float): Current level of [[../concepts/vvix.md|Vol-of-Vol Index]].
*   **Returns**:
    *   `Dict[str, Any]`: A dictionary containing:
        *   `operational_mode` (str): The detected market regime (e.g., "STANDARD_COHERENT", "DIVERGENCE_STRATEGY_MODE", "NEGATIVE_GEX_RISK_REDUCTION").
        *   `rdr_multiplier_applied` (float): The RDR-derived multiplier.
        *   `scaled_greek_limits` (Dict[str, float]): The adjusted Greek limits.
        *   `premium_selling_allowed` (bool): Indicates if premium selling is allowed in the current mode.

## Operational Modes
The `scale_portfolio_limits` method can determine three primary operational modes:
1.  **STANDARD_COHERENT**: The market is within a stable RDR range, and no critical GEX or VVIX overrides are active. Limits are scaled smoothly by the RDR multiplier.
2.  **NEGATIVE_GEX_RISK_REDUCTION**: Triggered when `current_gex` falls below `gex_critical`. This mode contracts Gamma and Vega limits while widening Delta limits.
3.  **DIVERGENCE_STRATEGY_MODE**: Triggered when `current_vvix` exceeds `vvix_threshold` or `rdr` exceeds `theta_upper`. This is a severe mode that drastically reduces short volatility/gamma risk and expands Delta buffers.

## Related Concepts
*   [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]]
*   [[../concepts/bi-symmetric-sigmoid-decay-function.md|Bi-Symmetric Sigmoid Decay Function]]
*   [[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio (RDR)]]
*   [[../concepts/gex.md|Gamma Exposure (GEX)]]
*   [[../concepts/vvix.md|Vol-of-Vol Index (VVIX)]]
*   [[../concepts/portfolio-greek-limits.md|Portfolio Greek Limits]]
*   [[../concepts/options-greeks.md|Options Greeks]]