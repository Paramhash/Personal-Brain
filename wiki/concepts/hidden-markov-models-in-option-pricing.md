---
domain: "derivatives"
tags: [HMM, option-pricing, volatility-modeling, regime-switching, short-dte, financial-modeling]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Hidden Markov Models (HMMs) in Option Pricing

Standard financial models like Geometric Brownian Motion (GBM) often fall short in accurately pricing options, particularly those with short durations (1DTE to 7DTE) where gamma sensitivity is extreme. GBM assumes a static market environment, failing to capture dynamic market phenomena.

Hidden Markov Models (HMMs) offer a more sophisticated approach by introducing a continuous-time hidden state ($Z_t$) that represents the underlying market regime. This allows for the construction of architectures capable of accurately mapping complex market behaviors such as [[volatility-clustering]], [[gap-risk]], and the [[volatility-smile]].

## Key Architectures

Here are the three foundational HMM architectures used in advanced options pricing, ordered by complexity and empirical accuracy:

1.  **[[Markov-Modulated Geometric Brownian Motion (MMGBM)]]**: The regime-switching baseline, extending GBM with state-dependent parameters.
2.  **[[Markov-Modulated Jump-Diffusion (MMJD)]]**: Essential for short-duration options, incorporating state-dependent jump processes to capture discontinuous price movements.
3.  **[[Markov-Switching Stochastic Volatility (MS-SV)]]**: An institutional-grade model that combines continuous stochastic volatility with discrete hidden states to fit the volatility surface dynamically.

## Solving HMM Architectures

Pricing options under complex HMM architectures like MMJD or MS-SV typically requires numerical methods. The [[Fast Fourier Transform (FFT) in Option Pricing]] (e.g., the Carr-Madan formula) is a common technique, leveraging the characteristic function of the log-price, often defined by matrix Riccati differential equations. The parallelizable nature of FFT calculations makes it suitable for real-time calibration of model parameters.