---
tags: ["stock-market-index", "equities", "financial-markets"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# Nasdaq 100

The Nasdaq 100 (NDX) is a stock market index composed of 100 of the largest non-financial companies listed on the Nasdaq stock market. It is a modified capitalization-weighted index, meaning that larger companies have a greater impact on the index's value. The index is widely regarded as a benchmark for large-cap growth stocks, particularly in the technology sector.

## Role in Zero-Cost Feature Engineering
The Nasdaq 100 serves as the universe of stocks for the [[../concepts/zero-cost-feature-engineering.md]] project. The [[../concepts/reinforcement-learning-agent.md]] is designed to analyze and make trading decisions specifically within this set of 100 companies.

Key aspects related to the NDX in this context include:
*   **Data Universe**: All 100 NDX stocks are targeted for data acquisition using [[../entities/yfinance.md]].
*   **Cross-Sectional Analysis**: Features like [[../concepts/cross-sectional-momentum.md]] are Z-scored against the other 99 stocks within this specific index, enabling relative performance comparisons.
*   **Agent Focus**: The RL agent's output is a "Top 10" list derived from this universe.

---
### Related Concepts
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../concepts/reinforcement-learning-agent.md]]
*   [[../concepts/cross-sectional-momentum.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].