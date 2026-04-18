# Validation Service

The **Validation Service** is a backend module designed to validate fields or sets of fields extracted from documents. It ensures data consistency, structural correctness, and adherence to predefined field constraints in a document type.

## Overview

Validation service dynamically generates field validators based on the schema of document type. These schemas include the field name, expected data type, constraints (e.g., array length), and other metadata. The service operates at runtime and does **not** require manual configuration for new document types, as validators are auto-generated from field definitions.

### Key Features

- ✅ **Automatic Validator Generation**: Validators are created automatically for each document type upon registration or schema update.
- 🔍 **Field-Level Validation**: Individual field values are validated according to their type and constraints.
- 📦 **Extensible Field Types**: Includes support for complex data structures like arrays, tables, nested types, and metadata constraints.
- 🧪 **Custom Rules Support**: Allows optional inclusion of validation rules for more advanced use cases (though rules may be `null` if unused).

### Usage Flow

1. **Document Processing**
   Document fields are extracted and passed to the Validation Service.

2. **Validator Resolution**
   The service locates the validator for each field based on the document type.

3. **Validation Execution**
   Each field is validated according to its type, constraints, and any custom rules.

4. **Result Reporting**
   A response is returned indicating validation success or failure, along with detailed error messages for invalid fields.


## Validation documentation

1. [Single-field validation](/documentation/high-sparrow/single_field.md) (deprecated)  
2. [Cross-field validation](/documentation/high-sparrow/multi_field.md)  
   2.1. [Rule syntax](/documentation/high-sparrow/rule_syntax.md)  
   2.2. [Built-in functions](/documentation/high-sparrow/built_in_functions.md)  
3. [External validation](/documentation/high-sparrow/external_validators.md)

