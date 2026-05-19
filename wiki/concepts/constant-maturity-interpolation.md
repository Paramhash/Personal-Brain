yaml
---
tags: ["financial-modeling", "implied-volatility", "interpolation", "option-pricing", "data-processing"]
created: 2023-10-27
reviewed: false
source_origin: "maopm_horizon_spread_blueprint.md"
---
```
# Constant-Maturity Interpolation

**Constant-Maturity Interpolation** is a technique used in financial modeling, particularly in option pricing and volatility surface construction, to derive implied volatility or other option-related metrics for specific, fixed maturities (e.g., 30 days, 180 days) even when no options with those exact expiry dates exist.

Options rarely expire precisely at round numbers like 30 or 180 days. To obtain consistent data points for analysis (such as calculating the [Option-Implied Horizon Spread](../concepts/option-implied-horizon-spread.md)), an interpolation method is applied across the implied volatility surface. This typically involves:
*   Maintaining an active, in-memory matrix of the implied volatility surface across various strikes and expiries.
*   Implementing a localized cubic spline or SABR model parameterization to accurately anchor variance and skew values exactly at the desired constant maturities (e.g., $T=30$ and $T=180$ days) on a daily basis.

This process is a critical component of the State Management & Interpolation Layer within the data infrastructure supporting systems like the [MAOPM architecture for signal fusion](../concepts/maopm-architecture-horizon-spread-gex-fusion.md), ensuring that consistent and comparable data points are available for signal generation.

---