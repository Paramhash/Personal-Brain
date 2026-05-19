---
tags: ["finance", "quantitative-finance", "options", "derivatives-pricing", "spanning", "model-independent"]
created: 2023-10-27
reviewed: false
source_origin: "/raw/gemini-code-1779191063341.py"
---
# Carr-Madan Spanning Theorem

The **Carr-Madan Spanning Theorem**, developed by Peter Carr and Dilip Madan, is a foundational result in financial mathematics that provides a model-independent way to replicate any twice-differentiable payoff function using a continuum of out-of-the-money (OTM) European call and put options, along with the underlying asset and a risk-free bond.

## Core Idea
The theorem demonstrates that the price of any derivative whose payoff depends solely on the underlying asset's price at maturity can be expressed as an integral of market option prices. This is particularly powerful because it does not require assuming a specific parametric model for asset price dynamics (e.g., Black-Scholes).

## Mathematical Formulation
For a payoff function $H(S_T)$, its risk-neutral expectation can be replicated. When the payoff is set to the log contract, $H(S_T) = \ln(S_T)$, the risk-neutral expectation of the log return can be integrated directly from OTM market option prices:

$$E^Q\left[\ln\left(\frac{S_T}{S_0}\right)\right] = e^{rT}\left[ \frac{S_0}{F_0} - 1 - \int_{0}^{F_0} \frac{1}{K^2} P(K, T) dK - \int_{F_0}^{\infty} \frac{1}{K^2} C(K, T) dK \right]$$

Where:
*   **$F_0 = S_0 e^{(r-d)T}$** is the forward price of the underlying asset at maturity $T$.
*   **$P(K, T)$ and $C(K, T)$** are the market prices of European puts and calls at strike $K$ and maturity $T$.
*   **$r$** is the risk-free rate and **$d$** is the continuous dividend yield.

## Application in ERP Isolation
This theorem is crucial for [[../concepts/q-measure-equity-risk-premium-isolation.md|Q-Measure Equity Risk Premium Isolation]] as it allows for the model-independent extraction of the [[../concepts/risk-neutral-measure.md|Q-measure]] expected log return directly from observed option prices, without relying on assumptions about the underlying asset's price distribution. This provides a robust way to quantify market expectations embedded in the option surface.