---
tags: ["options", "pricing-models", "hmm", "quantitative-finance"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Regime-Switching Option Pricing Model

A Regime-Switching Option Pricing Model is an advanced financial model that extends traditional option pricing frameworks, such as the [Black-Scholes Model](../concepts/black-scholes-model.md), by incorporating the concept of market regimes. Unlike models that assume constant parameters (e.g., volatility), this model posits that the underlying asset's dynamics (e.g., volatility, drift) can switch between a finite number of discrete, unobservable states or "regimes."

These regime switches are governed by a [Hidden Markov Model (HMM)](../concepts/hidden-markov-model.md), where the transitions between states are probabilistic and described by a [transition matrix](../concepts/transition-matrix.md). For example, the asset's volatility ($\sigma_t$) might jump between a "low volatility" state and a "high volatility" state. The underlying asset movement within each regime is often modeled as [Geometric Brownian Motion](../concepts/geometric-brownian-motion.md).

The primary application of these models is to capture the non-stationary nature of financial markets and to price options more accurately by accounting for sudden shifts in market conditions. As detailed in [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), these models can be inverted through a calibration process using actual market option prices. This allows for the extraction of current [risk-neutral state probabilities](../concepts/risk-neutral-vs-real-world-probabilities.md) ($\Pi$) and other hidden parameters (like regime volatilities and transition probabilities), providing a forward-looking view of market regimes.