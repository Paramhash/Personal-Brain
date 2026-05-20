---
tags: ["corporate-actions", "equities", "options", "market-metrics"]
created: 2023-10-27
reviewed: false
source_origin: "market-metrics.md"
---
# Dividends

**Dividends** are a distribution of a portion of a company's earnings, decided by its board of directors, to a class of its shareholders. They can be paid out as cash, stock, or other property. Dividends are typically paid quarterly, but some companies pay monthly, semi-annually, or annually.

Key dates associated with dividends:
*   **Declaration Date:** The date on which the company's board of directors announces the dividend.
*   **Ex-Dividend Date:** The first day a stock trades without the right to receive the declared dividend. To receive the dividend, an investor must own the stock before this date.
*   **Record Date:** The date on which a company determines which shareholders are eligible to receive a dividend.
*   **Payment Date:** The date on which the company actually pays the dividend to eligible shareholders.

**Relevance to Options Trading:**
Dividends can impact options pricing and trading strategies, particularly for short call positions. Deep in-the-money short calls on dividend-paying stocks carry a risk of early assignment around the ex-dividend date, as the call buyer may exercise to capture the dividend.

The [[../entities/tastyworks-market-metrics-api.md|Tastyworks Market Metrics API]] provides historical dividend data, including the `occurred-date` (ex-dividend date) and `amount` for a given equity symbol, which is crucial for managing dividend-related risks in options portfolios.

---