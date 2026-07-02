---
domain: "derivatives"
tags: [gap-risk, market-risk, option-pricing, short-dte, tail-risk]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Gap Risk

Gap risk refers to the potential for sudden, discontinuous jumps in asset prices, often occurring overnight or during periods of significant news. These price gaps are not captured by continuous diffusion processes like those in Geometric Brownian Motion (GBM) or even [[Markov-Modulated Geometric Brownian Motion (MMGBM)]].

For short-duration options (1DTE to 7DTE), gap risk is a primary threat, especially for short premium strategies like Iron Condors, where a sudden move can lead to significant losses. To accurately price options and manage risk in such scenarios, models must explicitly account for these discontinuous jumps. The [[Markov-Modulated Jump-Diffusion (MMJD)]] architecture is specifically designed to address gap risk by incorporating a Poisson jump process, allowing for structural probabilities of tail-risk events.