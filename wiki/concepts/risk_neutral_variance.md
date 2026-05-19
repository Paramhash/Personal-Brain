---
tags: ["finance", "options", "derivatives", "risk_management"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# Risk-Neutral Variance

## Definition
[[../concepts/risk_neutral_variance.md|Risk-neutral variance]] (also known as implied variance or implied volatility squared) is a measure of the expected variance of an underlying asset's returns, derived from the prices of its [[../concepts/options.md|options]] under a risk-neutral probability measure. In a risk-neutral world, all assets are expected to grow at the risk-free rate, and investors are indifferent to risk.

## Distinction from Real-World Variance
*   **Real-World (Physical) Variance:** Reflects the actual expected variance of returns under the true probability measure, incorporating investors' risk aversion.
*   **Risk-Neutral Variance:** Reflects the expected variance under a hypothetical risk-neutral measure. It is "implied" by option prices and incorporates a risk premium for volatility.

## Extraction from Option Prices
The [[../concepts/risk_neutral_variance.md|risk-neutral variance]] can be estimated non-parametrically from a continuum of out-of-the-money put and call option prices across different strike prices and maturities. This process involves integrating option prices to reconstruct the risk-neutral probability distribution of the underlying asset's future price.

## Role in Option-Implied Equity Risk Premium
As shown by [[../sources/martin_2017_expected_return.md|Martin (2017)]] and utilized in [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]], the [[../concepts/risk_neutral_variance.md|risk-neutral variance]] plays a crucial role in estimating the lower bound of the [[../concepts/option_implied_equity_risk_premium.md|option-implied equity risk premium]] (OIERP). Specifically, the term $rac{1}{R_{f,t}}var_{t}^{*}R_{T}$ (where $R_{f,t}$ is the risk-free rate and $var_{t}^{*}R_{T}$ is the risk-neutral variance of the gross return) serves as a tight proxy for the OIERP.

## Significance
*   **Forward-Looking Indicator:** Since it's derived from current option prices, [[../concepts/risk_neutral_variance.md|risk-neutral variance]] provides a forward-looking measure of market expectations regarding future volatility.
*   **Market Sentiment:** Changes in [[../concepts/risk_neutral_variance.md|risk-neutral variance]] (or implied volatility) often reflect shifts in market sentiment and perceived risk.
*   **Regime Detection:** As a component of the OIERP and subsequently the [[../concepts/horizon_spread_financial.md|horizon spread]], it indirectly contributes to the detection of [[../concepts/stock_market_regimes.md|stock market regimes]].

## Related Concepts
*   [[../concepts/options.md|Options]]
*   [[../concepts/option_implied_equity_risk_premium.md|Option-Implied Equity Risk Premium]]
*   [[../concepts/implied_volatility.md|Implied Volatility]]
*   [[../concepts/equity_risk_premium.md|Equity Risk Premium]]
*   [[../concepts/stochastic_discount_factor.md|Stochastic Discount Factor]]

---