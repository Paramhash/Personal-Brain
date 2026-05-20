---
tags: [trading, risk-management, limits, account-management]
created: 2023-10-27
reviewed: false
source_origin: "risk-parameters.md"
---
# Position Limits

Position limits refer to the maximum number of contracts or shares of a particular security that an individual or entity is permitted to hold in a trading account. These limits are typically set by exchanges, regulatory bodies, or brokerage firms like [[../entities/tastyworks.md|Tastyworks]] to manage risk, prevent market manipulation, and ensure market stability.

For example, the [[../entities/tastyworks-risk-parameters-api.md|Tastyworks Risk Parameters API]] provides a `Get Position Limit` endpoint and a `PositionLimit` data model to retrieve these maximum order and position sizes across various instrument types (equities, options, futures) for a given account. Traders can use this information for pre-trade checks to ensure their orders do not exceed these defined boundaries.

---