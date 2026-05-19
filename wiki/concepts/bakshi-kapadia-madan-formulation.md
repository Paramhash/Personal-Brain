---
tags: ["finance", "quantitative-finance", "options", "derivatives-pricing", "model-independent", "moments"]
created: 2023-10-27
reviewed: false
source_origin: "/raw/gemini-code-1779191063341.py"
---
# Bakshi-Kapadia-Madan (BKM) Formulation

The **Bakshi-Kapadia-Madan (BKM) Formulation**, introduced by Gurdip Bakshi, Charles Kapadia, and Dilip Madan in 2003, provides a model-independent framework for extracting risk-neutral moments (such as variance, skewness, and kurtosis) from option prices. Similar to the [[../concepts/carr-madan-spanning-theorem.md|Carr-Madan spanning theorem]], it leverages a continuum of out-of-the-money options to replicate specific payoff functions corresponding to these moments.

## Core Idea
The BKM formulation extends the concept of option-implied moments beyond just the expected return. By constructing specific portfolios of options, it's possible to replicate payoffs that correspond to the quadratic (variance), cubic (skewness), and quartic (kurtosis) log returns of the underlying asset. This allows for a direct, market-implied measure of the shape of the [[../concepts/risk-neutral-measure.md|risk-neutral probability distribution]].

## Mathematical Formulation for Variance ($V_Q$)
The $Q$-measure variance contract payoff is defined as the quadratic log return: $H(S_T) = \left[\ln\left(\frac{S_T}{S_0}\right)\right]^2$. Its value, representing the model-independent variance ($V_Q(T)$), can be calculated as:

$$V_Q(T) = \int_{F_0}^{\infty} \frac{2\left(1 - \ln\left(\frac{K}{S_0}\right)\right)}{K^2} C(K, T) dK + \int_{0}^{F_0} \frac{2\left(1 - \ln\left(\frac{K}{S_0}\right)\right)}{K^2} P(K, T) dK$$

## Mathematical Formulation for Skewness ($W_Q$)
The $Q$-measure skewness contract ($W_Q(T)$), which isolates the asymmetry or tail risk, is given by:

$$W_Q(T) = \int_{F_0}^{\infty} \frac{3\ln\left(\frac{K}{S_0}\right)\left(2 - \ln\left(\frac{K}{S_0}\right)\right)}{K^2} C(K, T) dK - \int_{0}^{F_0} \frac{3\ln\left(\frac{K}{S_0}\right)\left(2 - \ln\left(\frac{K}{S_0}\right)\right)}{K^2} P(K, T) dK$$

Where:
*   **$F_0$** is the forward price of the underlying asset.
*   **$P(K, T)$ and $C(K, T)$** are the market prices of European puts and calls at strike $K$ and maturity $T$.
*   **$S_0$** is the current spot price of the underlying asset.

## Application in ERP Isolation
The BKM formulation is essential for [[../concepts/q-measure-equity-risk-premium-isolation.md|Q-Measure Equity Risk Premium Isolation]] because it allows for the precise, model-independent quantification of the variance and skewness components embedded in option prices. These higher-order moments are crucial for understanding the shape of the risk-neutral distribution and its implications for the [[../concepts/equity-risk-premium.md|Equity Risk Premium]].