---
domain: cl-market-making
tags:
- dlmm
- gex
- market-making-strategy
- findings
aliases: []
created: 2026-10-02
reviewed: false
source_origin: dlmm-f-024-the-wall-envelope-is-routinely-narrower-than-the-sigma-width-so-adr-034-never-binds.md
ingest_hashes:
- a9713374a857b2f0
---
# GEX Intelligence
**In one line:** The component responsible for calculating and interpreting [[gamma-exposure-gex|Gamma Exposure (GEX)]] to identify significant strike levels, such as [[call-wall]] and [[put-wall]], for use in [[range-planning]].
## Intuition
GEX intelligence aims to extract actionable insights from the options market's gamma profile, identifying price levels where dealer hedging activity is concentrated. These levels are then used to inform liquidity deployment decisions, anticipating potential price magnets or resistance/support zones.
## Mechanism / math
The `gex-intelligence` engine typically employs functions like `buildGexProfile` to compute dollar gamma across various strikes. It then identifies the [[call-wall]] and [[put-wall]] by selecting the strikes with peak dollar gamma on their respective sides of the [[spot-price]].
## Where it matters
GEX intelligence is a foundational input for [[cl-market-making|concentrated liquidity market making]] strategies, particularly for defining the [[wall-envelope]] that constrains liquidity deployment ranges. It informs decisions about where to place liquidity and how wide that liquidity should be.
## Evidence and limits
*   **Call Wall Misinterpretation (F-024):** The definition of the [[call-wall]] as the strike with peak dollar gamma led to it routinely sitting very close to the [[spot-price]] (median 0.36% distance), acting as an at-the-money (ATM) "pin" rather than a true upper bound. This caused frequent [[active-bin-out-of-range]] rejections.
*   **Put Wall Effectiveness:** In contrast, the [[put-wall]] (median 14.98% from spot) functioned effectively as a lower bound due to the structural displacement of put open interest.
*   **Design Flaw Identified:** The core issue was not a defect in the GEX calculation itself, but a design flaw in *interpreting* the peak-gamma strike as an upper bound for the [[wall-envelope]]. A peak-gamma strike is a pin, not a ceiling.
*   **Resolution:** [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]] was ratified to address this by redefining wall selection to be side-constrained. This means the call wall must be chosen above spot, and the put wall below spot, ensuring they function as proper bounds. This change requires re-evaluating the impact on the [[wall-envelope]] and the [[deploy-width-sigma-multiple]].
## Related
[[gamma-exposure-gex]], [[call-wall]], [[put-wall]], [[wall-envelope]], [[range-planning]], [[spot-price]], [[active-bin-out-of-range]], [[adr-038-gex-walls-are-selected-on-the-correct-side-of-spot|ADR-038]], [[dlmm-2026-wall-envelope-narrower-than-sigma-width|F-024]]