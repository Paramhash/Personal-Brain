---
tags: [futures, options, margin, risk, clearing, cme, cfe]
created: 2023-10-27
reviewed: false
source_origin: "risk-parameters.md"
---
# SPAN Margin

SPAN, which stands for **Standard Portfolio Analysis of Risk**, is a portfolio margining system developed by the [[../entities/cme-exchange.md|CME]] (Chicago Mercantile Exchange) and widely adopted by clearing organizations worldwide. It is a sophisticated methodology used to calculate margin requirements for futures, options on futures, and other derivatives.

Unlike simpler margin systems, SPAN calculates margin based on the overall risk of a portfolio, taking into account potential gains and losses across different scenarios (e.g., price changes, volatility changes). This allows for more efficient use of capital by recognizing offsets between correlated positions.

The [[../entities/tastyworks-risk-parameters-api.md|Tastyworks Risk Parameters API]] provides a `Get SPAN Rows` endpoint to retrieve raw SPAN margin data for specific dates and exchanges like [[../entities/cme-exchange.md|CME]] and [[../entities/cfe-exchange.md|CFE]]. This raw data, represented by the `Row` data model, can be used by advanced users for detailed futures margin analysis and risk management.

---