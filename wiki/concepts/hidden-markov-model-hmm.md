---
tags: ["quantitative finance", "statistical modeling", "market regimes", "hidden markov models"]
created: 2023-10-27
reviewed: false
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
---
# Hidden Markov Model (HMM) in Finance

A Hidden Markov Model (HMM) is a statistical Markov model in which the system being modeled is assumed to be a Markov process with unobserved (hidden) states. It is used to model systems where the observed data depends on an underlying, unobservable state.

In finance, HMMs are frequently applied to identify and classify market regimes based on observable data like price movements, returns, or volatility. For example, an HMM might classify the market into states such as "bull market," "bear market," "high volatility," or "low volatility," even though these states are not directly observable.

## Application in the Structural Triad:

Within the [[../concepts/structural-triad-systematic-options-trading.md|Structural Triad for Advanced Systematic Options Trading]], HMMs are likely used to classify the current market regime. This classification provides a crucial contextual layer for interpreting the signals derived from [[../concepts/gamma-exposure-gex-profile.md|GEX profiles]] and [[../concepts/implied-historical-volatility-skew.md|IV-HV skew]], allowing systematic strategies to adapt to the prevailing market environment.

## Further Research:

Explore specific HMM architectures, input features (e.g., returns, volatility, volume), and training methodologies relevant for financial time series analysis and options trading context. Investigate how different market regimes identified by HMMs influence the effectiveness of various options strategies.

---