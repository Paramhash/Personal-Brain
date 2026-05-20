---
tags: ["finance", "instrument-type", "options"]
created: 2023-10-27
reviewed: false
source_origin: "symbol-search.md"
---
# Options Instrument

An options instrument is a contract that gives the buyer the right, but not the obligation, to buy or sell an underlying asset or instrument at a specified strike price on or before a certain date (the expiration date). There are two main types: call options (right to buy) and put options (right to sell).

In the context of the [[../concepts/symbol-data-model.md|SymbolData]] model, an instrument can indicate if it has listed options available via the `options` boolean field. While `Option` itself might be an `instrument-type` for specific option contracts, the `options` field in `SymbolData` refers to the underlying's option availability.