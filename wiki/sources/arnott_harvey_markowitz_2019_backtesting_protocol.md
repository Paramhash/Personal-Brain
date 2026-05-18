---
tags: ["research_paper", "backtesting", "quantitative_finance", "machine_learning", "methodology"]
created: 2023-10-27
reviewed: false
source_origin: "https://doi.org/10.3905/jfds.2019.1.1.064"
---
# A backtesting protocol in the era of machine learning (Arnott, Harvey, & Markowitz, 2019)

**Title:** A backtesting protocol in the era of machine learning
**Authors:** [[../entities/rob_arnott.md|Rob Arnott]], [[../entities/campbell_r_harvey.md|Campbell R. Harvey]], & [[../entities/harry_markowitz.md|Harry Markowitz]]
**Year:** 2019
**Source:** The Journal of Financial Data Science, Vol. 1, No. 1
**DOI:** 10.3905/jfds.2019.1.1.064

**Core Focus:**
This paper is a foundational text for constructing rigorous, non-delusional [[../concepts/backtesting.md|backtests]] in the context of modern quantitative finance, especially with the rise of machine learning. It lays out strict protocols required to prevent common biases and pitfalls that can lead to misleading historical performance.

The authors emphasize the importance of guarding against:
*   **[[../concepts/selection_bias_in_quantitative_models.md|Selection Bias]] (Data Mining):** The tendency to find strategies that appear successful purely by chance after testing many variations.
*   **[[../concepts/overfitting_in_quantitative_models.md|Overfitting]]:** Creating models that perform perfectly on historical data but fail to generalize to new data.
*   **[[../concepts/data_leakage_in_backtesting.md|Data Leakage]] (Look-ahead Bias):** Accidentally using future information in a historical simulation.

The paper provides a framework for designing and evaluating multi-factor quantitative models, ensuring that backtest results are robust and indicative of potential future performance. It is highly relevant for anyone involved in the design and validation of [[../concepts/systematic_options_strategies.md|systematic options strategies]].

**Key Takeaways:**
*   Strict protocols are essential for reliable backtesting.
*   Focus on preventing selection bias, overfitting, and data leakage.
*   A foundational guide for evaluating complex quantitative models.

**Related Concepts:**
*   [[../concepts/backtesting.md|Backtesting]]
*   [[../concepts/selection_bias_in_quantitative_models.md|Selection Bias in Quantitative Models]]
*   [[../concepts/overfitting_in_quantitative_models.md|Overfitting in Quantitative Models]]
*   [[../concepts/data_leakage_in_backtesting.md|Data Leakage in Backtesting]]
*   [[../concepts/quantitative_finance.md|Quantitative Finance]]

**See Also:**
*   [[../research/options_portfolio_research_guide.md|Guide to Options Portfolio Research]]
*   [[../entities/rob_arnott.md|Rob Arnott]]
*   [[../entities/campbell_r_harvey.md|Campbell R. Harvey]]
*   [[../entities/harry_markowitz.md|Harry Markowitz]]
*   [[../entities/the_journal_of_financial_data_science.md|The Journal of Financial Data Science]]