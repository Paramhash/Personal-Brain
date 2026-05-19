---
tags: [options-trading, financial-derivatives, risk-metrics]
created: 2023-10-27
reviewed: false
source_origin: "regime_risk_scaling.py"
---
# Options Greeks

**Options Greeks** are a set of measures that quantify the sensitivity of an option's price (or a portfolio's value) to changes in various underlying parameters. They are crucial tools for traders and risk managers to understand and manage the risks associated with options positions.

## Key Options Greeks

The most commonly referenced Greeks, and those managed by the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]], include:

*   **Delta (Δ)**:
    *   Measures the sensitivity of an option's price to a $1 change in the underlying asset's price.
    *   Represents the equivalent number of shares of the underlying asset that the option behaves like.
    *   A portfolio's net Delta indicates its directional exposure.

*   **Gamma (Γ)**:
    *   Measures the sensitivity of an option's Delta to a $1 change in the underlying asset's price.
    *   It's the "rate of change" of Delta. High Gamma means Delta changes rapidly with small moves in the underlying, leading to significant P&L swings and hedging challenges.
    *   Often associated with convexity and path-dependent risk.

*   **Vega (ν)**:
    *   Measures the sensitivity of an option's price to a 1% change in the underlying asset's implied volatility.
    *   High Vega exposure means a portfolio is highly sensitive to shifts in market expectations of future price swings.
    *   Often referred to as "kappa" (κ).

*   **Theta (Θ)**:
    *   Measures the sensitivity of an option's price to the passage of one day (time decay).
    *   It represents the amount an option's value will decrease each day, all else being equal.
    *   Long options typically have negative Theta (losing value over time), while short options have positive Theta (gaining value over time).

## Importance in Risk Management
Understanding and managing Greeks is essential for:
*   **Hedging**: Constructing portfolios that are neutral or have desired exposures to market factors.
*   **Risk Assessment**: Quantifying potential gains or losses under different market scenarios.
*   **Strategy Adjustment**: Adapting trading strategies based on current Greek exposures and market conditions.

The [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]] dynamically adjusts [[../concepts/portfolio-greek-limits.md|Portfolio Greek Limits]] to ensure that these exposures remain within acceptable bounds, especially during periods of market stress or divergence.