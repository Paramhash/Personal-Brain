yaml
---
tags: ["MAOPM", "option-pricing", "market-making", "signal-fusion", "horizon-spread", "GEX", "architecture", "financial-systems"]
created: 2023-10-27
reviewed: false
source_origin: "maopm_horizon_spread_blueprint.md"
---
```
# MAOPM Architectural Blueprint: Option-Implied Horizon Spread & GEX Signal Fusion

This blueprint details the integration of the [Option-Implied Horizon Spread](../concepts/option-implied-horizon-spread.md) alongside [Gamma Exposure (GEX)](../concepts/gamma-exposure-gex.md) within a [Multi-Agent Option Pricing & Market-Making (MAOPM)](../concepts/multi-agent-option-pricing-market-making-maopm.md) architecture. This fusion addresses a multi-frequency signal processing challenge by pairing a macro-driven structural shift indicator with a high-frequency microstructure indicator, bridging the gap between order-flow dynamics and macroeconomic regime changes.

## 1. Multi-Agent Signal Fusion Architecture

In the MAOPM architecture, signals are fused using a hierarchical, state-dependent gating network, rather than simple linear blending. This two-layer multi-agent framework allows a macro agent to modify the prior distributions or risk parameters of microstructure agents.

```
                  +-----------------------------------+
                  |        Macro Regime Agent         |
                  |     (Horizon Spread Evaluation)   |
                  +-----------------+-----------------+
                                    |
                    Outputs: Posterior Regime Prob.
                    (P_macro) & Volatility Skew Shift
                                    |
                                    v
                  +-----------------+-----------------+
                  |      Gating & Context Engine      |
                  |    (Dynamic Parameter Mapping)    |
                  +-----------------+-----------------+
                                    |
               Modifies: Position Limits, Hedging Speed, 
                         GEX Z-Score Thresholds
                                    |
                                    v
    +-------------------------------+-------------------------------+
    |                               |                               |
    v                               v                               v
