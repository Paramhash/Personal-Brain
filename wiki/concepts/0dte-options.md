yaml
---
tags: ["finance", "options-trading", "derivatives", "real-time-data"]
created: 2023-10-27
reviewed: false
source_origin: "gemini-code-1779189680884.py"
---
# 0DTE Options (Zero Days To Expiration)

**0DTE Options** refers to options contracts that expire on the same day they are traded. These instruments are characterized by their extremely short lifespan and highly dynamic behavior.

## Characteristics
*   **Hyper-Frequent Tracking**: Due to their imminent expiration, 0DTE options require continuous, real-time tracking.
*   **Rapid Strike Shifts**: Strike prices can shift rapidly throughout the trading day as the underlying asset moves.
*   **Fast Time Decay (Theta)**: The value of 0DTE options decays extremely quickly as time passes, making their pricing and risk profiles highly sensitive to even small time increments.
*   **High Gamma Sensitivity**: They exhibit high gamma, meaning their delta (sensitivity to underlying price changes) changes rapidly with small movements in the underlying asset.

## Processing Implications
The real-time and high-frequency nature of 0DTE options makes them particularly susceptible to data freshness mismatches if processed alongside slower-moving data. Architectures that attempt to force 0DTE data into a [[../concepts/unified-2d-matrix-anti-pattern.md|unified 2D matrix]] with longer-dated options will suffer from significant bottlenecks, as the rapid updates required for 0DTE would be delayed by the slower processing of other expiries.

For optimal processing, 0DTE data should be handled by dedicated, high-speed [[../concepts/parallel-data-pipelines.md|parallel data pipelines]] as part of a broader [[../concepts/pipeline-decoupling-strategy.md|pipeline decoupling strategy]].

---
Source: [[../sources/gemini-code-1779189680884.md|gemini-code-1779189680884.py]]