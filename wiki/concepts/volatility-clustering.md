---
domain: "derivatives"
tags: [volatility, market-phenomena, financial-modeling, time-series]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Volatility Clustering

Volatility clustering is a well-documented empirical phenomenon in financial markets where periods of high volatility tend to be followed by periods of high volatility, and periods of low volatility tend to be followed by periods of low volatility. In essence, volatility is not constant but rather exhibits persistence.

Standard models like Geometric Brownian Motion (GBM) fail to capture this dynamic because they assume a static volatility. Models like [[Markov-Modulated Geometric Brownian Motion (MMGBM)]] are specifically designed to account for volatility clustering by allowing market regimes to switch between different volatility levels, thus providing a more realistic representation of asset price dynamics relevant for [[Hidden Markov Models (HMMs) in Option Pricing|option pricing]].