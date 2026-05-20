---
tags: ["trading-rules", "regulation", "finra", "day-trading"]
created: 2023-10-27
reviewed: false
source_origin: "account-status.md"
---
# Pattern Day Trader (PDT)

A Pattern Day Trader (PDT) is a designation under [[../entities/finra.md|FINRA]] rules for individuals who execute four or more "day trades" within five business days in a margin account. A "day trade" is defined as the opening and closing of the same security position on the same trading day.

**Key Implications:**

*   **Minimum Equity Requirement:** PDTs are required to maintain a minimum of $25,000 in equity in their margin account at the close of any day on which a day trade occurs. If the account falls below this minimum, the trader will be issued a "day trade equity maintenance call" and will be restricted from day trading until the call is met.
*   **Trading Restrictions:** If the minimum equity requirement is not met, the account may be restricted to closing-only transactions for 90 days.

The [[../entities/tastytrade-api-account-status.md|Tastytrade Account Status API]] provides fields like `is-pattern-day-trader` and `day-trade-count` within the [[../concepts/trading-status-object.md|TradingStatus object]] to help monitor and manage PDT status.