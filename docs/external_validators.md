# External Validation

For more details, see the [External Validator](/documentation/external-validator-service-generator/) documentation.

External validation allows document validation logic to be delegated to an external API service. This enables the use of custom or proprietary logic that is outside the scope of internal rule-based validators.

---

## Overview

- External validators are tied to a specific **document type**.
- The system sends a request to an external API, which returns validation issues (errors or warnings).
- External validators support **custom severity**, **field-level** or **global messages**, and **position metadata**.

---

## Registering an External Validator

To register an external validator, use the following endpoint:

### Request

```http
POST /api/v5/document-types/{documentTypeId}/external-validators
```

Body
```json
{
  "name": "ExampleValidator",
  "url": "https://external.validator.com"  // Must expose /validate endpoint
}
```

### External API Requirements
Your external validator must expose the following HTTP endpoint:

```http
POST {external_validator_url}/validate
```

Request Body
```json
{
  "documentId": "string",         // ID of the document to validate
  "documentTypeId": "string"      // ID of the document type
}
```

Response Format
The external API must return a response in the following structure:

Response Format
```json
{
  "validationResult": {
    "issues": [
      {
        "code": "F123abc456",
        "errors": [
          {
            "severity": "error",
            "type": "FormatError",
            "message": "Date must be in YYYY-MM-DD format",
          }
        ],
        "warnings": []
      }
    ]
  }
}
```

