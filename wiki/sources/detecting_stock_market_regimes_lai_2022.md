---
tags: ["finance", "stock_market", "regime_switching", "options", "equity_risk_premium", "forecasting", "hidden_markov_model"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# Detecting Stock Market Regimes from Option Prices

**Author:** [[../entities/wan_ni_lai.md|Wan Ni Lai]]
**Publication Date:** February 1, 2022
**Journal/Publisher:** Elsevier
**JEL Codes:** G01, G12

## Abstract
This paper investigates the use of forward-looking information extracted from option prices to improve the detection of [[../concepts/stock_market_regimes.md|stock market regimes]]. Traditional [[../concepts/regime_switching_models.md|regime switching models]] often rely on historical observed returns, potentially overlooking valuable investor expectations. Lai demonstrates that "horizon spreads" in [[../concepts/option_implied_equity_risk_premium.md|option-implied equity risk premia]] allow for earlier and sharper detection of regime switches, as well as improved prediction of the [[../concepts/equity_risk_premium.md|equity premium]].

The findings are robust across significant market events, including the 2008/2009 global financial crisis and the 2020 Covid-19 pandemic, and hold for both US (S&P 500) and [[../entities/msci_emerging_market_index.md|Emerging Markets]] (MSCI Emerging Market Index).

## Key Contributions:
*   **Novel Indicator:** Introduces the [[../concepts/horizon_spread_financial.md|horizon spread]] (difference between long-term and short-term option-implied equity risk premia) as a superior indicator for regime detection.
*   **Improved Detection:** Shows that the horizon spread enables earlier and sharper identification of market regime shifts compared to indicators based on historical returns or conditional volatility.
*   **Enhanced Forecasting:** Demonstrates that [[../concepts/regime_switching_models.md|regime switching models]] incorporating the horizon spread lead to better out-of-sample forecasts of the [[../concepts/equity_risk_premium.md|equity risk premium]], as measured by [[../concepts/root_mean_square_forecast_error.md|RMSFE]].
*   **Empirical Evidence:** Provides evidence from two major crisis periods (GFC and Covid-19) across developed and emerging markets, highlighting the forward-looking nature of option prices.

## Methodology:
1.  **Extraction of Expected Equity Risk Premium:** Utilizes the framework by [[../sources/martin_2017_expected_return.md|Martin (2017)]] to estimate the expected equity risk premium from equity index options, leveraging the [[../concepts/risk_neutral_variance.md|risk-neutral variance]].
2.  **Calculation of Horizon Spread:** Defines the horizon spread as the difference between the 180-day (long-term) and 30-day (short-term) option-implied expected risk premia.
3.  **Regime Detection:** Employs a [[../concepts/hidden_markov_model.md|Hidden Markov Model]] (HMM) with two states (expansion and contraction) to detect regime shifts, using the horizon spread as the primary input. For comparison, HMMs are also estimated using observed returns and conditional volatility (Markov switching GARCH).
4.  **Forecasting Application:** Compares the out-of-sample forecasting performance of the equity risk premium using different regime indicators within a step-wise model selection approach, building on [[../sources/campbell_thompson_2008_predicting_excess_returns.md|Campbell and Thompson (2008)]] and [[../sources/guidolin_pedio_2021_forecasting_commodity_futures.md|Guidolin and Pedio (2021)]].

## Key Findings:
*   During normal periods, the long-term expected equity risk premium is generally higher than the short-term, consistent with models like [[../sources/campbell_cochrane_1999_habit_formation.md|Campbell and Cochrane (1999)]] and [[../sources/bansal_yaron_2004_long_run_risk.md|Bansal and Yaron (2004)]].
*   During crisis periods (GFC, Covid-19), this pattern reverses, with the short-term premium exceeding the long-term premium, and the horizon spread turning significantly negative.
*   The horizon spread yields sharper regime distinctions (lower "indecisive gray area" probabilities) and better model fit (lower [[../concepts/aic_bic_information_criteria.md|AIC and BIC]]) compared to models based on historical returns or conditional volatility.
*   The horizon spread indicator detected the Covid-19 contraction regime in emerging markets as early as December 2019, months before historical returns indicated a shift.
*   In a forecasting exercise, the horizon spread model consistently produced the lowest [[../concepts/root_mean_square_forecast_error.md|RMSFE]] for predicting the equity risk premium in both US and emerging markets.

## Data:
*   **Options Data:** Daily data from [[../entities/cboe_global_markets.md|CBOE Global Markets]] and [[../entities/optionmetrics.md|OptionMetrics]].
*   **Risk-Free Rate & Dividend Yield:** [[../entities/refinitiv_datastream.md|Refinitiv Datastream]].
*   **Equity Indexes:** [[../entities/sp_500_index.md|S&P 500]] (US) and [[../entities/msci_emerging_market_index.md|MSCI Emerging Market Index]] (EEM).
*   **Sample Period:** January 2006 to August 2020.

## Related Concepts:
*   [[../concepts/stock_market_regimes.md|Stock Market Regimes]]
*   [[../concepts/regime_switching_models.md|Regime Switching Models]]
*   [[../concepts/option_implied_equity_risk_premium.md|Option-Implied Equity Risk Premium]]
*   [[../concepts/horizon_spread_financial.md|Horizon Spread (Financial)]]
*   [[../concepts/hidden_markov_model.md|Hidden Markov Model]]
*   [[../concepts/equity_risk_premium.md|Equity Risk Premium]]
*   [[../concepts/risk_neutral_variance.md|Risk-Neutral Variance]]
*   [[../concepts/aic_bic_information_criteria.md|AIC and BIC Information Criteria]]
*   [[../concepts/root_mean_square_forecast_error.md|Root Mean Square Forecast Error (RMSFE)]]

## Cited Works:
*   [[../sources/martin_2017_expected_return.md|Martin (2017)]]
*   [[../sources/bansal_yaron_2004_long_run_risk.md|Bansal and Yaron (2004)]]
*   [[../sources/campbell_cochrane_1999_habit_formation.md|Campbell and Cochrane (1999)]]
*   [[../sources/campbell_thompson_2008_predicting_excess_returns.md|Campbell and Thompson (2008)]]
*   [[../sources/guidolin_pedio_2021_forecasting_commodity_futures.md|Guidolin and Pedio (2021)]]

---