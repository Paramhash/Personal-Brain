---
tags: ["finance", "investing", "risk", "premium", "equity", "erp"]
created: 2023-10-27
reviewed: false
source_origin: "/raw/gemini-code-1779191063341.py"
---
# Equity Risk Premium (ERP)

The **Equity Risk Premium (ERP)** is the excess return that investing in the stock market provides over a risk-free rate. It represents the additional compensation investors demand for taking on the higher risk associated with equity investments compared to a risk-free asset (like government bonds).

## Definition
The ERP can be broadly defined as:
$$\text{ERP} = \text{Expected Return on Equity} - \text{Risk-Free Rate}$$

In the context of quantitative finance and option pricing, the ERP at a specific maturity $T$ is more precisely defined by the difference between the expected asset return under the [[../concepts/physical-measure.md|physical measure]] ($P$-measure) and the [[../concepts/risk-neutral-measure.md|risk-neutral measure]] ($Q$-measure):

$$\text{ERP}_T = E^P\left[\ln\left(\frac{S_T}{S_0}\right)\right] - E^Q\left[\ln\left(\frac{S_T}{S_0}\right)\right]$$

## Importance
*   **Investment Decisions**: A higher ERP suggests that equities are more attractive relative to risk-free assets, potentially signaling a good time to invest in stocks.
*   **Valuation**: Used in various valuation models, such as the Capital Asset Pricing Model (CAPM) and Discounted Cash Flow (DCF) models, to determine the cost of equity.
*   **Market Sentiment**: Changes in the implied ERP (derived from option markets) can reflect shifts in market participants' risk aversion and expectations.

## Isolation via Q-Measure
The process of [[../concepts/q-measure-equity-risk-premium-isolation.md|Q-Measure Equity Risk Premium Isolation]] focuses on extracting the $Q$-measure component of the ERP from option prices, allowing for a model-independent assessment of market-implied risk. This involves using techniques like the [[../concepts/carr-madan-spanning-theorem.md|Carr-Madan spanning theorem]] and the [[../concepts/bakshi-kapadia-madan-formulation.md|Bakshi-Kapadia-Madan formulation]] to derive risk-neutral moments.