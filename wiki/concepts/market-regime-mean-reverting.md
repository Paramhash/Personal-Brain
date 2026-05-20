---
tags: [market-regimes, options, quantitative-finance, hidden-markov-model]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Market Regime: Mean-Reverting

"Mean-reverting" describes a market microstructure regime where the underlying asset's price, after deviating from an average or equilibrium level, tends to revert back towards that level. This behavior suggests a lack of strong directional momentum and a tendency for prices to oscillate around a central value.

Characteristics of a mean-reverting regime might include:
*   Moderate [[../concepts/realized-vol-intraday.md|intraday realized volatility]].
*   Less extreme [[../concepts/gex-concentration-at-expiry.md|GEX concentration]] or [[../concepts/oi-concentration-ratio.md|OI concentration]] compared to pinning or gamma squeeze states.
*   The underlying price moving within a relatively defined range.

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], "mean-reverting" is identified as State 1, characterized by the middle mean of the `realized_vol_intraday` feature among the three regimes.

---