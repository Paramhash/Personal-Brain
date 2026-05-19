---
tags: ["finance", "options", "equity_risk_premium", "forward_looking"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# Option-Implied Equity Risk Premium

## Definition
The [[../concepts/option_implied_equity_risk_premium.md|option-implied equity risk premium]] (OIERP) is an estimate of the expected excess return of an equity market index over the risk-free rate, derived from the prices of equity index [[../concepts/options.md|options]]. Unlike historical [[../concepts/equity_risk_premium.md|equity risk premium]] estimates that rely on past returns, the OIERP is considered forward-looking, as option prices reflect investors' current expectations and risk preferences regarding the future distribution of asset returns.

## Extraction Methodology
Following the work of [[../sources/martin_2017_expected_return.md|Martin (2017)]], the expected equity risk premium ($\mathbb{E}_{t}R_{T}-R_{f,t}$) for a given time horizon T can be approximated using the [[../concepts/risk_neutral_variance.md|risk-neutral variance]] of the underlying equity index returns:

$$\mathbb{E}_{t}R_{T}-R_{f,t}\gerac{1}{R_{f,t}}var_{t}^{*}R_{T}$$

where $R_{f,t}$ is the risk-free rate, and $var_{t}^{*}R_{T}$ is the conditional [[../concepts/risk_neutral_variance.md|risk-neutral variance]] of the gross return $R_T$ of the equity index. The risk-neutral variance can be non-parametrically estimated from a continuum of out-of-the-money put and call option prices. This lower bound is shown to be a sufficiently tight proxy for the expected equity risk premium.

## Forward-Looking Nature
Option prices integrate market participants' expectations about future volatility and the distribution of asset returns in a timely manner. This makes the OIERP a valuable indicator for assessing current market sentiment and anticipating future market states, as demonstrated by [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]].

## Role in Regime Detection
The OIERP, particularly when analyzed across different time horizons, provides crucial information for detecting [[../concepts/stock_market_regimes.md|stock market regimes]]. The difference between long-term and short-term OIERP, known as the [[../concepts/horizon_spread_financial.md|horizon spread]], acts as a sensitive indicator of shifts between expansion and contraction phases in the market.

## Related Concepts
*   [[../concepts/equity_risk_premium.md|Equity Risk Premium]]
*   [[../concepts/options.md|Options]]
*   [[../concepts/risk_neutral_variance.md|Risk-Neutral Variance]]
*   [[../concepts/horizon_spread_financial.md|Horizon Spread (Financial)]]
*   [[../concepts/stock_market_regimes.md|Stock Market Regimes]]
*   [[../concepts/stochastic_discount_factor.md|Stochastic Discount Factor]]

---