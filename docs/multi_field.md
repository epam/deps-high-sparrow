# Cross-Field Validation

Cross-field validation allows defining custom business rules that validate the relationship between multiple fields in a document. These rules are written as Python expressions and executed **without type checks**. If a rule fails, all involved fields will report the same validation error.

This mechanism is useful for enforcing dependencies or conditional logic between fields, such as "If Field A has value X, then Field B must not be empty."

---

## Overview

- Cross-field validators are linked to a document type.

- Each validator contains:

    - A single **Python rule**.
    - A list of **validated fields** that are subject to error highlighting.
    - A list of **dependent fields** which must be referenced in the `issueMessage`.

- If the rule fails, the validation message will be applied to all validated fields.

- Field type is not checked before rule execution.


---

## API: Add Cross-Field Validator

**Endpoint**

```http
POST /api/v5/document-types/{documentTypeId}/cross-field-validator
```

Request Body

```json
{
  "name": "string",                     // Rule name (informational)
  "description": "",                   // Optional rule description
  "rule": "string",                    // Python expression, must evaluate to boolean
  "severity": "warning",               // Can be "warning" or "error"
  "validatedFields": ["fieldA", "fieldB"], // Fields that will display the validation result
  "issueMessage": "Invalid relation between ${fieldA} and ${fieldB}", // Error message (include all dependent fields)
  "dependentFields": ["fieldA", "fieldB"],  // All field codes used inside the rule
  "forEach": false,                    // For array fields: if true - run the rule for each element
  "forAny": false                      // For array fields: if true - fail only if all array elements fail
}
```

If both forEach and forAny are false - the rule is run on array itself


Example Request
```json
{
  "name": "Date Order Validation",
  "description": "Start date must be before end date",
  "rule": "compare_dates(FstartDate, FendDate, op='lt')",
  "severity": "error",
  "validatedFields": ["startDate", "endDate"],
  "issueMessage": "Start date (${startDate}) must be earlier than end date (${endDate})",
  "dependentFields": ["startDate", "endDate"],
  "forEach": false,
  "forAny": false
}
```

## Rule Syntax
Cross-field validation rules use the same syntax as other field-level rules, including access to built-in Python functions and helper methods. Refer to the Built-in Functions and Single field validation documentation for details.

Example Rules

```python
# Rule: If field A is filled, then field B must be filled too
bool(FfieldA) == bool(FfieldB)
```

```python
# Rule: If date in fieldA is before date in fieldB
compare_dates(FfieldA, FfieldB, op="lt")
```

## Important Notes

- validatedFields control which fields are marked as invalid if the rule fails.
- dependentFields must include all field codes referenced in the rule.
- ${fieldCode} placeholders in the issueMessage are automatically substituted with field names.
- forEach and forAny are supported for array fields in the same way as standard validators.


## Use Cases

- Date relationships (e.g., start date < end date)
- Conditional dependencies (e.g., if checkbox is set, text must be filled)
- Field comparison (e.g., amount1 + amount2 must equal total)
