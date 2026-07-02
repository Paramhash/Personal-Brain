---
domain: "derivatives"
tags: [MS-SV, stochastic-volatility, regime-switching, volatility-term-structure, option-pricing]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Markov-Switching Stochastic Volatility (MS-SV)

Markov-Switching Stochastic Volatility (MS-SV) models, such as Regime-Switching Heston, represent an institutional-grade [[Hidden Markov Models (HMMs) in Option Pricing|HMM architecture]] for option pricing. While HMMs allow for discrete jumps in volatility, MS-SV models recognize that true market volatility is continuously shifting. They combine a continuous stochastic volatility process with discrete hidden states, offering a highly flexible framework for fitting the volatility surface.

## Dynamics

The dynamics of the asset price $S_t$ and its variance $V_t$ are given by:

$$ \frac{dS_t}{S_t} = \mu(Z_t) dt + \sqrt{V_t} dW_t^S $$

$$ dV_t = \kappa(Z_t) (\theta(Z_t) - V_t) dt + \xi(Z_t) \sqrt{V_t} dW_t^V $$

## How it Works

In MS-SV models, the variance $V_t$ diffuses continuously, but its structural parameters are modulated by the hidden state $Z_t$. These parameters include:

*   **Mean reversion speed $\kappa(Z_t)$**: How quickly volatility reverts to its long-term mean.
*   **Long-term variance level $\theta(Z_t)$**: The equilibrium level of variance.
*   **Vol-of-vol $\xi(Z_t)$**: The volatility of the variance process itself.

For example, in a "Crash" state, the mean-reversion level $\theta$ might instantly spike, causing near-term implied volatility to explode relative to back-month volatility.

## Pricing Impact

This architecture allows the term structure of volatility to shift dynamically and realistically. MS-SV models are highly effective at capturing the complex behavior of implied volatility surfaces, including the [[volatility-smile]] and term structure dynamics, making them a powerful tool for sophisticated option traders and risk managers.