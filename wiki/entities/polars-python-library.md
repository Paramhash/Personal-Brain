---
tags: ["Python", "Library", "Data Analysis", "Dataframes", "Performance"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# polars (Python Library)

Polars is a DataFrame library for Rust and Python that is designed for high performance. It leverages a columnar data structure and parallel processing to offer significantly faster operations compared to traditional DataFrame libraries like pandas, especially for large datasets.

In the context of the [Theta Data v3](../../entities/theta-data-v3.md) API, `polars` is one of the supported `dataframe_type` options when using the [ThetaClient (Python Library)](../entities/thetaclient-python-library.md) to retrieve data. This allows users to directly receive API responses as Polars DataFrames, which can be beneficial for performance-critical data processing workflows in Python.

## Usage Example (from Theta Data v3):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='polars')
df = client.stock_list_symbols()
```

## Related Entities:
*   [ThetaClient (Python Library)](../entities/thetaclient-python-library.md)
*   [pandas (Python Library)](../entities/pandas-python-library.md)

## Related Concepts:
*   [Data Formats](../../concepts/data-formats.md)

---