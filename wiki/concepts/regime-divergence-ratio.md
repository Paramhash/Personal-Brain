---
tags: [market analysis, gamma exposure, divergence, trading strategy, quantitative finance, market regimes]
created: 2023-10-27
reviewed: false
source_origin: "/raw/Regime Divergence Ratio.md"
---
# Regime Divergence Ratio

The **Regime Divergence Ratio** is a quantitative metric used to assess the synchronization between the hedging dynamics of a broad market index (like the S&P 500) and its underlying components. It helps identify periods where index-level behavior deviates significantly from the aggregate behavior of individual stocks, signaling different market "regimes" that imply distinct trading strategies.

The ratio is calculated after performing a series of gamma exposure (GEX) calculations, often involving high-performance computing (e.g., using a 3990X processor for 500 calculations).

## Calculation

The **Divergence Ratio** is calculated as follows:

$$\text{Divergence Ratio} = \frac{\text{Index GEX}}{\sum \text{Component GEX}}$$

Where:
*   **Index GEX**: Represents the Gamma Exposure of the S&P 500 Index itself.
*   **$\sum$ Component GEX**: Represents the sum of the individual Gamma Exposure values for all 500 component stocks within the S&P 500.

## Market Regimes Based on the Ratio

The value of the Divergence Ratio categorizes the market into distinct regimes:

### Divergent Regimes

These regimes indicate a significant decoupling between the index and its components, often leading to non-standard market behavior.

*   **Artificial Stability (Ratio > 2.0)**:
    *   **Characterization**: The index appears "pinned" or unusually stable, while its underlying components are exhibiting loose or volatile behavior. This suggests that index-level hedging (e.g., via SPX options) is disproportionately strong compared to the aggregate hedging of individual stocks.
    *   **Implication**: The market might be masking underlying volatility or directional pressure at the component level.

*   **Hidden Strength (Ratio < 0.5)**:
    *   **Characterization**: The index might appear volatile or weak, but its underlying components are being actively bought or show strong gamma support. This indicates that individual stock hedging is significantly stronger than the index-level hedging.
    *   **Implication**: Potential for a strong rebound or underlying bullish pressure not immediately apparent at the index level.

### Coherent Regime (0.5 $\le$ Ratio $\le$ 2.0)

When the Divergence Ratio falls within this range, the market is considered to be in a **Coherent Regime**. In this state, the index-level hedging is largely in sync with the underlying component hedging, and the market behaves as a unified entity. Standard gamma exposure rules and market dynamics generally apply. Arbitrage or "decoupling" trades are less effective here.

Within the Coherent Regime, three distinct zones are identified:

| Ratio Value    | Regime Characterization   | Market Behavior                                                              | Strategy Bias                                                                 |
| :------------- | :------------------------ | :--------------------------------------------------------------------------- | :---------------------------------------------------------------------------- |
| **0.5 to 0.9** | **Component-Led Strength** | Individual stocks are "heavier" in gamma than the index.                     | **Bullish Selection.** Pick high-gamma stocks to outperform the index.        |
| **0.9 to 1.1** | **Systemic Equilibrium**  | Perfect sync. Index and components move in lockstep.                         | **Index Trading.** Use SPY/SPX instruments; no edge in picking individuals.  |
| **1.1 to 2.0** | **Index-Led Stability**   | The index is "stickier" than the stocks, implying strong index-level support.| **Premium Selling.** Sell index credit spreads; buy-the-dip is highly reliable.|

## Implications within the Coherent Regime

### 1. Standard Gamma Rules Apply

In a Coherent Regime, especially near a ratio of 1.0, the [[../concepts/gamma-flip.md|Gamma Flip]] levels can be trusted implicitly.

*   **Above the Flip**: Dealers are typically long-gamma, leading to a "Mean Reverting" environment where price movements are met with counter-hedging (selling on rallies, buying on dips).
*   **Below the Flip**: Dealers are typically short-gamma, leading to an "Acceleration" environment where price movements are exacerbated by hedging (selling into declines, buying into rallies).

### 2. High Correlation Environment

When the ratio is near **1.0** (Systemic Equilibrium), market correlation is high. This is generally not an opportune time for dispersion trades (e.g., selling index volatility against buying stock volatility) as the index and its components tend to move in unison. The "Volatility Surface" of the S&P 500 appears relatively flat and uniform across sectors.

### 3. The "Efficiency" Trap

Markets in the Coherent Regime are considered "efficiently hedged." This means there are fewer hidden traps or sudden "gamma squeezes" because liquidity is well-distributed. Traders should be mindful of the edges of this regime:

*   **Watch for the "Edges"**: As the ratio approaches **2.0** (transitioning to Artificial Stability) or drops toward **0.5** (transitioning to Hidden Strength), it's crucial to prepare for the strategies associated with those divergent regimes. The transition *out* of the Coherent Regime often precedes significant volatility spikes, as the market is forced to re-hedge synchronized positioning.

## Monitoring the "Drift"

The Divergence Ratio should be visualized as a running time-series. Setting alerts for prolonged periods within the **0.9–1.1** range (Systemic Equilibrium) is advisable. Extended periods of Systemic Equilibrium can lead to a "coiled spring" effect, where the market builds up synchronized positioning. When the ratio eventually breaks out of the broader 0.5–2.0 Coherent Regime band, the ensuing market move is often violent due to the necessity of re-hedging massive, synchronized positions.