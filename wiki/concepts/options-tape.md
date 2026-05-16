---
tags: ["options", "market-data", "trading", "data-feeds"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# Options Tape

The "Options Tape" refers to the real-time stream of all executed trades and quotes for options contracts across various exchanges. It provides a comprehensive, granular view of market activity for options.

## Components of the Options Tape

*   **Trades:** Records of actual options contracts bought and sold, including price, volume, and timestamp.
*   **Quotes:** Real-time bid and ask prices for options contracts, often including size (number of contracts available at that price).
*   **Exchange Information:** Identifies the exchange where the trade or quote originated.

## Importance

Accessing the full options tape is crucial for:
*   **High-Frequency Trading:** Essential for strategies that rely on micro-movements and order flow analysis.
*   **Liquidity Analysis:** Understanding where liquidity is concentrated and how it's shifting.
*   **Implied Volatility Calculation:** Deriving accurate implied volatility figures from live market prices.
*   **[Options Greeks](../concepts/options-greeks.md) Calculation:** Providing the raw data necessary to calculate Greeks and aggregated metrics like [Gamma Exposure (GEX)](../concepts/gamma-exposure.md) locally.

## Data Providers

Providers like [Polygon.io](../entities/polygon-io.md) are known for streaming the entire options tape via [WebSockets](../concepts/websockets.md), offering a high-bandwidth, "clean" data feed suitable for demanding analytical tasks. Other [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md) may offer summarized or pre-processed data derived from the tape.

---