---
tags: ["tastytrade", "api", "market-data", "quotes", "dxlink"]
created: 2023-10-27
reviewed: false
source_origin: "faq.md"
---
# tastytrade Streaming Market Data and Quotes

Accessing streaming market data and quotes through the [[../entities/tastytrade.md|tastytrade]] API is a multi-step process involving an external quote provider, [[../entities/dxlink.md|DxLink]].

## Process Overview

1.  **Fetch API Quote Token:** Obtain a specific API quote token from tastytrade. This token is distinct from the standard access token used for other API requests.
2.  **Authenticate with DxLink:** Use the fetched API quote token to authenticate with [[../entities/dxlink.md|DxLink]], which is the quote provider.
3.  **Stream Quotes:** Once authenticated with DxLink, you can begin streaming market data and quotes.

## Further Information

For detailed instructions on how to stream quotes, refer to the "Streaming Market Data" section in the official tastytrade API documentation.

## Related Concepts

*   [[../entities/tastytrade.md|tastytrade]]
*   [[../entities/dxlink.md|DxLink]]
*   [[./tastytrade-api-conventions.md|tastytrade API Conventions]]

---
*This information is derived from the tastytrade API FAQ.*