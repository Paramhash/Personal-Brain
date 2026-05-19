---
tags: ["Data Source", "Market Data", "Exchanges"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Data Feeds

The [Theta Data v3](../../entities/theta-data-v3.md) API sources its financial market data from various reputable data feeds. Understanding these feeds is important as they dictate the characteristics of the data, such as real-time vs. delayed, and the specific asset classes covered.

## Primary Data Feeds:

*   **[Nasdaq Basic](../entities/nasdaq-basic.md)**:
    *   Provides real-time last sale and quotation data for Nasdaq-listed securities.
    *   Often used for real-time stock snapshot data in Theta Data v3 for higher [Subscription Tiers](../concepts/subscription-tiers.md).

*   **[UTP & CTA Feeds](../entities/utp-cta-feeds.md)**:
    *   The Consolidated Tape Association (CTA) and Unlisted Trading Privileges (UTP) feeds are Securities Information Processors (SIPs) that consolidate trade and quote data from all participating U.S. exchanges for NYSE and Nasdaq-listed securities, respectively.
    *   Used for 15-minute delayed stock data and comprehensive historical stock data in Theta Data v3.

*   **[OPRA (Options Price Reporting Authority)](../entities/opra.md)**:
    *   The primary source for last sale and quotation information for options contracts traded on U.S. options exchanges.
    *   Used for all options data, including historical and snapshot data, and [Option Greeks](../concepts/option-greeks.md) calculations in Theta Data v3.

## Impact on Data:
The choice of data feed can influence:
*   **Timeliness**: Real-time vs. 15-minute delayed data.
*   **Coverage**: Which exchanges and asset classes are included.
*   **Reporting Standards**: How End-of-Day (EOD) reports, trade conditions, and quote conditions are generated or interpreted.

For more details on specific data characteristics, refer to the individual endpoint documentation and related articles on [Trade Conditions](../concepts/trade-conditions.md), [Quote Conditions](../concepts/quote-conditions.md), and [Exchanges](../concepts/exchanges.md).

---