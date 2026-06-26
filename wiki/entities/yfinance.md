---
tags: ["python-library", "data-acquisition", "financial-data", "open-source"]
created: 2023-10-27
reviewed: false
source_origin: "/wiki/sources/zero-cost-feature-engineering-payload.md"
---
# yfinance

`yfinance` is a free and open-source Python library that provides a convenient way to download historical market data from Yahoo Finance.

## Usage in Zero-Cost Feature Engineering
In the context of [[../concepts/zero-cost-feature-engineering.md]], `yfinance` is the primary tool for acquiring the necessary End-of-Day (EOD) price and volume data for the [[../entities/nasdaq-100.md]] stocks. The workflow involves a single network request to efficiently pull data for all 100 tickers:

```python
import yfinance as yf
# ... (list of Nasdaq 100 tickers)
data = yf.download(tickers, period="6mo")
```

This allows for the calculation of all five features without incurring any data costs.

---
### Related Concepts
*   [[../concepts/zero-cost-feature-engineering.md]]
*   [[../entities/pandas-ta.md]]

### Source
This information is derived from the [[../sources/zero-cost-feature-engineering-payload.md]].