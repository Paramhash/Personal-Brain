yaml
---
tags: ["technology", "database", "cache", "in-memory-store"]
created: 2023-10-27
reviewed: false
source_origin: "gemini-code-1779189680884.py"
---
# Redis

**Redis** (Remote Dictionary Server) is an open-source, in-memory data structure store, used as a database, cache, and message broker. It supports various data structures such as strings, hashes, lists, sets, sorted sets with range queries, bitmaps, hyperloglogs, and geospatial indexes with radius queries.

## Role in Data Pipelines
In the context of [[../concepts/parallel-data-pipelines.md|parallel data pipelines]], Redis serves as an excellent choice for a lightweight, shared memory cache or central state controller. Its high performance and ability to handle frequent read/write operations make it ideal for pipelines to write their processed metrics and for other components to quickly retrieve the latest state.

---
Source: [[../sources/gemini-code-1779189680884.md|gemini-code-1779189680884.py]]