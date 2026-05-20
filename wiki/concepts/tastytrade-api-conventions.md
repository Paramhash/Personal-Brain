---
tags: ["tastytrade", "API", "REST", "JSON", "conventions", "headers", "parameters", "response"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Conventions

The tastytrade API adheres to standard RESTful principles and uses JSON for all request and response bodies.

## Headers

All API requests require specific headers:

*   **`User-Agent`**: Mandatory for all requests. Format: `<product>/<version>` (e.g., `tastytrade-api-client/1.0`). The specific product and version chosen do not matter as long as the format is correct.
*   **`Content-Type`**: Should be `application/json` for requests with a body.
*   **`Accept`**: Should be `application/json` as responses are always in JSON format.
*   **`Accept-Version`**: Used to target a specific API version. The value is a date in `YYYYMMDD` format. Refer to [[../concepts/tastytrade-api-versioning.md|tastytrade API Versioning]] for more details.

## Parameters

### JSON Body Parameters

JSON keys in both request and response bodies are **dasherized**.

**Example:**
```json
{
  "this-key-is-dasherized": "value goes here"
}
```

For `POST`, `PUT`, `PATCH`, and `DELETE` requests, parameters are sent in the JSON request body.

**Example (POST /accounts/{account_number}/orders):**
```json
{
  "underlying-symbol": "AAPL",
  "quantity": 1,
  "time-in-force": "Day"
  // other params here
}
```

### URL Parameters (Query Parameters)

`GET` requests send parameters in the URL as query parameters.

**Array[String] Parameters:**
For parameters of type `Array[String]`, use the format `my-key[]=value`. To send multiple values, repeat the key: `my-key[]=value1&my-key[]=value2`.

## Response Schema

API responses generally follow a consistent JSON structure:

*   **Successful Responses**:
    ```json
    {
      "data": {
        "items": [
          /* list of json objects */
        ]
      },
      "context": "/accounts/{account_number}/positions"
    }
    ```
    Multi-object responses will have an `items` array nested within the `data` object.

*   **Error Responses**:
    ```json
    {
      "error": {
        "code": "not_permitted",
        "message": "User not permitted access"
      }
    }
    ```
    Error responses include an `error` object with `code` and `message` properties. For more details on specific error codes, see [[../concepts/tastytrade-api-error-codes.md|tastytrade API Error Codes]].

This document outlines the fundamental conventions for interacting with the tastytrade API. For a broader understanding, refer back to the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].