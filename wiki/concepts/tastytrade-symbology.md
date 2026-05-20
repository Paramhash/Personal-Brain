---
tags: ["concept", "tastyworks-api", "symbology", "instrument-symbols"]
created: 2023-10-27
reviewed: false
source_origin: "instruments.md"
---
# tastytrade Symbology

The [[../entities/tastyworks-instruments-api.md|tastyworks Instruments API]] uses specific symbol formats for different instrument types. Understanding these conventions is crucial for interacting with the API and interpreting data.

| Instrument Type | Symbol Format | Example |
|----------------|---------------|---------|
| Equity | Ticker symbol | `AAPL`, `SPY` |
| Equity Option | OCC format: `SYMBOL  YYMMDDCSSSSSSSS` (6-char padded symbol + date + C/P + 8-digit strike×1000) | `AAPL  260417C00200000` |
| Future | `/` prefix + product code + month code + year digit | `/ESM6` |
| Future Option | `./` prefix + underlying future + space + option root + expiration + C/P + strike | `./ESZ9 EW4U9 190927P2975` |
| Cryptocurrency | Trading pair with `/` separator | `BTC/USD` |
| Warrant | Ticker symbol (typically ending in `W`) | `RGTIW` |

**Futures month codes:**
*   F = January
*   G = February
*   H = March
*   J = April
*   K = May
*   M = June
*   N = July
*   Q = August
*   U = September
*   V = October
*   X = November
*   Z = December