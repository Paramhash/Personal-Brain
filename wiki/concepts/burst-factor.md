---
domain: cl-market-making
tags:
- market-microstructure
- price-dynamics
- dlmm
- hedging
aliases: []
created: '2026-10-02'
reviewed: false
source_origin: dlmm-ev-gate-calibration-2026-10-01.md
ingest_hashes:
- 0e6227858a6c4458
---
# Burst factor
**In one line:** A quantitative measure indicating the extent to which a financial asset's price movements deviate from a continuous Gaussian process, exhibiting periods of stasis followed by sudden, discrete jumps or "bursts."
## Intuition
In many real-world markets, prices do not change continuously. Instead, they often remain at a certain level for some time, then move abruptly to a new level. This "bursty" behavior means that for a given level of overall volatility, there are fewer actual price changes (and thus fewer opportunities for trades or hedging) than a purely continuous model (like a Gaussian random walk) would suggest.
## Mechanism / math
The source quantifies the [[burst-factor]] by comparing the expected absolute return `E|r|` to the theoretical value for a Gaussian process `sd·√(2/π)`:
$$ \text{Burst Factor} = \frac{E|r|}{\text{sd} \cdot \sqrt{2/\pi}} $$
Where:
*   `E|r|` is the expected absolute value of returns over a given interval (e.g., 30 seconds).
*   `sd` is the standard deviation of returns over the same interval.
*   `√(2/π)` is a constant derived from the expected absolute value of a standard normal random variable.

A [[burst-factor]] value less than 1 indicates burstiness. For the DLMM pool's active bin, the source found a burst factor of approximately 0.739, implying that the pool trades 1.35x less than a Gaussian model would assume for the same variance. This is also correlated with the percentage of unchanged observations (e.g., 50.6% for the pool vs. 0.1% for Deribit spot over 30-second intervals).
## Where it matters
The [[burst-factor]] directly impacts the accuracy of hedge turnover and [[hedge-drag]] calculations in [[cl-market-making]] models like the [[ev-gate]]. A lower [[burst-factor]] implies less frequent hedging activity for a given volatility, leading to lower actual hedging costs than a continuous model would predict. Ignoring this factor can lead to an overestimation of hedging costs and suboptimal liquidity deployment decisions.
## Evidence and limits
The [[dlmm-2026-ev-gate-calibration|EV gate calibration]] effort identified the pool's [[burst-factor]] as a key explanation for the initial overstatement of [[hedge-drag]] in the [[ev-gate]] model. Incorporating this factor, alongside the pool's lower [[realized-volatility]], brought the model's hedge cost estimates into close agreement with simulator results. The factor can vary daily and depends on market conditions and pool activity, necessitating continuous monitoring and potential recalibration.
## Related
[[ev-gate-calibration]]
[[hedge-drag]]
[[realized-volatility]]
[[dlmm-bins]]
[[cl-market-making]]
[[ev-gate]]