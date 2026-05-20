---
tags: [market-regimes, options, quantitative-finance, hidden-markov-model]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Market Regime: Pinning

"Pinning" refers to a market microstructure regime, particularly prevalent in near-expiry options, where the underlying asset's price tends to gravitate towards and remain close to a specific strike price as expiration approaches. This phenomenon is often attributed to the hedging activities of options market makers. If a large amount of open interest (OI) or gamma exposure (GEX) is concentrated at a particular strike, dealers who are short options at that strike may actively trade the underlying to keep its price near that strike to minimize their hedging costs or gamma exposure.

Characteristics of a pinning regime often include:
*   Low [[../concepts/realized-vol-intraday.md|intraday realized volatility]].
*   High [[../concepts/oi-concentration-ratio.md|OI concentration]] at or near the At-The-Money (ATM) strike.
*   The underlying spot price being close to a significant [[../concepts/spot-to-gamma-wall-distance.md|gamma wall]].

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], "pinning" is identified as State 0, characterized by the lowest mean of the `realized_vol_intraday` feature among the three regimes.

---