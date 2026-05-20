---
tags: [trading, margin, risk, finance, leverage]
created: 2023-10-27
reviewed: false
source_origin: "risk-parameters.md"
---
# Margin Requirements

Margin requirements are the minimum amount of equity an investor must maintain in their margin account to cover potential losses from leveraged positions. They are set by regulatory bodies and brokerage firms to mitigate risk.

Key types of margin requirements include:
*   **Initial Margin:** The percentage of the purchase price of a security that an investor must pay for with their own cash when using a margin account.
*   **Maintenance Margin:** The minimum amount of equity that must be maintained in a margin account after a security has been purchased. If the account value falls below this level, a margin call is issued.
*   **Naked Option Margin:** Specific, often higher, margin requirements for selling uncovered (naked) options, due to the potentially unlimited risk involved.

The [[../entities/tastyworks-risk-parameters-api.md|Tastyworks Risk Parameters API]] offers endpoints like `Get Effective Margin Requirements` to retrieve symbol-specific initial, maintenance, and naked option margin rates (represented by the `MarginRequirement` data model). It also provides a `Get Public Margin Configuration` endpoint which includes global parameters like the [[../concepts/risk-free-rate.md|risk-free rate]] (part of the `MarginRequirementsGlobalConfiguration` data model) used in margin calculations.

---