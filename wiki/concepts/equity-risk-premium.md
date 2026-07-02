yaml
---
domain: "derivatives"
tags: [asset-pricing, expected-returns, option-pricing, risk-compensation, financial-markets]
created: 2024-07-30
reviewed: false
source_origin: "Detecting stock market regimes from option prices.md"
---
# Equity Risk Premium (ERP)

## Definition
The Equity Risk Premium (ERP) is the excess return that an individual stock or the overall stock market is expected to deliver over a risk-free rate. It represents the compensation investors demand for bearing the higher risk associated with equity investments compared to risk-free assets like government bonds.

## Estimation from Option Prices
Traditionally, ERP is estimated using historical data or dividend discount models. However, a forward-looking measure of the ERP can be extracted from equity index option prices. Martin (2017) demonstrated that the expected equity risk premium can be approximated by a lower bound derived from the conditional risk-neutral variance of the underlying equity index.

The formula for this lower bound is:
`Et[RT - Rf,t] ≥ (1/Rf,t) * var*t(RT)`
Where:
*   `Et[RT - Rf,t]` is the expected equity risk premium at time `t` for horizon `T`.
*   `Rf,t` is the risk-free rate.
*   `var*t(RT)` is the conditional risk-neutral variance of the gross return `RT`, which can be estimated non-parametrically from a continuum of out-of-the-money put and call option prices.

This option-implied ERP provides a timely and forward-looking measure of investor expectations.

## Short-Term vs. Long-Term ERP
The ability to extract ERP for different time horizons (e.g., 30 days, 180 days) from options provides an additional dimension of information.
*   **Classic Asset Pricing Models**: Models like the habit formation model (Campbell and Cochrane, 1999) and the long-run risk model (Bansal and Yaron, 2004) predict that the long-term ERP should be higher than the short-term ERP, compensating investors for long-run risks.
*   **Crisis Periods**: During financial crises, this relationship can reverse. The short-term ERP may exceed the long-term ERP, reflecting exceptionally high imminent risk and investors' demand for greater compensation for immediate uncertainty, expecting risks to abate over longer horizons. This phenomenon is central to the concept of the [[horizon-spread-option-implied-erp|horizon spread]].

## Role in Regime Detection and Forecasting
The option-implied ERP, particularly its horizon structure, is a powerful indicator for [[stock-market-regimes|stock market regime]] detection. Research by [[wan-ni-lai]] (2022) shows that the [[horizon-spread-option-implied-erp|horizon spread]] derived from these option-implied ERPs offers superior performance in:
*   **Detecting Regime Shifts**: Providing earlier and sharper signals of transitions between expansion and contraction regimes.
*   **Forecasting Equity Premium**: Improving the accuracy of future equity premium forecasts.

## Related Concepts
*   [[horizon-spread-option-implied-erp]]
*   [[stock-market-regimes]]
*   [[option-implied-volatility]]
*   [[detecting-stock-market-regimes-from-option-prices-lai-2022|Detecting Stock Market Regimes from Option Prices (Lai, 2022)]]
---