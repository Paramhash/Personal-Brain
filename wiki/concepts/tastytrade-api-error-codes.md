---
tags: ["tastytrade", "API", "error handling", "HTTP status codes"]
created: 2023-10-27
reviewed: false
source_origin: "api-overview.md"
---
# tastytrade API Error Codes

The tastytrade API uses standard HTTP status codes to indicate the success or failure of a request. When an error occurs, the response body will typically include an `error` object with a `code` and `message` property, as described in [[../concepts/tastytrade-api-conventions.md|tastytrade API Conventions]].

Here are common error codes you might encounter:

*   **`400 Bad Request`**:
    *   **Meaning**: The request was malformed or contained invalid parameters.
    *   **Common Causes**: Missing required parameters, incorrect data types, or invalid format in the request body.

*   **`401 Unauthorized`**:
    *   **Meaning**: The request lacks valid authentication credentials.
    *   **Common Causes**: An expired or invalid access token, or incorrect username/password during login. Refer to [[../concepts/tastytrade-api-authentication.md|tastytrade API Authentication]] for more details.

*   **`403 Forbidden`**:
    *   **Meaning**: The authenticated user does not have permission to access the requested resource.
    *   **Common Causes**: Attempting to access data for an account belonging to a different customer, or lacking the necessary [[../concepts/tastytrade-api-trading-statuses.md|trading privileges]].

*   **`404 Not Found`**:
    *   **Meaning**: The requested endpoint or resource does not exist.
    *   **Common Causes**: Incorrect URL path, or attempting to fetch data for a resource (e.g., a specific order) that does not exist.

*   **`406 Not Acceptable`**:
    *   **Meaning**: The server cannot produce a response matching the list of acceptable values defined in the request's proactive negotiation headers.
    *   **Common Causes**: Most commonly, requesting an unsupported API version via the `Accept-Version` header. See [[../concepts/tastytrade-api-versioning.md|tastytrade API Versioning]].

*   **`422 Unprocessable Content`**:
    *   **Meaning**: The request was well-formed but could not be processed due to semantic errors or business logic rules.
    *   **Common Causes**: An invalid trading action (e.g., an order being rejected by the order system due to market conditions or account restrictions).

*   **`429 Too Many Requests`**:
    *   **Meaning**: The user has sent too many requests in a given amount of time (rate limiting).
    *   **Common Causes**: Exceeding the API's rate limits. Clients should implement exponential backoff or other rate-limiting strategies.

*   **`500 Internal Server Error`**:
    *   **Meaning**: An unexpected error occurred on tastytrade's servers.
    *   **Common Causes**: An issue with the API infrastructure. These responses typically include a support identifier that can be provided to tastytrade support for investigation.

Understanding these error codes helps in debugging and building robust integrations with the tastytrade API. For a general overview, see the [[../concepts/tastytrade-api-overview.md|tastytrade API Overview]].