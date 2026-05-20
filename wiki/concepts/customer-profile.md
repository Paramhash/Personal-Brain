---
tags: ["customer", "profile", "api-model", "tastyworks", "identity", "contact", "regulatory"]
created: 2023-10-27
reviewed: false
source_origin: "accounts-and-customers.md"
---
# Customer Profile (Tastyworks API)

The Customer Profile concept in the Tastyworks API revolves around the `Customer` data model and the `GET /customers/{customer_id}` endpoint, which allows retrieval of a customer's comprehensive personal and account-related information.

## Get Customer Endpoint

Retrieves the full profile for a customer.

**Request**

```
GET /customers/{customer_id}
```

**Path Parameters**

*   `customer_id` (string, Required): The customer identifier. The literal string `me` can be used to reference the currently authenticated customer, avoiding the need to know or store their internal ID.

**Query Parameters**

*   `allow-missing` (boolean, Optional): If `true`, returns a partial result even if some customer data is unavailable.

**Response** — `200 OK`

Returns a `Customer` object.

## Customer Data Model

The `Customer` object describes the full customer profile, encompassing personal information, contact details, regulatory status, and account application state.

### Identity

*   `id` (string): The internal customer identifier. (Use `me` in API paths instead of this value).
*   `first-name` (string): Customer's first name.
*   `last-name` (string): Customer's last name.
*   `middle-name` (string): Customer's middle name.
*   `prefix-name` (string): Name prefix (e.g., Mr., Mrs., Dr.).
*   `suffix-name` (string): Name suffix (e.g., Jr., III).
*   `first-surname` (string): First surname (used in some regional naming conventions).
*   `second-surname` (string): Second surname (used in some regional naming conventions).
*   `gender` (string): Customer's gender.
*   `birth-date` (string): Customer's date of birth.
*   `birth-country` (string): Customer's country of birth.
*   `user-id` (string): The customer's user ID for authentication.
*   `external-id` (string): External identifier for the customer.

### Contact Information

*   `email` (string): Customer's email address.
*   `home-phone-number` (string): Home phone number.
*   `mobile-phone-number` (string): Mobile phone number.
*   `work-phone-number` (string): Work phone number.
*   `address` (object): Primary residential address.
*   `mailing-address` (object): Mailing address (if different from residential).

### Citizenship & Tax

*   `citizenship-country` (string): Customer's country of citizenship.
*   `usa-citizenship-type` (string): Type of US citizenship (e.g., citizen, resident alien, non-resident alien).
*   `is-foreign` (string): Whether the customer is classified as a foreign person.
*   `regulatory-domain` (string): The regulatory domain the customer falls under.
*   `tax-number` (string): Tax identification number (SSN or ITIN for US customers).
*   `tax-number-type` (string): Type of tax number provided.
*   `foreign-tax-number` (string): Foreign tax identification number (for non-US customers).
*   `subject-to-tax-withholding` (boolean): Whether the customer is subject to backup tax withholding.
*   `visa-type` (string): Visa type (for non-citizen residents).
*   `visa-expiration-date` (string): Visa expiration date.

### Affiliations & Disclosures

*   `has-industry-affiliation` (boolean): Whether the customer has an affiliation with a FINRA member firm.
*   `industry-affiliation-firm` (string): Name of the affiliated FINRA member firm.
*   `has-listed-affiliation` (boolean): Whether the customer is affiliated with a publicly listed company.
*   `listed-affiliation-symbol` (string): The ticker symbol of the affiliated listed company.
*   `has-political-affiliation` (boolean): Whether the customer has a political affiliation requiring disclosure.
*   `political-organization` (string): Name of the political organization.
*   `has-institutional-assets` (string): Whether the customer has institutional-level assets.
*   `is-investment-adviser` (string): Whether the customer is a registered investment adviser.
*   `family-member-names` (string): Names of family members (for affiliated person disclosures).

### Account Application & Status

*   `has-pending-or-approved-application` (string): Whether the customer has a pending or approved account application.
*   `permitted-account-types` (string): Account types the customer is permitted to open.
*   `is-professional` (boolean): Whether the customer is classified as a professional for market data purposes.
*   `has-delayed-quotes` (boolean): Whether the customer receives delayed (rather than real-time) quotes.
*   `created-at` (datetime): Timestamp when the customer record was created.

### Agreements

*   `agreed-to-margining` (boolean): Whether the customer has agreed to the margin agreement.
*   `agreed-to-terms` (boolean): Whether the customer has agreed to the terms of service.
*   `signature-of-agreement` (boolean): Whether the customer has signed the account agreement.

### Related Objects

*   `customer-suitability` (object): Nested suitability questionnaire responses.
*   `entity` (object): Entity details (for entity/trust/corporate accounts).
*   `person` (object): Person details (additional personal information).
*   `identifiable-type` (string): The type of identifiable entity (e.g., `person`, `entity`).
*   `desk-customer-id` (string): Internal desk customer identifier.
*   `ext-crm-id` (string): External CRM identifier.

Customers typically have one or more associated brokerage accounts. For details on managing these, see [[../concepts/account-management.md]].

---