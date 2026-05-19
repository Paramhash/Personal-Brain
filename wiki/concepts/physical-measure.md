---
tags: ["finance", "quantitative-finance", "risk-management", "p-measure", "real-world-probability"]
created: 2023-10-27
reviewed: false
source_origin: "/raw/gemini-code-1779191063341.py"
---
# Physical Measure (P-Measure)

The **Physical Measure**, often denoted as the **$P$-measure**, represents the actual, real-world probability distribution of asset prices. It is the probability measure under which investors make decisions, reflecting their true expectations about future asset movements and their attitudes towards risk.

## Key Characteristics:
*   **Real-World Probabilities**: Reflects the actual likelihood of various outcomes in the market.
*   **Expected Returns**: Under the $P$-measure, assets are expected to earn a return greater than the risk-free rate, incorporating a [[../concepts/equity-risk-premium.md|risk premium]] to compensate investors for bearing risk.
*   **Statistical Inference**: Used for statistical analysis, forecasting, and risk management, as it describes the actual dynamics of asset prices.

## Relation to Equity Risk Premium
The $P$-measure is crucial for defining the [[../concepts/equity-risk-premium.md|Equity Risk Premium (ERP)]]. The ERP is the difference between the expected return of an asset under the $P$-measure and its expected return under the [[../concepts/risk-neutral-measure.md|risk-neutral measure]] ($Q$-measure).

$$\text{ERP}_T = E^P\left[\ln\left(\frac{S_T}{S_0}\right)\right] - E^Q\left[\ln\left(\frac{S_T}{S_0}\right)\right]$$

Understanding the divergence between $P$-measure expectations (often derived from historical data or economic models) and $Q$-measure expectations (derived from option prices) is central to frameworks like [[../concepts/q-measure-equity-risk-premium-isolation.md|Q-Measure Equity Risk Premium Isolation]].