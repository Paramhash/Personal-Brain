---
tags: ["options", "volatility", "historical_data", "risk_measurement"]
created: 2023-10-27
reviewed: false
source_origin: "../research/options_portfolio_research_guide.md"
---
# Realized Volatility

Realized Volatility (also known as historical volatility) is a measure of the actual price fluctuations of an underlying asset over a specific historical period. It is calculated from a series of past observed prices (e.g., daily closing prices, intraday prices) and represents the actual "wiggling" of the asset's price.

**Calculation:**
Realized volatility is typically calculated as the standard deviation of the asset's logarithmic returns over a given period, annualized. For example, daily returns can be used to calculate a daily standard deviation, which is then multiplied by the square root of the number of trading days in a year (e.g., $\sqrt{252}$) to get an annualized figure.

**Key Differences from Implied Volatility:**
*   **Historical vs. Forward-Looking:** Realized volatility is backward-looking, reflecting past price movements. [[../concepts/implied_volatility.md|Implied volatility]] is forward-looking, reflecting market expectations of future volatility.
*   **Direct Observation vs. Derived:** Realized volatility is directly calculated from observed prices. Implied volatility is derived from option prices using a pricing model.

**Importance in Options Trading and Research:**
*   **Benchmark for Implied Volatility:** Realized volatility serves as a benchmark against which [[../concepts/implied_volatility.md|implied volatility]] can be compared. The persistent difference between the two is known as the [[../concepts/volatility_risk_premium.md|Volatility Risk Premium (VRP)]].
*   **Model Input:** While not directly used in Black-Scholes for pricing, realized volatility can be an input for other models or for calibrating [[../concepts/stochastic_volatility_models.md|stochastic volatility models]].
*   **Performance Evaluation:** In [[../concepts/backtesting.md|backtesting]] options strategies, comparing the strategy's performance against periods of high vs. low realized volatility can provide insights into its robustness.

**See Also:**
*   [[../research/options_portfolio_research_guide.md|Guide to Options Portfolio Research]]
*   [[../concepts/implied_volatility.md|Implied Volatility]]
*   [[../concepts/volatility_risk_premium.md|Volatility Risk Premium (VRP)]]