---
tags: ["finance", "quantitative-finance", "options", "pricing", "risk-neutral", "q-measure"]
created: 2023-10-27
reviewed: false
source_origin: "/raw/gemini-code-1779191063341.py"
---
# Risk-Neutral Measure (Q-Measure)

The **Risk-Neutral Measure**, often denoted as the **$Q$-measure**, is a fundamental concept in financial mathematics, particularly in the pricing of derivatives. It is a theoretical probability measure under which the expected return of any asset is equal to the risk-free rate. This means that all assets, when discounted at the risk-free rate, have the same expected value.

## Key Characteristics:
*   **Expected Return**: Under the $Q$-measure, the expected return of any tradable asset is the risk-free rate. This simplifies pricing as it removes the need to estimate individual asset risk premia.
*   **Martingale Property**: Discounted asset prices are martingales under the $Q$-measure.
*   **No Arbitrage**: The existence of a risk-neutral measure is equivalent to the absence of arbitrage opportunities in a complete market.
*   **Derivative Pricing**: It is primarily used for pricing derivatives, as the price of a derivative can be calculated as its expected future payoff under the $Q$-measure, discounted at the risk-free rate.

## Relation to Equity Risk Premium
In the context of [[../concepts/q-measure-equity-risk-premium-isolation.md|Q-Measure Equity Risk Premium Isolation]], the $Q$-measure expected log return is a key component. The difference between the expected return under the [[../concepts/physical-measure.md|physical measure]] ($P$-measure) and the $Q$-measure forms the basis of the [[../concepts/equity-risk-premium.md|Equity Risk Premium]].

The expected log return under the $Q$-measure is given by:
$$E^Q\left[\ln\left(\frac{S_T}{S_0}\right)\right] = (r - d)T - \frac{1}{2}V_Q(T)$$
Where $r$ is the risk-free rate, $d$ is the continuous dividend yield, and $V_Q(T)$ is the $Q$-measure model-independent total variance.