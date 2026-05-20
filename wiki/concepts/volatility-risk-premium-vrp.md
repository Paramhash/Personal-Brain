---
tags: ["options trading", "volatility", "VRP", "implied volatility", "realized volatility"]
created: 2023-10-27
reviewed: false
source_origin: "combine hmm, gex profile, iv-hv skew to form structural triad used by advanced systematic options traders .md"
---
# Volatility Risk Premium (VRP)

The Volatility Risk Premium (VRP) is a fundamental concept in options trading, representing the difference between the market's expectation of future volatility (Implied Volatility, IV) and the actual volatility realized over a period (Realized Volatility, RV). A positive VRP suggests that options are priced to reflect higher future volatility than what has historically occurred, often indicating a premium that can be harvested by options sellers.

## Calculation Module

The VRP module within a [[../concepts/systematic-options-trading-pipeline-1dte-7dte.md|systematic options trading pipeline]] typically involves these steps:

1.  **Realized Volatility (RV):**
    *   Computes a rolling close-to-close log return volatility over a short lookback window (e.g., 10-day, 20-day annualized). This captures the current "speed" of the market.

2.  **Implied Volatility (IV):**
    *   Isolates the At-The-Money (ATM) Implied Volatility specifically for the target trading expirations (e.g., 1DTE to 7DTE). This represents the market's forward-looking expectation of volatility for those short-term options.

3.  **Volatility Risk Premium (VRP):**
    *   Calculates the arithmetic or geometric spread between IV and RV:
        $$\text{VRP} = \text{IV}_{\text{ATM}} - \text{RV}$$

## Significance

A high VRP can signal an attractive environment for selling options premium, as the market is pricing in a greater degree of future uncertainty than historical data suggests. Conversely, a low or negative VRP might indicate that options are cheap relative to historical volatility, potentially favoring options buyers or signaling caution for sellers. VRP is a critical component of the "structural triad" used by advanced systematic options traders.