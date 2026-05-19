---
tags: ["finance", "quantitative-finance", "options", "risk-management", "volatility-surface", "erp"]
created: 2023-10-27
reviewed: false
source_origin: "/raw/gemini-code-1779191063341.py"
---
# Option-Implied Horizon Spread (IHS)

The **Option-Implied Horizon Spread ($\Delta \text{IHS}$)** is a derived metric in quantitative finance that measures the difference in the [[../concepts/equity-risk-premium.md|Equity Risk Premium (ERP)]] between different maturities, typically a longer-dated and a shorter-dated horizon. It provides insights into how market participants' risk perceptions and expectations for future returns vary across the term structure of options.

## Construction
The $\Delta \text{IHS}$ is constructed by taking the difference between the long-dated and short-dated $Q$-measure equity risk premium profiles, which are isolated using techniques described in [[../concepts/q-measure-equity-risk-premium-isolation.md|Q-Measure Equity Risk Premium Isolation]]. For example, comparing 180-day and 30-day maturities:

$$\Delta \text{IHS} = \text{ERP}_{180} - \text{ERP}_{30}$$

Substituting the spanned log contract values and risk-neutral moments:

$$\Delta \text{IHS} = \left[ E^P_{180} - E^P_{30} \right] - \left[ \left((r_{180} - d_{180})T_{180} - \frac{1}{2}V_Q(180)\right) - \left((r_{30} - d_{30})T_{30} - \frac{1}{2}V_Q(30)\right) \right]$$

Where:
*   $E^P_T$ is the expected log return under the [[../concepts/physical-measure.md|P-measure]] at maturity $T$.
*   $r_T$ is the risk-free rate at maturity $T$.
*   $d_T$ is the continuous dividend yield at maturity $T$.
*   $V_Q(T)$ is the [[../concepts/bakshi-kapadia-madan-formulation.md|Q-measure model-independent variance]] at maturity $T$.

## Significance
*   **Term Structure of Risk**: $\Delta \text{IHS}$ reflects the market's view on how risk and expected returns evolve over different time horizons.
*   **Early Warning Indicator**: A severe contraction or negative turn in $\Delta \text{IHS}$, especially when accompanied by low historical volatility, can signal expanding long-dated downside tail-hedging demand. This suggests that market participants are quietly preparing for potential future downside risks, even if immediate spot market indicators remain calm.
*   **Microstructure Adjustment**: Such signals can trigger adjustments in automated trading systems or risk management frameworks, allowing for proactive responses to shifts in market sentiment and underlying risk profiles.