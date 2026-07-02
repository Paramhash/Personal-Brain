yaml
---
domain: "derivatives"
tags: [stock-market-regimes, option-pricing, equity-risk-premium, hidden-markov-models, financial-crises, forecasting, horizon-spread]
created: 2022-02-01
reviewed: false
source_origin: "Detecting stock market regimes from option market prices.md"
---
# Detecting Stock Market Regimes from Option Prices

## Author
[[wan-ni-lai]]

## Date
February 1, 2022

## Abstract
This paper investigates the use of forward-looking information extracted from option prices to improve the detection of stock market regimes. It demonstrates that the "horizon spread" in option-implied equity risk premia (the difference between long-term and short-term expected risk premia) allows for earlier and sharper detection of regime switches compared to traditional methods relying on observed returns or conditional volatility. The findings hold true across significant disaster periods, such as the 2008/2009 financial crisis and the 2020 Covid pandemic, and are consistent in both US and Emerging equity markets. Furthermore, the improved regime detection translates into enhanced forecasting performance for the equity premium.

## Key Findings
*   **Improved Regime Detection**: Option-implied horizon spreads provide earlier and clearer signals of stock market regime switches (e.g., from calm to crisis) than historical returns or conditional volatility.
*   **Horizon Spread Behavior**: The horizon spread is typically positive in normal times (long-term ERP > short-term ERP) but turns negative during crises (short-term ERP > long-term ERP), reflecting investors' heightened short-term risk aversion.
*   **Forecasting Performance**: Models incorporating option-implied horizon spreads for regime detection exhibit superior out-of-sample forecasting performance for the equity risk premium.
*   **Applicability**: Results are robust across US (S&P 500) and Emerging Markets (MSCI Emerging Market index) and during major financial crises (GFC 2008-2009, Covid-19 2020).

## Methodology
1.  **Extracting Expected Equity Risk Premium (ERP)**: The paper follows Martin (2017) to estimate the expected equity risk premium from equity index options, using the lower bound derived from risk-neutral variance.
2.  **Calculating Horizon Spread**: The horizon spread (ΔHS) is defined as the difference between the long-term (180-day) and short-term (30-day) expected equity risk premium, both extracted from options.
3.  **Regime Detection**: A Hidden Markov Model (HMM) with two hidden states (expansion and contraction) is applied to the horizon spread time series. For comparison, HMMs are also applied to historical returns and conditional volatility (using a Markov-switching GARCH model).
4.  **Forecasting Application**: The different regime-switching models are used in a step-wise forecasting exercise for the future equity risk premium, comparing their Root Mean Square Forecast Error (RMSFE).

## Data
*   **Period**: January 2006 to August 2020.
*   **Sources**: CBOE Global Markets and OptionMetrics for daily options data; Refinitiv Datastream for US TBill rate and index dividend yield.
*   **Indices**: S&P 500 (US market) and MSCI Emerging Market index (EEM).
*   **Filtering**: Options with zero bid price, replicated entries, or less than 7 days to expiry are excluded. Expected risk premia are computed only if more than 3 put and call options are available for a given horizon, with linear interpolation for fixed horizons (30, 90, 180, 360 days).

## Related Concepts
*   [[stock-market-regimes]]
*   [[horizon-spread-option-implied-erp]]
*   [[equity-risk-premium]]
*   [[hidden-markov-models]]
*   [[option-implied-volatility]]

## References
The paper cites several relevant works, including:
*   Aït-Sahalia, Y., Karaman, M., & Mancini, L. (2020). The term structure of equity and variance risk premia. *Journal of Econometrics*.
*   Ang, A., & Timmermann, A. (2012). Regime changes and financial markets. *Annual Review of Financial Economics*.
*   Martin, I. (2017). What is the expected return on the market? *The Quarterly Journal of Economics*.

## JEL Codes
G01, G12

## Publisher
Elsevier

## Version of Record
https://www.sciencedirect.com/science/article/pii/S
Manuscript_90e43461f037a8a69ec252ea1872957c
---