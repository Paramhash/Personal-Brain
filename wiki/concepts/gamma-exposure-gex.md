---
tags: ["options trading", "market microstructure", "gamma", "gex", "derivatives"]
created: 2023-10-27
reviewed: false
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
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