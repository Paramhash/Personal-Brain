---
tags: [gamma exposure, market dynamics, mean reversion, acceleration, trading strategy, options trading]
created: 2023-10-27
reviewed: false
source_origin: "/raw/Regime Divergence Ratio.md"
---
# Gamma Flip

The **Gamma Flip** (also known as the "Gamma Flip Level" or "GEX Flip") is a critical threshold in options market analysis, particularly concerning dealer positioning and its impact on underlying asset price action. It represents a price level (or range) where the aggregate gamma exposure of market makers (dealers) shifts from net short to net long, or vice-versa.

## Dealer Positioning and Market Behavior

The Gamma Flip dictates the prevailing market environment based on whether the underlying asset's price is above or below this level:

*   **Above the Flip: Mean Reverting Environment**
    *   When the market price is **above** the Gamma Flip level, dealers are typically **net long gamma**.
    *   In this state, dealers' hedging activities tend to dampen volatility and promote mean reversion. As the market moves higher, dealers sell the underlying asset to re-hedge their long gamma positions. As the market moves lower, they buy the underlying.
    *   This creates a "sticky" market where every 1% move higher meets selling pressure, and every 1% move lower meets buying support, leading to a tendency for prices to revert to a central point.

*   **Below the Flip: Acceleration Environment**
    *   When the market price is **below** the Gamma Flip level, dealers are typically **net short gamma**.
    *   In this state, dealers' hedging activities tend to exacerbate price movements, leading to increased volatility and momentum. As the market falls, dealers must sell more of the underlying asset to re-hedge their short gamma positions, accelerating the decline. As the market rises, they buy, accelerating the rise.
    *   This creates an "acceleration" environment where price movements are amplified, often leading to trending behavior rather than mean reversion.

## Relevance to Market Regimes

The reliability of the Gamma Flip as an indicator is particularly strong when the market is in a [[../concepts/regime-divergence-ratio.md#Coherent-Regime-(0.5-Ratio-2.0)|Coherent Regime]], as identified by the [[../concepts/regime-divergence-ratio.md|Regime Divergence Ratio]]. In such coherent states, the index and its components are well-synchronized, allowing standard gamma rules to apply more implicitly and predictably.