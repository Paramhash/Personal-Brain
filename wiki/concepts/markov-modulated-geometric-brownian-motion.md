---
domain: "derivatives"
tags: [MMGBM, regime-switching, geometric-brownian-motion, volatility-clustering, option-pricing]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Markov-Modulated Geometric Brownian Motion (MMGBM)

Markov-Modulated Geometric Brownian Motion (MMGBM) is a foundational [[Hidden Markov Models (HMMs) in Option Pricing|regime-switching model]] that extends the standard Geometric Brownian Motion (GBM) by allowing its parameters to be governed by a hidden continuous-time Markov chain ($Z_t$). It is often referred to as the Regime-Switching Black-Scholes model.

## Dynamics

The underlying asset price $S_t$ follows a diffusion process where the drift $\mu$ and, crucially, the volatility $\sigma$ are dependent on the hidden market regime $Z_t$:

$$ \frac{dS_t}{S_t} = \mu(Z_t) dt + \sigma(Z_t) dW_t $$

## How it Works

The market transitions between a finite number of discrete states (e.g., $Z_t \in \{1, 2\}$ for a "Low Volatility" state and a "High Volatility" state). In each state, the model parameters, such as volatility ($\sigma_1 = 12\%$ in State 1, $\sigma_2 = 30\%$ in State 2), are distinct.

## Pricing Impact

Instead of a single Black-Scholes calculation, option pricing under MMGBM becomes a system of coupled Partial Differential Equations (PDEs). This model is excellent for capturing [[volatility-clustering]], which is the tendency for periods of high volatility to follow high volatility, and vice versa. However, because it relies purely on continuous diffusion, it still tends to underprice [[gap-risk]] (sudden, discontinuous price jumps), especially relevant for short-duration options.