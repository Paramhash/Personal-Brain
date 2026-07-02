---
domain: "derivatives"
tags: [FFT, numerical-methods, option-pricing, computational-finance, characteristic-function, carr-madan]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Fast Fourier Transform (FFT) in Option Pricing

The Fast Fourier Transform (FFT) is a highly efficient algorithm used in computational finance for pricing options, particularly when dealing with complex models that do not have closed-form solutions. It is a cornerstone for solving models like [[Markov-Modulated Jump-Diffusion (MMJD)]] and [[Markov-Switching Stochastic Volatility (MS-SV)]].

## Application

These advanced models often define the characteristic function of the log-price as a matrix Riccati differential equation. Pricing options using these characteristic functions cannot be done with simple algebraic formulas. Instead, the FFT, notably through the **Carr-Madan formula**, allows for the efficient computation of option prices across an entire range of strike prices simultaneously.

## Computational Advantage

Calculating the FFT involves computing complex matrix exponentials. A significant advantage of using FFT for option pricing is its high parallelizability. This means that evaluating an entire option chain can be distributed across multiple processor cores (e.g., a 64-core processor), enabling near-instantaneous calibration of jump-diffusion or stochastic volatility parameters across the entire volatility surface. This capability transforms what might traditionally be a delayed end-of-day risk report into a live, intraday execution filter, providing critical real-time insights for traders.