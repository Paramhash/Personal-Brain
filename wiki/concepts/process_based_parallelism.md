---
tags: ["parallel-computing", "python", "performance", "multiprocessing"]
created: 2023-10-27
reviewed: false
source_origin: "gex_compute_pipeline.md"
---
# Process-Based Parallelism

Process-Based Parallelism is a strategy for achieving concurrent execution by spawning multiple independent processes, each with its own Python interpreter and memory space. This approach is crucial in Python for computationally intensive tasks because it effectively bypasses the [[../entities/python_global_interpreter_lock_gil.md]] (GIL), which otherwise limits true parallel execution of CPU-bound threads within a single process.

## Implementation in Python

In Python, process-based parallelism can be implemented using:
*   The built-in `multiprocessing` module.
*   The `concurrent.futures.ProcessPoolExecutor` for a higher-level interface.

## Compute Distribution Model (Ticker Chunks)

For workloads like high-performance Gamma Exposure (GEX) calculations across numerous tickers, a common distribution model involves:
*   **Worker Pools:** Mapping physical CPU cores (e.g., on a [[../entities/amd_threadripper_3990x.md]]) to a distributed pool of worker processes.
*   **Chunking:** Dividing the total workload (e.g., 500 component tickers) into smaller, manageable chunks. Each worker process is assigned one or more tickers to process independently.
*   **Inside the Worker:** An individual worker process is responsible for fetching raw option chain data for its assigned ticker, filtering for specific expiries (0DTE, 21DTE, 45DTE), calculating contract-level GEX, and aggregating the results.

This model ensures that each core is fully utilized without being bottlenecked by the GIL, maximizing parallel efficiency.

## Source

This concept is derived from the [[../sources/gex_compute_pipeline_blueprint.md]].