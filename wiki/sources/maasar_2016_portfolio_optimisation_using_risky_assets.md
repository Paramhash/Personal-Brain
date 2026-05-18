---
tags: ["research_paper", "options", "portfolio_optimization", "risk_management", "conditional_value_at_risk"]
created: 2023-10-27
reviewed: false
source_origin: "https://doi.org/10.4230/OASIcs.SCOR.2016.9"
---
# Portfolio Optimisation Using Risky Assets with Options as Derivative Insurance (Maasar, 2016)

**Title:** Portfolio Optimisation Using Risky Assets with Options as Derivative Insurance
**Author:** [[../entities/m_a_maasar.md|M.A. Maasar]]
**Year:** 2016
**Source:** OASIcs-OpenAccess Series in Informatics, Vol. 50
**DOI:** 10.4230/OASIcs.SCOR.2016.9

**Core Focus:**
This paper addresses the limitations of traditional [[../concepts/mean_variance_optimization.md|mean-variance frameworks]] when applied to portfolios containing options, primarily due to their non-linear payoff structures. It explores how incorporating index options into an [[../concepts/options_portfolio_optimization.md|optimization model]] can affect downside risk.

The central theme is the minimization of [[../concepts/conditional_value_at_risk.md|Conditional Value-at-Risk (CVaR)]] rather than standard variance, to account for the [[../concepts/tail_risk_modeling.md|tail risk]] characteristics introduced by options. The research provides both in-sample optimization and out-of-sample [[../concepts/backtesting.md|backtesting]] to demonstrate how systematically integrated put structures can lower the cost of [[../concepts/portfolio_insurance.md|portfolio insurance]].

**Key Takeaways:**
*   Traditional mean-variance optimization is inadequate for options portfolios.
*   CVaR minimization is a more appropriate objective for options portfolio optimization, especially for downside risk management.
*   Systematic integration of put options can effectively reduce portfolio insurance costs.
*   Empirical evidence from both in-sample and out-of-sample tests supports the approach.

**Related Concepts:**
*   [[../concepts/options_portfolio_optimization.md|Options Portfolio Optimization]]
*   [[../concepts/conditional_value_at_risk.md|Conditional Value-at-Risk (CVaR)]]
*   [[../concepts/tail_risk_modeling.md|Tail Risk Modeling]]
*   [[../concepts/backtesting.md|Backtesting]]
*   [[../concepts/portfolio_insurance.md|Portfolio Insurance]]

**See Also:**
*   [[../research/options_portfolio_research_guide.md|Guide to Options Portfolio Research]]
*   [[../entities/m_a_maasar.md|M.A. Maasar]]