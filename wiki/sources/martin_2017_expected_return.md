---
tags: ["finance", "equity_risk_premium", "options", "asset_pricing"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# What is the Expected Return on the Market? (Martin, 2017)

**Author:** Ian Martin
**Publication Year:** 2017
**Journal:** *The Quarterly Journal of Economics*

## Summary
This seminal paper by [[../entities/ian_martin.md|Ian Martin]] demonstrates a method to estimate the expected [[../concepts/equity_risk_premium.md|equity risk premium]] from [[../concepts/options.md|equity index options]]. Martin shows that the expected equity risk premium can be expressed as a lower bound related to the [[../concepts/risk_neutral_variance.md|risk-neutral variance]] of the market's return, scaled by the risk-free rate.

## Key Contribution
The paper establishes that the term $rac{1}{R_{f,t}}var_{t}^{*}R_{T}$ (where $R_{f,t}$ is the risk-free rate and $var_{t}^{*}R_{T}$ is the conditional [[../concepts/risk_neutral_variance.md|risk-neutral variance]] of the market's gross return) provides a sufficiently tight lower bound for the expected [[../concepts/equity_risk_premium.md|equity risk premium]]. This allows for a forward-looking estimation of the [[../concepts/equity_risk_premium.md|equity risk premium]] directly from [[../concepts/options.md|option prices]], which reflect market participants' expectations.

## Impact
This methodology has been widely adopted in subsequent research, including [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]], to extract [[../concepts/option_implied_equity_risk_premium.md|option-implied equity risk premia]] for various applications, such as detecting [[../concepts/stock_market_regimes.md|stock market regimes]].

## Related Concepts
*   [[../concepts/equity_risk_premium.md|Equity Risk Premium]]
*   [[../concepts/option_implied_equity_risk_premium.md|Option-Implied Equity Risk Premium]]
*   [[../concepts/options.md|Options]]
*   [[../concepts/risk_neutral_variance.md|Risk-Neutral Variance]]
*   [[../concepts/stochastic_discount_factor.md|Stochastic Discount Factor]]
*   [[../concepts/asset_pricing.md|Asset Pricing]]

---