yaml
---
domain: "derivatives"
tags: [equity-risk-premium, option-pricing, forward-looking-indicators, regime-detection, financial-crises]
created: 2024-07-30
reviewed: false
source_origin: "Detecting stock market regimes from option prices.md"
---
# Horizon Spread (Option-Implied Equity Risk Premium)

## Definition
The Horizon Spread (ΔHS) in the context of option-implied equity risk premium (ERP) is defined as the difference between the long-term expected equity risk premium and the short-term expected equity risk premium, both derived from equity index option prices.

Mathematically:
`ΔHS = E[R]L - E[R]S`
Where:
*   `E[R]L` is the long-term expected risk premium (e.g., 180-day horizon).
*   `E[R]S` is the short-term expected risk premium (e.g., 30-day horizon).

## Extraction from Options
The expected equity risk premium for different horizons is extracted from equity index option prices using methodologies such as that proposed by Martin (2017). This involves estimating the conditional risk-neutral variance from a continuum of out-of-the-money put and call options.

## Behavior Across Regimes
*   **Normal Times (Expansion Regime)**: In periods of market calm, the horizon spread is typically **positive**. This aligns with classic asset pricing models (e.g., habit formation, long-run risk models) which suggest investors require a higher premium for holding assets over longer horizons to compensate for long-run risks.
*   **Crisis Periods (Contraction Regime)**: During financial crises or periods of high uncertainty, the horizon spread tends to turn **negative**. This indicates that the short-term expected risk premium exceeds the long-term expected risk premium. Investors demand a significantly higher premium for immediate risks, expecting uncertainty to abate over longer horizons.

## Role in Regime Detection
Research by [[wan-ni-lai]] in "Detecting Stock Market Regimes from Option Prices" (2022) highlights the superior performance of the horizon spread as an indicator for [[stock-market-regimes|stock market regime]] detection:
*   **Earlier Detection**: It provides earlier signals of regime shifts compared to traditional indicators like historical returns or conditional volatility.
*   **Sharper Distinction**: The distribution of the horizon spread shows a more distinct bimodal characteristic between expansion and contraction states, leading to clearer and more decisive probabilities in [[hidden-markov-models|Hidden Markov Models]].
*   **Improved Forecasting**: Its effectiveness in regime detection translates into better out-of-sample forecasting performance for the [[equity-risk-premium|equity risk premium]].

## Significance
The horizon spread, derived from forward-looking option prices, offers a valuable tool for understanding market sentiment and anticipating shifts in market dynamics, providing insights that backward-looking indicators may miss or signal with a delay.

## Related Concepts
*   [[equity-risk-premium]]
*   [[stock-market-regimes]]
*   [[option-implied-volatility]]
*   [[hidden-markov-models]]
*   [[detecting-stock-market-regimes-from-option-prices-lai-2022|Detecting Stock Market Regimes from Option Prices (Lai, 2022)]]
---