+-----------------------+   +-----------------------+   +-----------------------+
|  Market Maker Agent   |   |   Delta Hedging Agent |   |  Statistical Arbitr.  |
| (Bid/Ask Skew & Vol)  |   | (Rebalancing Urgency) |   |    (Skew Arbitrage)   |
+-----------------------+   +-----------------------+   +-----------------------+
```

### Layer 1: The Macro Regime Agent (The Horizon Spread)
*   **Role:** Computes the structural posterior probability ($P_{\text{macro}}$) of being in an expansionary, compressed risk premium, or systemic crisis regime.
*   **Mechanism:** Leverages the [Option-Implied Horizon Spread](../concepts/option-implied-horizon-spread.md), which possesses minimal mass in the "indecisive zone" ([Lai, 2022](../sources/lai-2022-horizon-spread.md)), outputting highly confident, binary-leaning regime state weights.
*   **Operational Frequency:** Evaluated hourly/daily or triggered asynchronously when the spread crosses historical standard deviation boundaries.

### Layer 2: Microstructure Execution Agents (GEX & Regime Divergence)
*   **Role:** Manages intra-day liquidity provisioning, order-book profiling, and inventory rebalancing.
*   **Mechanism:** Utilizes [GEX](../concepts/gamma-exposure-gex.md) Z-scores and the Regime Divergence Ratio (RDR) to map local dealer positioning and predict immediate localized price acceleration or pinning effects.

### The Fusion Matrix (How They Complement)
The Macro Agent acts as a parametric filter over the Microstructure Execution Agents, modifying execution constraints rather than directly altering the trade execution loop:

*   **Low Vol / Positive Macro Regime (Normal Horizon Spread):** Microstructure agents operate with default parameters. [GEX](../concepts/gamma-exposure-gex.md) models dictate local boundaries; short gamma positions are scaled normally, and mean-reversion market-making engines operate with tight spreads.
*   **Macro Regime Divergence (Negative/Inverting Horizon Spread, GEX still Normal):** This condition, observed in December 2019, indicates long-dated risk premium expansion while front-month options remain cheap.
    *   **Action:** The Gating Engine systematically clips maximum inventory risk limits for market-making agents and widens the baseline bid-ask spread matrix, anticipating a high-impact structural break. The Delta Hedging Agent is forced to shorten rebalancing intervals, shifting from time-based (15-minute) to tight delta-band-based rebalancing.
*   **Systemic Crisis Regime (Inverted Horizon Spread + GEX Z-score < -2):** Microstructure agents adopt an aggressive defensive posture, transitioning from liquidity provisioning to inventory liquidation and tail-risk protection.

## 2. Near-Real-Time Data Infrastructure Requirements

To calculate the option-implied equity risk premium (ERP) at 30-day and 180-day horizons in near-real-time, the system must ingest full option chains, strip out risk-free rates/dividend yields via put-call parity, extract the [risk-neutral probability density functions ($Q$-measure)](../concepts/risk-neutral-vs-physical-measures.md), and contrast them against a rolling [physical drift ($P$-measure)](../concepts/risk-neutral-vs-physical-measures.md).

### Minimum Infrastructure Stack
To avoid lag, computation is decoupled into an Ingestion Pipeline and an Analytical Engine:

*   **Ingestion Layer (Kafka / Redpanda Cluster):** A distributed message bus for raw tick-by-tick options traffic (hundreds of thousands of messages per second at peak).
*   **State Management & Interpolation Layer (Flink / Faust):**
    *   Maintains an active, in-memory matrix of the implied volatility surface across strikes.
    *   **[Constant-Maturity Interpolation](../concepts/constant-maturity-interpolation.md):** Implements localized cubic spline or SABR model parameterization to anchor variance and skew exactly at $T=30$ and $T=180$ daily.
*   **Compute Engine (Rust / C++ or optimized Python/Vectorized Node.js):**
    *   Extracts risk-neutral expectations by numerically integrating across implied variance curves (e.g., Bakshi-Kapadia-Madand method or Carr-Madan formulation).
    *   Updates the horizon spread metric at fixed time-intervals or structural delta-volume buckets (e.g., every 10 seconds or 1,000 contracts traded), as macro premiums do not evolve at sub-second scales.

## 3. Provider Suitability: ThetaData vs. Polygon.io

To compute the horizon spread at high granularity, continuous, clean, per-strike bid/ask quotes for SPX/SPY (or underlying equities) at both near and mid-term expiries are required.

| Feature Requirement | [Polygon.io](../entities/polygon-io.md) | [ThetaData](../entities/thetadata.md) |
| :--- | :--- | :--- |
| **Data Feed Type** | Tick-level trades and quotes via WebSockets. | Rest API for historical; specialized binary WebSockets for streaming. |
| **Granularity** | Millisecond-level tick data. | Nanosecond/microsecond-level contract events. |
| **Chain Architecture** | Flat message streams. Emits individual tick events per contract identifier. | Hierarchical framing. Allows structuring queries by underlying or root symbol. |
| **Implied Vol / Greek Engines** | Raw data provided. User must calculate surface, interpolation, and greeks locally. | Pre-calculated real-time greeks and IV surfaces built directly into the data tier. |
| **Compute Overhead** | **High.** You must construct the entire order book and IV surface from raw ticks manually. | **Low.** You can stream pre-calculated IV matrices or sample specific tenors efficiently. |

### Architectural Recommendation
*   **Go with [Polygon.io](../entities/polygon-io.md) if:** You require a pure, un-opinionated, ultra-low-latency raw firehose, and your setup includes a dedicated 64-core compute cluster running an in-memory database to build custom SABR or local volatility surface models from raw ticks.
*   **Go with [ThetaData](../entities/thetadata.md) if:** You aim to minimize immediate infrastructure overhead. [ThetaData](../entities/thetadata.md) handles the compute-heavy step of building the IV surface and calculating real-time greeks on their servers, allowing your MAOPM data ingestion agent to pull clean, pre-filtered 30-day and 180-day constant-maturity variance profiles directly. This offloads significant processing debt from your local network gateway, enabling your system to focus resources on agent decision-making and risk-mitigation logic.

---