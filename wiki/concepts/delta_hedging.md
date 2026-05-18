---
tags: ["options", "hedging", "risk_management", "derivatives"]
created: 2023-10-27
reviewed: false
source_origin: "../research/options_portfolio_research_guide.md"
---
# Delta Hedging

Delta hedging is a strategy used to reduce or eliminate the directional risk (exposure to price changes in the underlying asset) of an options position or a portfolio of options. It involves taking an offsetting position in the underlying asset (e.g., shares, futures) based on the option's [[../concepts/option_greeks.md|delta]].

**Understanding Delta:**
Delta is one of the [[../concepts/option_greeks.md|option Greeks]], representing the sensitivity of an option's price to a $1 change in the underlying asset's price. A delta of 0.50 means the option's price is expected to change by $0.50 for every $1 change in the underlying.

**How Delta Hedging Works:**
To achieve a delta-neutral position (where the overall portfolio delta is zero), an investor takes a position in the underlying asset equal to the negative of the option's delta.
*   If you are long a call option with a delta of +0.60, you would short 60 shares of the underlying (or 0.60 units of a futures contract) to become delta-neutral.
*   If you are short a put option with a delta of -0.40, you would buy 40 shares of the underlying (or 0.40 units of a futures contract) to become delta-neutral.

**Dynamic Nature:**
Delta is not constant; it changes as the underlying price moves, as time passes, and as volatility changes. Therefore, delta hedging is a dynamic process that requires frequent adjustments (rebalancing) to maintain delta-neutrality. This rebalancing is driven by the option's [[../concepts/option_greeks.md|gamma]], which measures the rate of change of delta.

**Backtesting Realities:**
When [[../concepts/backtesting.md|backtesting]] strategies that rely on dynamic replication or delta-neutrality, it is crucial to account for:
*   **[[../concepts/transaction_costs_in_options.md|Transaction Costs]]:** Each rebalancing trade incurs costs (commissions, bid-ask spreads) on the underlying shares/futures. These costs can significantly erode profits, especially with frequent hedging.
*   **Timing Lag:** The frequency of rebalancing (e.g., end-of-day vs. continuous intraday hedging) impacts the effectiveness and cost of the hedge.
*   **Slippage:** The difference between the expected price of a trade and the actual execution price.

**See Also:**
*   [[../research/options_portfolio_research_guide.md|Guide to Options Portfolio Research]]
*   [[../concepts/option_greeks.md|Option Greeks]]
*   [[../concepts/transaction_costs_in_options.md|Transaction Costs in Options]]