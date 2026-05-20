---
tags: ["financial model", "options pricing", "mathematical model", "derivatives"]
created: 2023-10-27
reviewed: false
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
---
# Black-Scholes Model

The Black-Scholes model (often referred to as Black-Scholes-Merton) is a seminal mathematical model for the pricing of European-style options. Developed by Fischer Black, Myron Scholes, and Robert Merton, it provides a theoretical framework for determining the fair price of an option contract, taking into account factors such as the underlying asset's price, strike price, time to expiration, volatility, and risk-free interest rate.

## Application in Options Trading Pipelines

In a [[../concepts/systematic-options-trading-pipeline-1dte-7dte.md|systematic options trading pipeline]], the Black-Scholes model is frequently used as a component within the [[../concepts/gamma-exposure-gex.md|Gamma Exposure (GEX) Calculation Module]]. Specifically, it can be employed to:

*   **Calculate Gamma ($\Gamma$):** Gamma, one of the "Greeks," measures the rate of change of an option's delta with respect to a change in the underlying asset's price. The Black-Scholes formula provides a way to derive this value, which is then used in the GEX calculation.

While more advanced models and empirical methods exist, Black-Scholes remains a foundational tool for understanding options pricing and its sensitivities.