---
domain: cl-market-making
tags:
- concentrated-liquidity
- range-planning
- volatility-forecasting
- dlmm
- range-width
- strategy
- deployment
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-01-warehouse-manager-cl-inventory-strategy.md
ingest_hashes:
- 7638e82c02c80159
- 51d65d339fbde01d
updated: '2026-10-02'
sources:
- dlmm-01-warehouse-manager-cl-inventory-strategy.md
- dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md
---
# Sigma-Derived Deployed Window
**In one line:** The actual, narrower price range within which a [[cl-position]] is placed, determined by volatility forecasts (sigma) and contained within the broader [[buffered-policy-envelope]].
## Intuition
While the [[buffered-policy-envelope]] provides a safe outer limit, the [[sigma-derived-deployed-window]] aims for optimal capital efficiency. By using volatility forecasts (sigma), the bot can dynamically adjust the width of its liquidity provision to concentrate capital where price is most likely to trade, maximizing fee capture while managing [[impermanent-loss]] exposure.
## Mechanism / math
The source specifies that this window is the "actual CL placement," distinct from the wider [[buffered-policy-envelope]] which serves as the hard deployment boundary. The width of this window is directly related to the forecasted volatility (sigma).
## Where it matters
This window is crucial for the granular deployment of liquidity. Its precise calculation and dynamic adjustment are key to optimizing fee generation and managing the risk-reward profile of a [[cl-position]]. It directly impacts the capital efficiency and profitability of the market-making strategy.
## Evidence and limits
The [[warehouse-manager-cl-inventory-strategy]] explicitly states that the "narrower sigma window" should be used as the "actual CL placement," within the "buffered envelope as the hard deployment boundary." This highlights its role in fine-tuning liquidity provision. The effectiveness of this component depends heavily on the accuracy of the volatility estimation and forecasting.
## Related
[[buffered-policy-envelope]]
[[market-boundaries-cl]]
[[volatility]]
[[cl-position]]
[[m06-volatility-estimation-and-forecasting]]
[[adr-034-range-width-rule-for-fine-binned-pools]]

## Update from dlmm-f-022-the-planner-deploys-the-wall-envelope-as-the-range-and-never-implements-the-ratified-width-rule.md (2026-10-02)

# Sigma-Derived Deployed Window
**In one line:** The actual range of [[dlmm-bins|bins]] where concentrated liquidity is deployed, calculated based on a multiple of forecasted [[implied-volatility|sigma]] and a specified horizon, centered on the active bin, and clamped within the [[wall-envelope]].
## Intuition
Instead of deploying liquidity across a wide, static range, the sigma-derived deployed window aims to concentrate capital more efficiently around the current market price, based on a forecast of how far the price is likely to move within a given time horizon. This allows for higher fee capture per unit of capital while still managing the risk of being out of range.
## Mechanism / math
The calculation of the sigma-derived deployed window follows these steps, as outlined in `range_planning.md` §2b (introduced by [[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]):

1.  **Sigma Horizon:** The expected price movement is estimated using the forecasted [[implied-volatility|sigma]] ($\sigma$) and the square root of the `horizonSeconds`:
    $$ \text{sigmaHorizon} = \sigma \times \sqrt{\text{horizonSeconds}} $$
2.  **Target Half-Width Percentage:** This is determined by applying a `deployWidthSigmaMultiple` to the `sigmaHorizon`:
    $$ \text{targetHalfWidthPct} = \text{deployWidthSigmaMultiple} \times \text{sigmaHorizon} $$
3.  **Target Half Bins:** This percentage is converted into a number of bins:
    $$ \text{targetHalfBins} = \lceil \ln(1 + \text{targetHalfWidthPct}) / \ln(1 + \text{binStep} / 10\_000) \rceil $$
4.  **Clamped Width:** The total width of the deployed window (`width`) is then clamped:
    *   It must be at least `MIN_BINS_PER_POSITION`.
    *   It must not exceed the total width of the [[wall-envelope]] (`envelopeBins`).
    $$ \text{width} = \text{clamp}( 2 \times \text{targetHalfBins} + 1, \text{MIN\_BINS\_PER\_POSITION}, \text{envelopeBins} ) $$
5.  **Centering and Shifting:** The final window of `width` bins is placed **centered on the active bin**. If centering results in an odd remainder, it is allocated to the lower side first. The window is then shifted inward only as far as necessary to remain entirely within the [[wall-envelope]].
## Where it matters
*   **Capital Efficiency:** By deploying a narrower, dynamically adjusted window, liquidity is concentrated where it is most likely to earn fees, improving capital efficiency.
*   **Fee Yield vs. Out-of-Range Risk:** The `deployWidthSigmaMultiple` allows for a trade-off: a smaller multiple increases fee yield per unit of capital but raises the risk of the price moving out of range, while a larger multiple reduces out-of-range events but dilutes fee capture.
*   **Accurate Performance Measurement:** As demonstrated by [[dlmm-2026-planner-deploys-wall-envelope|F-022]], correctly implementing this window is crucial for accurate [[hedge-churn-artifact|hedge churn]] and [[fee-yield|fee yield]] measurements, as a wider assumed range (like the full [[wall-envelope]]) significantly understates inventory sensitivity.
## Evidence and limits
[[dlmm-2026-planner-deploys-wall-envelope|F-022]] highlighted a critical implementation gap where the planner was deploying the full [[wall-envelope]] instead of this narrower, sigma-derived window. This led to previous [[hedge-churn-artifact|hedge churn]] figures being understated by approximately 4.64x. The resolution of F-022 corrected this, ensuring that the deployed range is now a 203-bin window (in one observed case) inside a wider 402-bin envelope, leading to more accurate risk and performance assessments.

The `deployWidthSigmaMultiple` is still an unratified parameter, defaulting to 1, and its optimal value requires further research.
## Related
[[range-planning]]
[[wall-envelope]]
[[deploy-width-sigma-multiple]]
[[dlmm-bins]]
[[implied-volatility]]
[[hedge-churn-artifact]]
[[fee-yield]]
[[adr-034-range-width-rule-for-fine-binned-pools|ADR-034]]
[[dlmm-2026-planner-deploys-wall-envelope]]

---
