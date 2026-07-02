---
domain: "derivatives"
tags: [MMJD, jump-diffusion, gap-risk, volatility-smile, option-pricing, short-dte]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Markov-Modulated Jump-Diffusion (MMJD)

Markov-Modulated Jump-Diffusion (MMJD) is an advanced [[Hidden Markov Models (HMMs) in Option Pricing|HMM architecture]] designed to address the limitations of continuous diffusion models, particularly for short-duration options (1DTE to 7DTE) where [[gap-risk]] is a primary concern. It extends the concept of [[Markov-Modulated Geometric Brownian Motion (MMGBM)]] by incorporating a Poisson jump process, where both the frequency and magnitude of jumps are dictated by the hidden market regime.

## Dynamics

The asset price dynamics under MMJD are given by:

$$ \frac{dS_t}{S_{t-}} = \mu(Z_t) dt + \sigma(Z_t) dW_t + (e^{J(Z_t)} - 1) dN_t(Z_t) $$

## Components

*   **$dW_t$**: Represents the continuous Brownian motion, capturing standard day-to-day price fluctuations.
*   **$dN_t(Z_t)$**: A Poisson process with a state-dependent intensity $\lambda(Z_t)$. This means the arrival rate of price jumps can vary significantly between market regimes (e.g., aggressively scaled up in a "Trending/High-Vol" state).
*   **$J(Z_t)$**: The jump magnitude, which is drawn from a state-dependent probability distribution (often a normal distribution with state-specific mean and variance).

## Pricing Impact

MMJD models are crucial for generating a pronounced [[volatility-smile]] and aggressive Out-of-the-Money (OTM) skew that closely matches real-world short-duration options chains. This accuracy stems from its ability to assign a structural probability to tail-risk events, which are often underestimated by models lacking jump components. It directly addresses the challenge of pricing options exposed to sudden, discontinuous price movements.