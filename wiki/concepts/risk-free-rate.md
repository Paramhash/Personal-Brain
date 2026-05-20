---
tags: [finance, economics, interest-rate, margin, options-pricing]
created: 2023-10-27
reviewed: false
source_origin: "risk-parameters.md"
---
# Risk-Free Rate

The risk-free rate is the theoretical rate of return of an investment with zero risk. In practice, it is often approximated by the yield on short-term government securities (e.g., U.S. Treasury bills), as these are considered to have minimal default risk.

The risk-free rate is a fundamental concept in finance, used in various calculations and models, including:
*   **Margin Calculations:** It can be a component in determining the cost of borrowing for [[../concepts/margin-requirements.md|margin accounts]] or in calculating certain margin requirements.
*   **Options Pricing Models:** Models like the Black-Scholes model use the risk-free rate as a key input to discount future cash flows and determine the theoretical fair value of an option.
*   **Valuation:** It serves as a baseline for discounting future cash flows in valuation models.

The [[../entities/tastyworks-risk-parameters-api.md|Tastyworks Risk Parameters API]] offers a `Get Public Margin Configuration` endpoint that provides the current risk-free rate (as part of the `MarginRequirementsGlobalConfiguration` data model) used in their internal margin calculations. This publicly accessible endpoint does not require authentication.

---