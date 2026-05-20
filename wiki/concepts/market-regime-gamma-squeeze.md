---
tags: [market-regimes, options, quantitative-finance, hidden-markov-model]
created: 2023-10-27
reviewed: false
source_origin: "Near-Expiry HMM for SPX 7DTE-1DTE Options Dynamics.md"
---
# Market Regime: Gamma Squeeze

A "gamma squeeze" is a market microstructure regime characterized by rapid and often amplified price movements in the underlying asset, driven by the hedging activities of options market makers. It typically occurs when dealers are significantly short gamma and the underlying price moves sharply in one direction. As the price moves, their negative gamma exposure increases, forcing them to buy (if price rises) or sell (if price falls) the underlying asset to maintain a delta-neutral hedge. This hedging activity further pushes the price in the same direction, creating a feedback loop or "squeeze."

Characteristics of a gamma squeeze regime often include:
*   High [[../concepts/realized-vol-intraday.md|intraday realized volatility]].
*   Significant [[../concepts/gex-concentration-at-expiry.md|GEX concentration]] or [[../concepts/oi-concentration-ratio.md|OI concentration]] that creates large gamma exposures.
*   Rapid changes in [[../concepts/atm-gamma-velocity.md|ATM gamma velocity]].
*   Strong directional flow indicated by the [[../concepts/call-put-volume-ratio.md|call/put volume ratio]].

In the [[../concepts/near-expiry-hmm-options-dynamics.md|Near-Expiry HMM for SPX/SPY Options Dynamics]], "gamma squeeze" is identified as State 2, characterized by the highest mean of the `realized_vol_intraday` feature among the three regimes.

---