---
tags: ["Market Data", "Financial Exchanges", "Trade Data", "Quote Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Exchanges

Financial exchanges are marketplaces where securities, commodities, derivatives, and other financial instruments are traded. In the context of the [Theta Data v3](../../entities/theta-data-v3.md) API, exchange information is often provided in trade and quote data to indicate where a particular transaction or quotation originated.

The API references external articles for detailed mappings of exchange codes:
*   [Exchanges Article](/Articles/Errors-Exchanges-Conditions/Exchanges.html)

## Relevance in Theta Data v3:
*   **Trade Data**: Endpoints like [Stock History Trade Endpoint](../concepts/stock-history-trade-endpoint.md) and [Option History Trade Endpoint](../concepts/option-history-trade-endpoint.md) include an `exchange` field, indicating where the trade was executed.
*   **Quote Data**: Endpoints like [Stock History Quote Endpoint](../concepts/stock-history-quote-endpoint.md) and [Option History Quote Endpoint](../concepts/option-history-quote-endpoint.md) include `bid_exchange` and `ask_exchange` fields, identifying the exchanges providing the best bid and ask.
*   **Venue Parameter**: The `venue` [API Parameter](../concepts/api-parameters.md#venue) allows specifying the data source, such as `nqb` for [Nasdaq Basic](../entities/nasdaq-basic.md) or `utp_cta` for [UTP & CTA Feeds](../entities/utp-cta-feeds.md), which are consolidated feeds from multiple exchanges.

Understanding the exchange codes can be important for detailed analysis, especially when examining market microstructure or routing strategies.

## Related Concepts:
*   [Data Feeds](../concepts/data-feeds.md)
*   [Trade Conditions](../concepts/trade-conditions.md)
*   [Quote Conditions](../concepts/quote-conditions.md)
*   [API Parameters](../concepts/api-parameters.md)

---