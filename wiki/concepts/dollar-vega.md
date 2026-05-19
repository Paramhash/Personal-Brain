---
tags: [options-trading, risk-metrics, derivatives, quantitative-finance]
created: 2023-10-27
reviewed: false
source_origin: "temporal_risk_architecture.md"
---
# Dollar-Vega ($\mathcal{V}_{\$}$)

## Definition
Dollar-Vega ($\mathcal{V}_{\$}$), also known as Vega Notional or Dollar-Value of Vega, is a measure of an option's sensitivity to a 1% change in implied volatility, expressed in dollar terms. Unlike standard Vega, which is typically expressed as the change in option price for a 1% *point* change in implied volatility, Dollar-Vega scales this sensitivity to a more intuitive dollar value, often by multiplying Vega by the underlying asset's price.

## Calculation and Significance
The exact calculation can vary, but it generally involves:
$$\mathcal{V}_{\$} = \text{Vega} \times \text{Underlying Price} \times 0.01$$
(for a 1% change in implied volatility, assuming Vega is for a 1% point change)

Dollar-Vega is crucial for risk management as it directly quantifies the monetary impact of volatility changes on a portfolio. It helps traders understand their exposure to shifts in implied volatility across different options and underlying assets.

## Role in Temporal Risk Architectures
In advanced risk management frameworks like the [[../concepts/dual-engine-temporal-risk-architecture.md|Dual-Engine Temporal Risk Architecture]], Dollar-Vega serves as a duration-weighting factor for the Strategic Engine. When calculating the $\text{RDR}_{\text{Strategic}}$, longer-dated options' [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX)]] can be weighted by their Dollar-Vega to emphasize contracts that have a more significant sensitivity to structural volatility changes, thereby reflecting institutional positioning and macro volatility regimes more accurately.