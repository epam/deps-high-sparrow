# Add Custom Validation Rule

‼️ **deprecated** Use [Cross-field validation](/documentation/high-sparrow/multi_field.md) instead.

This endpoint allows you to attach a **custom validation rule** to an existing field validator for a specific document type.

Custom rules enable additional validation logic using Python expressions that reference values of other fields by their unique field codes.

---

## Field Structure

Each field validator includes the following attributes:

| Attribute     | Description |
|---------------|-------------|
| `code`        | Unique field identifier. Typically corresponds to a field in the document. |
| `type`        | Describes the data type of the field. Commonly used types include `array` and `string`. |
| `description` | Contains metadata such as `item_type` (for arrays) and `max_length` constraints. |
| `rules`       | Optional custom rules for the field (can be `null` if not specified). |
| `is_required` | Indicates whether the field is mandatory for the document type. |

## Endpoint

POST /api/v5/document-types/{documentTypeId}/validators/{validatorCode}/rules


- `{documentTypeId}` – ID of the document type.
- `{validatorCode}` – Code of the field validator to which the rule is being added.

---

## Request Body

```json
{
  "name": "string",
  "severity": "warning",
  "rule": "string",
  "issueMessage": "string",
  "description": "",
  "needWarningEvenIfOptional": false,
  "forEach": false,
  "forAny": false,
  "checkOptionalFields": false
}
```

| Field                       | Type      | Required | Description                                                                           |
| --------------------------- | --------- | -------- | ------------------------------------------------------------------------------------- |
| `name`                      | `string`  | Yes      | Human-readable name for the rule.                                                     |
| `severity`                  | `string`  | Yes      | Severity level of the rule. Allowed values: `"warning"`, `"error"`.                   |
| `rule`                      | `string`  | Yes      | Python expression for validation logic. Use `F<fieldCode>` to reference field values. |
| `issueMessage`              | `string`  | Yes      | Message returned if the rule fails.                                                   |
| `description`               | `string`  | No       | Optional description of the rule’s purpose.                                           |
| `needWarningEvenIfOptional` | `boolean` | No       | If `true`, shows a warning even if the field is optional and not present.             |
| `forEach`                   | `boolean` | No       | For array fields: apply rule to each item individually.                               |
| `forAny`                    | `boolean` | No       | For array fields: validation fails only if **all** items fail.                        |
| `checkOptionalFields`       | `boolean` | No       | Reserved for future use. Currently not used.                                          |
