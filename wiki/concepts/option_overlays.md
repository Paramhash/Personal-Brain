---
tags: ["options", "portfolio_management", "hedging", "systematic_investing"]
created: 2023-10-27
reviewed: false
source_origin: "../research/options_portfolio_research_guide.md"
---
# Option Overlays

Option overlays are strategies where options positions are added to an existing portfolio of underlying assets (e.g., stocks, bonds, ETFs) to modify its risk-return profile without significantly altering the core asset allocation. They are typically used by institutional investors and portfolio managers to achieve specific objectives such such as:

*   **Yield Enhancement:** Selling options (e.g., covered calls, cash-secured puts) to generate additional income from the portfolio, often targeting the [[../concepts/volatility_risk_premium.md|Volatility Risk Premium (VRP)]].
*   **Downside Protection (Portfolio Insurance):** Buying protective puts or implementing more complex option structures to limit potential losses during market downturns.
*   **Risk Reduction:** Using options to hedge specific risks (e.g., currency risk, interest rate risk) or to reduce overall portfolio volatility.
*   **Targeted Exposure:** Gaining exposure to specific market views (e.g., volatility, market direction) with less capital outlay than direct asset ownership.

**Key Characteristics:**
*   **Modular:** The options component is separate from, but interacts with, the underlying asset portfolio.
*   **Capital Efficient:** Options can provide significant leverage or protection with a relatively small capital commitment compared to the underlying assets.
*   **Dynamic:** Many overlay strategies require active management and rebalancing due to the time decay and changing sensitivities of options (e.g., [[../concepts/delta_hedging.md|delta-hedging]]).

**Systematic Design:**
The systematic design of option overlays involves defining clear rules for:
*   **Option Selection:** Choosing strike prices, maturities, and option types (calls/puts).
*   **Position Sizing:** Determining the number of contracts to trade relative to the underlying portfolio.
*   **Rebalancing:** Establishing frequencies and triggers for adjusting option positions.
*   **[[../concepts/risk_management.md|Risk Management]]:** Setting limits on potential losses and managing exposure to various [[../concepts/option_greeks.md|Greeks]].

**Related Research:**
*   [[../sources/guo_loeper_2020_designing_all_weather_overlays.md|Guo & Loeper (2020) - Designing All-Weather Overlays — A Study on Option-Based Systematic Strategies]] provides an empirical template for structural design, examining systematic options selling strategies paired with downside protection.

**See Also:**
*   [[../research/options_portfolio_research_guide.md|Guide to Options Portfolio Research]]
*   [[../concepts/systematic_options_strategies.md|Systematic Options Strategies]]
*   [[../concepts/options_portfolio_optimization.md|Options Portfolio Optimization]]