---
tags: ["data-provider", "options", "greeks", "fintech", "quant-trading"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# ThetaData

ThetaData has emerged as a leading data provider for serious retail quantitative traders, known for its strong price-to-performance ratio in delivering real-time options data.

## Model

ThetaData provides real-time streaming [Options Greeks](../concepts/options-greeks.md) (Delta, Gamma, Vega, Theta) via a local "Theta Terminal." This terminal handles data compression and delivery, making it efficient for users to consume high volumes of data.

## Key Features & Benefits

*   **Real-time Greeks:** Direct access to per-contract Greek values.
*   **Developer-Friendly:** Offers an efficient [Python SDK](../entities/python.md), making it easy for developers to integrate into their trading and analysis workflows.
*   **Cost-Effective:** Positioned as a high-value option for its capabilities.
*   **Raw Chain Access:** Allows users to pull the raw options chain data, enabling local computation and aggregation of metrics like [Gamma Exposure (GEX)](../concepts/gamma-exposure.md) profiles.

## Cost

Approximately $25/month for the Standard plan and up to $60/month for the Pro plan, offering real-time options data.

## Suitability

ThetaData is particularly well-suited for users with powerful local computing resources, such as an [AMD Ryzen Threadripper 3990X](../entities/amd-ryzen-threadripper-3990x.md). These users can leverage their hardware to process the raw options chain data and perform custom calculations and aggregations, such as generating [GEX Divergence dashboards](../concepts/gamma-exposure.md) using parallel processing tools like [Ray](../entities/ray.md) or [multiprocessing](../entities/multiprocessing.md).

It is a core recommendation for the "DIY" approach to options analytics, as detailed in [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md).

---