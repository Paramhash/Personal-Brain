---
tags: ["finance", "investing", "risk", "returns"]
created: 2023-10-27
reviewed: false
source_origin: "detecting_stock_market_regimes.md"
---
# Equity Risk Premium (ERP)

## Definition
The [[../concepts/equity_risk_premium.md|equity risk premium]] (ERP) is the excess return that an individual stock or the overall stock market is expected to deliver over a risk-free rate. It represents the additional compensation investors demand for taking on the higher risk associated with equity investments compared to a risk-free asset (like government bonds or T-bills).

## Calculation
The ERP can be expressed as:
$$ERP = \mathbb{E}[R_{equity}] - R_{f}$$
Where:
*   $\mathbb{E}[R_{equity}]$ is the expected return on the equity market.
*   $R_{f}$ is the risk-free rate.

## Types of ERP
1.  **Historical ERP:** Calculated based on the historical difference between actual equity market returns and risk-free rates over a long period. While easy to compute, it assumes past performance is indicative of future returns, which may not always hold.
2.  **Forward-Looking ERP:** Estimates of the ERP based on current market data and investor expectations. This can be derived from:
    *   **Dividend Discount Models:** Using current stock prices, expected dividends, and growth rates.
    *   **Survey Data:** Polling financial professionals for their expectations.
    *   **[[../concepts/option_implied_equity_risk_premium.md|Option-Implied Equity Risk Premium (OIERP)]]:** Derived from [[../concepts/options.md|option prices]], which reflect market participants' forward-looking expectations about volatility and return distributions. This method is highlighted in research like [[../sources/detecting_stock_market_regimes_lai_2022.md|Lai (2022)]] and [[../sources/martin_2017_expected_return.md|Martin (2017)]].

## Importance
*   **[[../concepts/asset_pricing.md|Asset Pricing]]:** A fundamental component in asset pricing models, influencing the required rate of return for equity investments.
*   **Investment Decisions:** Crucial for investors and portfolio managers in making [[../concepts/asset_allocation.md|asset allocation]] decisions and evaluating investment opportunities.
*   **Economic Forecasting:** Changes in the ERP can signal shifts in market sentiment and economic outlook.

## Horizon Effects
The ERP can vary with the investment horizon. Classic [[../concepts/asset_pricing.md|asset pricing models]] (e.g., [[../sources/campbell_cochrane_1999_habit_formation.md|habit formation]], [[../sources/bansal_yaron_2004_long_run_risk.md|long-run risk]]) often predict a higher ERP for longer horizons. However, during crisis periods, the short-term ERP can temporarily exceed the long-term ERP due to heightened immediate risk, leading to a negative [[../concepts/horizon_spread_financial.md|horizon spread]].

## Related Concepts
*   [[../concepts/option_implied_equity_risk_premium.md|Option-Implied Equity Risk Premium]]
*   [[../concepts/horizon_spread_financial.md|Horizon Spread (Financial)]]
*   [[../concepts/risk_free_rate.md|Risk-Free Rate]]
*   [[../concepts/asset_pricing.md|Asset Pricing]]
*   [[../concepts/stock_market_regimes.md|Stock Market Regimes]]
*   [[../concepts/options.md|Options]]

---