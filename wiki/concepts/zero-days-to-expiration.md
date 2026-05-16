---
tags: ["options", "0DTE", "trading-strategy", "risk-management"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# Zero Days To Expiration (0DTE) Options

Zero Days To Expiration (0DTE) options are options contracts that expire on the same day they are traded. These options have become increasingly popular due to their unique risk-reward characteristics and rapid price movements.

## Characteristics

*   **High Theta Decay:** [Theta](../concepts/options-greeks.md) (time decay) is at its maximum for 0DTE options, meaning their value erodes very quickly as the day progresses.
*   **Extreme Sensitivity to Underlying Price:** Small movements in the underlying asset can lead to significant percentage changes in 0DTE option prices, especially for out-of-the-money contracts.
*   **High Gamma:** [Gamma](../concepts/options-greeks.md) is also very high for 0DTE options, particularly near the strike price, leading to rapid changes in [Delta](../concepts/options-greeks.md).
*   **Liquidity:** Many underlying assets, particularly major indices, have highly liquid 0DTE markets.

## Trading Strategies

0DTE options are often used for:
*   **Intraday Speculation:** Profiting from short-term price movements.
*   **Hedging:** Providing very short-term, precise hedges against intraday portfolio risk.
*   **Income Generation:** Selling options with high Theta decay.

## Risks

*   **Rapid Value Erosion:** The high Theta decay can quickly diminish the value of long option positions.
*   **Extreme Volatility:** Price swings can be very large and fast, leading to significant losses if not managed carefully.
*   **Pin Risk:** The risk that an option expires exactly at the strike price, leading to uncertainty about assignment.

## Data Providers

Access to real-time data for 0DTE options, including their [Options Greeks](../concepts/options-greeks.md) and [Volatility Surfaces](../concepts/volatility-surfaces.md), is crucial for trading them effectively. Some [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md), such as [FlashAlpha](../entities/flashalpha.md), offer specific data packages that include 0DTE information.

---