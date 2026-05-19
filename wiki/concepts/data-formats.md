---
tags: ["API", "Output", "Format", "Data Representation"]
created: 2023-10-27
reviewed: false
source_origin: "openapiv3.yaml"
---
# Data Formats

The [Theta Data v3](../../entities/theta-data-v3.md) API supports several data formats for its responses, allowing users to choose the most suitable representation for their applications. The desired format can typically be specified using the `format` [API Parameter](../concepts/api-parameters.md#format).

## Supported Formats:

*   **CSV (`csv`)**:
    *   Comma-separated values.
    *   A common, human-readable format suitable for spreadsheet applications and simple parsing.
    *   Often the default format.

*   **JSON (`json`)**:
    *   JavaScript Object Notation.
    *   A lightweight, human-readable data interchange format.
    *   Widely used in web APIs for structured data.

*   **NDJSON (`ndjson`)**:
    *   Newline-Delimited JSON.
    *   Each line in the response is a separate JSON object.
    *   Useful for streaming large datasets where each record can be processed independently.

*   **HTML (`html`)**:
    *   HyperText Markup Language.
    *   Returns data formatted for display in a web browser.
    *   Often provided as a convenience for quick viewing.

*   **Python/pandas (`python/pandas`)**:
    *   When using the [ThetaClient (Python Library)](../entities/thetaclient-python-library.md) with `dataframe_type='pandas'`, responses are directly converted into [pandas DataFrames](../entities/pandas-python-library.md).
    *   Ideal for Python users who want to immediately work with data using pandas' extensive analysis capabilities.

*   **Python/polars (`python/polars`)**:
    *   When using the [ThetaClient (Python Library)](../entities/thetaclient-python-library.md) with `dataframe_type='polars'`, responses are directly converted into [polars DataFrames](../entities/polars-python-library.md).
    *   Offers high-performance data processing for Python users, especially with large datasets.

## Specifying the Format:
The `format` parameter is typically an optional query parameter in most API requests. For example:
`http://127.0.0.1:25503/v3/stock/list/symbols?format=json`

When using the Python `ThetaClient`, the `dataframe_type` argument handles the conversion to pandas or polars DataFrames automatically.

---