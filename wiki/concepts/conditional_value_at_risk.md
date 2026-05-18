---
tags: ["risk_management", "quantitative_finance", "tail_risk", "optimization"]
created: 2023-10-27
reviewed: false
source_origin: "../research/options_portfolio_research_guide.md"
---
# Conditional Value-at-Risk (CVaR)

Conditional Value-at-Risk (CVaR), also known as Expected Shortfall (ES), is a risk measure used in quantitative finance to quantify the expected loss of a portfolio beyond a certain confidence level. It is a more robust and coherent risk measure than [[../concepts/value_at_risk.md|Value-at-Risk (VaR)]] because it considers the magnitude of losses in the tail of the distribution, not just the threshold at which they occur.

**Key Characteristics:**
*   **Tail Risk Focus:** CVaR specifically measures the average loss that occurs when the loss exceeds the VaR threshold. For example, a 95% CVaR of $1 million means that, on average, if losses exceed the 95% VaR, the expected loss will be $1 million.
*   **Coherent Risk Measure:** Unlike VaR, CVaR satisfies the properties of a coherent risk measure (monotonicity, sub-additivity, positive homogeneity, and translational invariance), making it more suitable for [[../concepts/portfolio_optimization.md|portfolio optimization]] and [[../concepts/risk_management.md|risk management]].
*   **Non-linear Payoffs:** CVaR is particularly useful for portfolios containing assets with non-linear payoffs, such as options, where traditional variance-based measures may be inadequate.

**Application in Options Portfolio Optimization:**
For portfolios incorporating options, especially those designed for [[../concepts/portfolio_insurance.md|portfolio insurance]] or [[../concepts/tail_risk_modeling.md|tail-risk]] mitigation, optimizing for CVaR is often preferred over minimizing variance. This is because options can significantly alter the tail behavior of a portfolio's return distribution. By minimizing CVaR, investors aim to reduce the severity of potential large losses.

**Related Research:**
*   [[../sources/maasar_2016_portfolio_optimisation_using_risky_assets.md|Maasar (2016) - Portfolio Optimisation Using Risky Assets with Options as Derivative Insurance]] explores how incorporating index options into an optimization model affects downside risk when minimizing CVaR.

**See Also:**
*   [[../research/options_portfolio_research_guide.md|Guide to Options Portfolio Research]]
*   [[../concepts/tail_risk_modeling.md|Tail Risk Modeling]]
*   [[../concepts/options_portfolio_optimization.md|Options Portfolio Optimization]]