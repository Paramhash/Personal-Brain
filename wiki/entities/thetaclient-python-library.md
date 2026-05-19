---
tags: ["Python", "Library", "API Client", "Financial Data"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# ThetaClient (Python Library)

`ThetaClient` is a Python library designed to interact with the [Theta Data v3](../../entities/theta-data-v3.md) API. It simplifies the process of requesting and receiving financial market data by providing a convenient programmatic interface.

Users can specify the desired DataFrame type (`pandas` or `polars`) when initializing the client, allowing for direct integration with popular data analysis workflows in Python.

## Usage Example (from Theta Data v3):
```python
from thetadata import ThetaClient
from datetime import date

# Initialize client to return pandas DataFrames
client_pandas = ThetaClient(dataframe_type='pandas')
df_pandas = client_pandas.stock_list_symbols()

# Initialize client to return polars DataFrames
client_polars = ThetaClient(dataframe_type='polars')
df_polars = client_polars.stock_list_symbols()
```

## Related Entities:
*   [Theta Data v3](../entities/theta-data-v3.md)
*   [pandas (Python Library)](../entities/pandas-python-library.md)
*   [polars (Python Library)](../entities/polars-python-library.md)

## Related Concepts:
*   [API Endpoints](../../concepts/api-endpoints.md)
*   [Data Formats](../../concepts/data-formats.md)

---