---
tags:
- options trading
- market microstructure
- gamma
- gex
- derivatives
- financial-metrics
- options-trading
- market-structure
- risk-indicators
- quantitative finance
- GEX
- market makers
- options
- market-making
- risk-management
created: 2023-10-27
reviewed: false
source_origin: combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md
aliases:
- gex
- Gamma Exposure (GEX)
- gamma-exposure
- gamma_exposure_gex
updated: '2026-10-02'
sources:
- combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md
- merged note gex.md
- merged note gamma-exposure.md
- merged note gamma_exposure_gex.md
ingest_hashes:
- 2c4528a8104b5d41
- d085d2a11abe0ecc
- c5b51c5aeb36c5b7
---
# Gamma Exposure (GEX)

Gamma Exposure (GEX) is a key market indicator used in options trading to quantify the potential impact of dealer hedging activities on the underlying asset's price. It represents the total dollar amount of gamma across all outstanding options contracts, indicating how much dealers need to buy or sell the underlying asset for every dollar move in its price to maintain a delta-neutral position.

## Calculation Module

For every option contract in the chain at a given timestamp $t$:

1.  **Calculate Gamma ($\Gamma$):** This can be derived using the [[../entities/black-scholes-model.md|Black-Scholes model]] or extracted directly from the options data feed.
2.  **Calculate Total Dollar Gamma Exposure:**
    *   For Call Options:
        $$\text{GEX}_{\text{Call}} = \text{Open Interest} \times \Gamma \times \text{Spot Price}^2 \times 100$$
    *   For Put Options:
        $$\text{GEX}_{\text{Put}} = \text{Open Interest} \times \Gamma \times \text{Spot Price}^2 \times (-100)$$

## Output and Interpretation

The output of the GEX calculation module includes:
*   **Aggregated Net GEX:** The sum of GEX across the entire options chain.
*   **Localized GEX Concentrations:** Identification of specific strike levels where significant gamma exposure exists. These concentrations can indicate "structural overhead walls" (resistance) or "downside trapdoors" (support) where price action might be influenced by dealer hedging.

In a [[../concepts/systematic-options-trading-pipeline-1dte-7dte.md|systematic options trading pipeline]], GEX is a crucial component of the "structural triad," providing insights into potential market turning points or acceleration zones.

## Merged from gex.md (2026-10-02)

# Gamma Exposure (GEX)

**Gamma Exposure (GEX)**, in the context of market risk, typically refers to the aggregate net dealer gamma exposure across the options market for a particular underlying asset or index. It is a crucial metric for understanding market structure and potential feedback loops between options hedging and underlying price movements.

## Significance
*   **Dealer Hedging**: Dealers who sell options (often to retail or institutional buyers) become short gamma. To remain delta-neutral, they must buy the underlying asset as prices rise and sell as prices fall.
*   **Positive GEX**: When dealers are net long gamma, they buy into falling markets and sell into rising markets, acting as a stabilizing force.
*   **Negative GEX**: When dealers are net short gamma, they must sell into falling markets and buy into rising markets. This creates a "gamma squeeze" or "gamma trap," where dealer hedging amplifies price movements, leading to increased volatility and potentially rapid, large price swings.

## Role in Regime Risk Scaling
Within the [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]], GEX serves as a critical absolute filter:
*   **`gex_critical`**: A predefined negative threshold (e.g., -100,000,000 USD per 1% move).
*   **Override Trigger**: If the `current_gex` falls below this `gex_critical` level, it triggers a "NEGATIVE_GEX_RISK_REDUCTION" operational mode. This mode implements specific, often severe, adjustments to [[../concepts/portfolio-greek-limits.md|portfolio Greek limits]] to mitigate risks associated with a dealer short-gamma environment.

## Impact on Portfolio Limits
When a negative GEX override is active, the engine typically:
*   **Contracts Gamma Limits**: Significantly reduces allowable [[../concepts/options-greeks.md|Gamma]] exposure.
*   **Contracts Vega Limits**: Reduces [[../concepts/options-greeks.md|Vega]] exposure.
*   **Widens Delta Limits**: Increases allowable [[../concepts/options-greeks.md|Delta]] exposure to absorb localized spot gaps and prevent over-hedging churn in a volatile environment.

