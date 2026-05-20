---
tags: ["options-pricing", "quantitative-finance", "risk-neutral-density", "implied-volatility", "theorem"]
created: 2023-10-27
reviewed: false
source_origin: "HMM-derived probability estimates compare to other methods.md"
---
# Breeden-Litzenberger Theorem

The Breeden-Litzenberger (1978) theorem is a fundamental result in financial economics that establishes a direct relationship between the prices of European call options and the [[../concepts/risk-neutral-density-rnd.md|risk-neutral probability density function (RND)]] of the underlying asset's price at expiration.

## Statement of the Theorem

The theorem states that, under certain assumptions (such as continuous trading, no arbitrage, and a complete market), the risk-neutral probability density function $f(S_T = K)$ of the underlying asset's price ($S_T$) at expiration ($T$) being equal to a specific strike price ($K$) is proportional to the second derivative of the call option price ($C$) with respect to that strike price:

$$f(S_T = K) = e^{rT} \frac{\partial^2 C}{\partial K^2}$$

Where:
*   $S_T$ is the asset price at expiration
*   $K$ is the strike price
*   $r$ is the risk-free rate
*   $T$ is the time to expiration
*   $C$ is the European call option price

## Implications and Applications

*   **Extraction of RND:** The theorem provides a non-parametric method to extract the market's implied [[../concepts/risk-neutral-density-rnd.md|risk-neutral probability distribution]] directly from observed option prices across a range of strike prices. This is a powerful tool for understanding market sentiment and expectations about future price movements.
*   **Market Expectations:** By analyzing the shape of the RND curve, one can infer market expectations regarding skewness (e.g., fat tails, probability of extreme events) and kurtosis (e.g., peakedness) of future price distributions.
*   **Strike Selection:** In options trading, particularly for strategies like spreads, the RND derived via Breeden-Litzenberger can be used to precisely select strike prices that align with specific probability targets.

## Limitations

*   **European Options:** The theorem strictly applies to European-style options, which can only be exercised at expiration.
*   **Continuity and Differentiability:** It assumes that option prices are twice differentiable with respect to strike price, which may require interpolation or smoothing of observed market data.
*   **No Arbitrage:** The underlying assumption of no arbitrage opportunities is crucial.

The Breeden-Litzenberger theorem is a cornerstone for understanding and utilizing the information embedded in the options market's [[../concepts/implied-volatility.md|implied volatility]] surface.