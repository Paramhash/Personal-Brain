---
tags: ["symbology", "market-data", "streaming", "dxlink", "api"]
created: 2024-07-30
reviewed: false
source_origin: "streaming-market-data.md"
---
# DXLink Symbology

To receive live market event data via [[../entities/dxlink.md|DXLink]], clients must use a symbol format that meets DXLink's specific requirements. tastytrade's API simplifies this by providing a `streamer-symbol` field within its instrument data endpoints.

This `streamer-symbol` field contains the correctly formatted symbol for use with DXLink.

## Endpoints Providing `streamer-symbol`

The `streamer-symbol` field is available in the HTTP response bodies of the following tastytrade instrument endpoints:

*   `GET /instruments/cryptocurrencies`
*   `GET /instruments/equities/:symbol`
*   `GET /instruments/futures`
*   `GET /futures-option-chains/:product-code/nested`
*   `GET /option-chains/:underlying-symbol/nested`

### Example for Futures

When fetching futures instrument data, the `streamer-symbol` will be included:

```http
GET /instruments/futures
```

```json
{
    "data": {
        "items": [
            {
                "symbol": "/6AM3",
                "streamer-exchange-code": "XCME",
                "streamer-symbol": "/6AM23:XCME"
            }
        ]
    }
}
```

In this example, `/6AM23:XCME` is the correct format to use when subscribing to futures market events for that contract via DXLink.

## Related Concepts

*   [[../concepts/streaming-market-data.md|Streaming Market Data (tastytrade & DXLink)]]
*   [[../entities/dxlink.md|DXLink]]