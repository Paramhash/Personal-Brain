---
tags: ["api", "symbology", "trading", "instruments", "tastytrade"]
created: 2023-10-27
reviewed: false
source_origin: "llms.txt"
---
# tastytrade API Symbology

The [[../entities/tastytrade-open-api.md|tastytrade Open API]] employs a specific symbology convention for identifying various financial instruments across its platform. Understanding this system is crucial for making accurate API requests.

## Symbology Conventions
*   **Equities**: Represented by their standard stock ticker symbol (e.g., `AAPL`, `SPY`).
*   **OCC Equity Options**: Follow the Options Clearing Corporation (OCC) standard.
*   **Futures**: Prefixed with a `/` (e.g., `/ES`, `/CL`).
*   **Futures Options**: Prefixed with `./` (e.g., `./ES`, `./CL`).
*   **Cryptocurrency Pairs**: Typically represented as a pair (e.g., `BTC/USD`).

The API provides endpoints within the "Instruments" section of its reference to look up and verify symbology, including full option chains and details for various asset classes.

## Related
*   [[../entities/tastytrade-open-api.md|tastytrade Open API]]