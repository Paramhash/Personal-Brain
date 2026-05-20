---
tags: ["quantitative-finance", "pricing", "risk-management", "probabilities"]
created: 2023-10-27
reviewed: false
source_origin: "how to obtain HMM estimates of probability from option prices.md"
---
# Risk-Neutral vs. Real-World Probabilities ($\mathbb{Q}$ vs. $\mathbb{P}$)

In quantitative finance, it's crucial to distinguish between two types of probability measures:

1.  **Real-World Probabilities ($\mathbb{P}$-measure):** These are the actual probabilities of events occurring in the real world. They are typically estimated from historical data and reflect the true statistical likelihood of an asset's price movements, including expected returns and volatility. These are used for portfolio optimization, risk management, and forecasting actual future outcomes.

2.  **Risk-Neutral Probabilities ($\mathbb{Q}$-measure):** These are theoretical probabilities used for pricing financial derivatives. Under a risk-neutral measure, all assets are assumed to grow at the risk-free rate, and investors are indifferent to risk. This means that the expected return of any asset under the $\mathbb{Q}$-measure is the risk-free rate. Option prices, for instance, are typically derived using risk-neutral probabilities, as they embed the market's consensus view on future outcomes, adjusted for risk aversion.

The key difference lies in the **risk premium**. Real-world probabilities incorporate a risk premium (investors demand higher returns for taking on more risk), while risk-neutral probabilities do not. When [obtaining HMM estimates from option prices](../concepts/how-to-obtain-hmm-estimates-from-option-prices.md), the probabilities extracted are inherently risk-neutral ($\mathbb{Q}$-measures) because option prices themselves are derived under this framework. This means they reflect what the market is *pricing in* for future regimes, rather than what is statistically most likely to happen in the real world.