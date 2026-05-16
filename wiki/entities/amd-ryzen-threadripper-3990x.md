---
tags: ["hardware", "cpu", "high-performance-computing", "quant-trading", "workstation"]
created: 2023-10-27
reviewed: false
source_origin: "Data provider that provides real-time Greeks.md"
---
# AMD Ryzen Threadripper 3990X

The AMD Ryzen Threadripper 3990X is a high-end desktop processor known for its exceptional core and thread count, making it a powerful tool for computationally intensive tasks.

## Specifications

*   **Cores/Threads:** 64 Cores / 128 Threads
*   **Architecture:** Zen 2
*   **Target Use:** Content creation, scientific computing, virtualization, and high-performance workstations.

## Relevance to Quantitative Finance

In the context of quantitative finance and options trading, the 3990X's high core count offers a unique advantage:

*   **Local Computation:** It enables users to perform complex calculations, such as deriving [Options Greeks](../concepts/options-greeks.md) and aggregating [Gamma Exposure (GEX)](../concepts/gamma-exposure.md) profiles, locally rather than relying on pre-calculated data from providers. This can lead to cost savings and greater control over the analytical process.
*   **Parallel Processing:** Its 128 threads are ideal for parallelizing tasks like processing real-time market data for hundreds of stocks simultaneously, using tools such as [multiprocessing](../entities/multiprocessing.md) or [Ray](../entities/ray.md).
*   **Data Ingestion:** It can efficiently handle high-bandwidth data streams from providers like [Polygon.io](../entities/polygon-io.md) or [ThetaData](../entities/thetadata.md), allowing for comprehensive real-time analysis.

The 3990X's capabilities are a central factor in the "cost vs. computation" trade-off when selecting [Real-time Options Greeks Data Providers](../concepts/real-time-options-greeks-data-providers.md). Its presence can shift the optimal strategy towards acquiring raw data and performing calculations in-house.

Further details on leveraging such hardware for options analytics can be found in [Optimizing Greek Calculations with Ray and Multiprocessing](../research/optimizing-greek-calculations-with-ray.md).

---