---
domain: "derivatives"
tags: [volatility-smile, implied-volatility, option-pricing, market-phenomena, skew]
created: 2023-10-27
reviewed: false
source_origin: "appropriate HMM architectures for modeling underlying asset price dynamics relevant to option pricing.md"
---
# Volatility Smile

The volatility smile (or volatility skew) is an empirical phenomenon in options markets where implied volatility for options with the same expiration date but different strike prices is not constant, as predicted by the Black-Scholes model. Instead, a plot of implied volatility against strike price often shows a "smile" or "smirk" shape.

*   **Smile**: Implied volatility is higher for both out-of-the-money (OTM) and in-the-money (ITM) options compared to at-the-money (ATM) options.
*   **Skew**: More commonly, especially in equity markets, implied volatility is higher for OTM put options (lower strikes) than for OTM call options (higher strikes), creating a downward sloping "smirk."

This phenomenon reflects the market's perception of tail risk (e.g., higher probability of extreme downward movements in equities). Models like [[Markov-Modulated Jump-Diffusion (MMJD)]] are capable of generating a pronounced volatility smile and aggressive OTM skew that matches real-world options chains, precisely because they assign a structural probability to tail-risk events. [[Markov-Switching Stochastic Volatility (MS-SV)]] models also excel at fitting the volatility smile and its dynamic evolution.