---
tags: ["margin", "risk-management", "trading", "advanced-strategies"]
created: 2023-10-27
reviewed: false
source_origin: "account-status.md"
---
# Portfolio Margin

Portfolio margin is an advanced, risk-based margin methodology that calculates margin requirements based on the overall risk of a customer's portfolio, rather than on fixed percentages for individual positions (as in [[../concepts/reg-t-margin.md|Reg-T margin]]).

This approach often results in lower margin requirements for diversified portfolios with offsetting positions, as it considers the potential loss of the entire portfolio under various market scenarios. It is typically available to experienced traders with substantial account equity.

The [[../entities/tastytrade-api-account-status.md|Tastytrade Account Status API]] includes the `is-portfolio-margin-enabled` field within the [[../concepts/trading-status-object.md|TradingStatus object]] to indicate if this margin type is active for an account.