---
tags: ["volatility", "quantitative-finance", "historical-data", "risk-measurement"]
created: 2023-10-27
reviewed: false
source_origin: "HMM-derived probability estimates compare to other methods.md"
---
# Realized Volatility (RV)

Realized Volatility (RV), also known as historical volatility, is a measure of the actual price fluctuations of an underlying asset over a specific past period. It quantifies how much the price of an asset has moved in the past, typically expressed as an annualized standard deviation of its returns.

## Calculation

RV is commonly calculated as the standard deviation of historical log returns over a defined lookback window. For example, a 10-day or 20-day annualized RV would involve:

1.  Calculating the daily log returns: $R_t = \ln(P_t / P_{t-1})$
2.  Calculating the standard deviation of these log returns over the lookback window.
3.  Annualizing the result by multiplying by the square root of the number of trading days in a year (e.g., $\sqrt{252}$).

Other methods, such as Parkinson volatility (which uses high and low prices), can also be used to estimate RV.

## Key Characteristics

*   **Backward-Looking:** RV is based purely on historical price data.
*   **Objective:** It is a direct statistical measure of past price movements, unlike [[../concepts/implied-volatility.md|implied volatility]] which is derived from market expectations.
*   **Input for Forecasting:** While backward-looking, RV is often used as a baseline or input for forecasting future volatility, assuming that past behavior can offer some indication of future trends.

## Role in Options Trading

*   **Benchmarking:** RV serves as a benchmark against which [[../concepts/implied-volatility.md|implied volatility (IV)]] is compared.
*   **[[../concepts/volatility-risk-premium-vrp.md|Volatility Risk Premium (VRP)]]:** RV is a crucial component in calculating the [[../concepts/volatility-risk-premium-vrp.md|Volatility Risk Premium (VRP)]], which is the difference between IV and RV. A positive VRP indicates that options are priced to expect more volatility than has been historically observed, which can be attractive for options sellers.
*   **Strategy Adjustment:** Traders might adjust their strategies based on the relationship between RV and IV. For instance, if RV is significantly higher than IV, it might suggest that options are relatively cheap.

## In [[../concepts/systematic-options-backtesting-pipeline.md|Systematic Options Backtesting Pipelines]]

In a [[../concepts/systematic-options-backtesting-pipeline.md|systematic options backtesting pipeline]], a Volatility & VRP Module computes rolling close-to-close log return volatility over short lookback windows (e.g., 10-day, 20-day) to capture current realized speeds. This RV is then used in conjunction with [[../concepts/implied-volatility.md|ATM IV]] to calculate the VRP, a key signal for trade entry decisions.