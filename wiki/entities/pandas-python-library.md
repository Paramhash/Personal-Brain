---
tags: ["Python", "Library", "Data Analysis", "Dataframes"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# pandas (Python Library)

Pandas is a fast, powerful, flexible, and easy-to-use open-source data analysis and manipulation tool, built on top of the Python programming language. It is widely used for working with tabular data, often in the form of DataFrames.

In the context of the [Theta Data v3](../../entities/theta-data-v3.md) API, `pandas` is one of the supported `dataframe_type` options when using the [ThetaClient (Python Library)](../entities/thetaclient-python-library.md) to retrieve data. This allows users to directly receive API responses as pandas DataFrames, facilitating further data analysis and manipulation within the Python ecosystem.

## Usage Example (from Theta Data v3):
```python
from thetadata import ThetaClient
from datetime import date

client = ThetaClient(dataframe_type='pandas')
df = client.stock_list_symbols()
```

## Related Entities:
*   [ThetaClient (Python Library)](../entities/thetaclient-python-library.md)
*   [polars (Python Library)](../entities/polars-python-library.md)

## Related Concepts:
*   [Data Formats](../../concepts/data-formats.md)

---