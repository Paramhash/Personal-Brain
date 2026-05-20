---
tags: ["tastytrade", "api", "errors", "http-headers", "authentication"]
created: 2023-10-27
reviewed: false
source_origin: "faq.md"
---
# 401 Authorization Required Error (User-Agent Specific)

A `401 Authorization Required` error can occur even with valid credentials if the `User-Agent` HTTP header does not meet specific [[./tastytrade-api-conventions.md|tastytrade API Conventions]].

## Requirement

The `User-Agent` header **must** follow the format: `<product>/<version>`.

## Example Error Response

If the `User-Agent` header is malformed or missing, you might receive a response similar to this:

```html
<html>
<head>
  <title>401 Authorization Required</title>
</head>
<body>
  <center>
    <h1>401 Authorization Required</h1>
  </center>
  <hr>
  <center>nginx</center>
</body>
</html>
```

## Resolution

Ensure all API requests include a `User-Agent` header formatted as `<your_product_name>/<your_product_version>`.

## Related Concepts

*   [[../entities/tastytrade.md|tastytrade]]
*   [[./tastytrade-api-conventions.md|tastytrade API Conventions]]
*   [[./tastytrade-auth-patterns.md|tastytrade Auth Patterns]]

---
*This information is derived from the tastytrade API FAQ.*