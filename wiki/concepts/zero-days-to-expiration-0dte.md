---
tags: [options-trading, market-microstructure, derivatives, temporal-risk]
created: 2023-10-27
reviewed: false
source_origin: "temporal_risk_architecture.md"
---
# Zero Days To Expiration (0DTE) Options

## Definition
Zero Days To Expiration (0DTE) options are derivative contracts that expire on the same trading day they are opened or traded. They are characterized by their extremely short lifespan, leading to unique pricing dynamics and market impact.

## Characteristics and Market Impact
*   **High Gamma Sensitivity:** 0DTE options exhibit extremely high nominal gamma, meaning their delta changes rapidly with small movements in the underlying asset price. This can lead to significant dealer hedging activity.
*   **Low Vega:** Due to their short time to expiration, 0DTE options have virtually no [[../concepts/dollar-vega.md|Vega]], making them insensitive to changes in implied volatility.
*   **Dominance in Intraday Liquidity:** The massive volume and rapid decay of 0DTE options can dominate intraday order flow and liquidity, often leading to "dealer pinning" where the underlying asset price is drawn towards high gamma strike prices.
*   **Impact on Risk Management:** The unique characteristics of 0DTE options necessitate specialized risk management approaches, such as the [[../concepts/dual-engine-temporal-risk-architecture.md|Dual-Engine Temporal Risk Architecture]], to prevent their short-term noise from contaminating longer-term structural risk signals. They are a primary focus of the Tactical Engine in such architectures.