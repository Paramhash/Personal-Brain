---
tags: ["vectorization", "greeks", "gamma", "numpy", "numba", "performance"]
created: 2023-10-27
reviewed: false
source_origin: "gex_compute_pipeline.md"
---
# Vectorized Greek Calculation

Vectorized Greek calculation is an optimization technique used to compute financial Greeks (such as Gamma, Delta, Vega, Theta) for an entire option chain or a large set of options simultaneously, rather than iterating through each option contract individually. This approach leverages the power of array-oriented programming, significantly reducing computation time and improving efficiency, especially for high-performance systems.

## Key Principles

*   **Array Operations:** Instead of scalar operations in a loop, vectorized calculations treat inputs (Spot, Strike, Time to Expiration, Implied Volatility, Risk-free Rate) as arrays or matrices.
*   **Broadcasting:** Libraries like [[../entities/numpy.md]] allow operations between arrays of different shapes, automatically "broadcasting" smaller arrays across larger ones to perform element-wise calculations.
*   **JIT Compilation:** Tools like [[../entities/numba.md]] can Just-In-Time (JIT) compile Python functions to highly optimized machine code, further accelerating numerical computations.

## Gamma ($\Gamma$) Calculation Example

For Gamma Exposure (GEX) calculations, Gamma ($\Gamma$) is a critical input. The standard Spot Gamma formula is:

$$\Gamma = rac{N'(d_1)}{S \sigma \sqrt{T}}$$

Where $N'(d_1)$ is the probability density function of the standard normal distribution evaluated at $d_1$.

By representing $S$ (Spot), $K$ (Strike), $T$ (Time to Expiration), $\sigma$ (Implied Volatility), and $r$ (Risk-free rate) as vectorized [[../entities/numpy.md]] arrays, the entire option chain's Gamma can be computed in a single, highly efficient step. This avoids the performance overhead of line-by-line Black-Scholes pricing.

## Benefits

*   **Speed:** Dramatically faster computation compared to traditional looping.
*   **Efficiency:** Better utilization of CPU resources, especially with multi-core processors when combined with [[../concepts/process_based_parallelism.md]].
*   **Readability:** Often leads to more concise and readable code for mathematical operations.

## Source

This concept is derived from the [[../sources/gex_compute_pipeline_blueprint.md]].