This proactive adjustment helps protect the portfolio from the amplified price movements characteristic of negative GEX regimes.

## Related Concepts
*   [[../concepts/regime-risk-scaling-engine.md|Regime Risk Scaling Engine]]
*   [[../concepts/portfolio-greek-limits.md|Portfolio Greek Limits]]
*   [[../concepts/options-greeks.md|Options Greeks]]

## Merged from gamma-exposure.md (2026-10-02)

**Gamma Exposure (GEX)**, often referring to total market maker GEX, is a critical derivatives-market variable that reflects the aggregate gamma position of market makers in the options market. Gamma measures the rate of change of an option's delta with respect to a change in the underlying asset's price.

The sign and magnitude of GEX have significant implications for market stability and liquidity:

*   **Positive GEX:** When total market maker GEX is deeply positive, it acts as a stabilizing buffer. Market makers, who are typically short gamma, become long gamma overall. To remain delta-neutral, they must buy the underlying asset when prices fall and sell when prices rise. This hedging behavior dampens volatility, creating a mean-reverting effect.
*   **Negative GEX:** When GEX flips negative, market makers become short gamma overall. To hedge, they must sell the underlying asset when prices fall and buy when prices rise. This behavior exacerbates price movements, leading to violent liquidity vacuums and accelerating trends.

In the context of [[../concepts/hidden-markov-models-for-options-trading.md|Hidden Markov Models for options trading]], GEX is a powerful emission input. An HMM can be trained to detect the exact transition into a negative GEX regime, often *before* the price chart displays any clear directional signals. This early detection allows traders to anticipate potential shifts from stable, mean-reverting environments to explosive, trending ones, which is crucial for managing short-term options positions.

## Merged from gamma_exposure_gex.md (2026-10-02)

# Gamma Exposure (GEX)

Gamma Exposure (GEX) is a measure of the sensitivity of an options dealer's delta hedging position to changes in the underlying asset's price. It quantifies the potential impact of options trading on market movements, particularly around key price levels. A high positive GEX suggests dealers are long gamma, meaning they will buy into falling prices and sell into rising prices, potentially dampening volatility. Conversely, negative GEX suggests dealers are short gamma, leading them to sell into falling prices and buy into rising prices, which can exacerbate volatility.

## Calculation Context

GEX calculations are critical for understanding market dynamics, especially for:
*   **0DTE (Zero Days To Expiration) Options:** Highly sensitive to price movements and time decay, requiring frequent updates.
*   **21DTE / 45DTE Options:** Provide a broader view of market positioning over longer timeframes.

## Dollar GEX Formula

The Dollar GEX per contract is typically computed using the following formula, assuming the calculation measures the dollar impact per 1% move in the underlying:

$$	ext{GEX}_{	ext{contract}} = \Gamma 	imes 	ext{Open Interest} 	imes 	ext{Contract Size (100)} 	imes S^2 	imes 0.01$$

Where:
*   $\Gamma$ (Gamma) is the second derivative of the option price with respect to the underlying asset's price.
*   `Open Interest` is the number of outstanding contracts.
*   `Contract Size` is typically 100 shares per option contract.
*   $S$ is the Spot Price of the underlying asset.

## Optimization for GEX Calculation

Efficient GEX calculation, especially across many tickers and expiries, requires:
*   [[../concepts/vectorized_greek_calculation.md]] for rapid Gamma computation.
*   Robust [[../concepts/process_based_parallelism.md]] to handle the computational load.
*   Effective [[../concepts/local_cache_layer.md]] for data ingestion and memory management.
*   A well-defined [[../concepts/intraday_gex_schedule.md]] to capture market shifts.

## Determining GEX Sign

A critical aspect of GEX aggregation is determining the final sign (Positive/Negative GEX) for component summation. This often involves inspecting volume/Open Interest at the Bid vs. Ask or applying institutional heuristics. Further research into this area is explored in [[../research/gex_sign_determination.md]].

## Source

This concept is derived from the [[../sources/gex_compute_pipeline_blueprint.md]].

---
tags: ["options", "greeks", "gamma", "finance"]
created: 2023-10-27
reviewed: false
source_origin: "gex_compute_pipeline.md"
---
