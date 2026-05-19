---
tags: ["finance", "options", "equity_risk_premium", "market_indicators"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# Horizon Spread (Financial)

## Definition
The [[../concepts/horizon_spread_financial.md|horizon spread]] in a financial context, particularly as defined by [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]], refers to the difference between the long-term and short-term expected [[../concepts/equity_risk_premium.md|equity risk premium]] extracted from [[../concepts/options.md|option prices]]. It is calculated as:

$$\Delta_{HS_{i,t}} = E[R_{i,t}]_L - E[R_{i,t}]_S$$

Where:
*   $\Delta_{HS_{i,t}}$ is the horizon spread for market $i$ at time $t$.
*   $E[R_{i,t}]_{L}$ is the long-term expected risk premium (e.g., from options with 180 days to maturity).
*   $E[R_{i,t}]_{S}$ is the short-term expected risk premium (e.g., from options with 30 days to maturity).

## Behavior in Different Regimes
*   **Normal Times (Expansion Regime):** In line with classic [[../concepts/asset_pricing.md|asset pricing models]] like [[../sources/campbell_cochrane_1999_habit_formation.md|habit formation]] and [[../sources/bansal_yaron_2004_long_run_risk.md|long-run risk]], investors typically require a higher long-term return to compensate for long-run risks. Thus, the [[../concepts/horizon_spread_financial.md|horizon spread]] is expected to be **positive**.
*   **Crisis Periods (Contraction Regime):** During periods of high imminent risk (e.g., financial crises, pandemics), the short-term required return may exceed the long-term required return, as investors demand higher compensation for immediate uncertainty. In these periods, the [[../concepts/horizon_spread_financial.md|horizon spread]] is expected to turn **negative**.

## Significance as a Regime Indicator
The distinct behavior of the [[../concepts/horizon_spread_financial.md|horizon spread]] across different market states makes it a powerful forward-looking indicator for detecting [[../concepts/stock_market_regimes.md|stock market regimes]]. Research shows that using the horizon spread in [[../concepts/hidden_markov_model.md|Hidden Markov Models]] provides:
*   **Earlier Detection:** It can signal regime shifts sooner than indicators based on historical returns or conditional volatility.
*   **Sharper Distinction:** It leads to clearer probabilities of being in a specific regime, reducing the "indecisive gray area" where probabilities are neither close to zero nor one.
*   **Improved Forecasting:** Models incorporating the horizon spread demonstrate better out-of-sample forecasting performance for the [[../concepts/equity_risk_premium.md|equity risk premium]].

## Related Concepts
*   [[../concepts/option_implied_equity_risk_premium.md|Option-Implied Equity Risk Premium]]
*   [[../concepts/equity_risk_premium.md|Equity Risk Premium]]
*   [[../concepts/stock_market_regimes.md|Stock Market Regimes]]
*   [[../concepts/regime_switching_models.md|Regime Switching Models]]
*   [[../concepts/options.md|Options]]
*   [[../concepts/hidden_markov_model.md|Hidden Markov Model]]

---