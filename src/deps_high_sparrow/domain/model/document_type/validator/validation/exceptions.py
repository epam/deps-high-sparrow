class ValidationServiceException(Exception):
    code = "validation_service_exception"


class RuleAlreadyExists(ValidationServiceException):
    code = "rule_already_exists"

    def __init__(self):
        self.msg = "Rule already exists."
        super().__init__(self.msg)


class RuleNotFound(ValidationServiceException):
    code = "rule_not_found"

    def __init__(self, rule_id):
        self.msg = f"Rule with id {rule_id} does not exist."
        super().__init__(self.msg)


class CanNotOverrideName(ValidationServiceException):
    code = "can_not_override_name"

    def __init__(self, forbidden):
        self.msg = f"Cannot override {forbidden}"
        super().__init__(self.msg)


class NameIsNotDefined(ValidationServiceException):
    code = "name_is_not_defined"

    def __init__(self, name):
        self.msg = f"Name '{name}' is not defined"
        super().__init__(self.msg)


class InvalidSyntax(ValidationServiceException):
    code = "invalid_syntax"

    def __init__(self, message):
        self.msg = f"Invalid syntax: {message}"
        super().__init__(self.msg)


class CompareWithOptionalField(ValidationServiceException):
    code = "compare_with_optional_field"

    def __init__(self, name):
        self.msg = f"Optional field {name} without value"
        super().__init__(self.msg)


class InvalidType(ValidationServiceException):
    code = "invalid_type"

    def __init__(self, message):
        self.msg = f"Invalid type: {message}"
        super().__init__(self.msg)


class FieldNotFound(ValidationServiceException):
    code = "field_not_found"

    def __init__(self, field_code, document_type_code):
        self.msg = f"Field with field code {field_code} " f"and document_type_code {document_type_code} does not exist"
        super().__init__(self.msg)


class FieldAlreadyExists(ValidationServiceException):
    code = "field_already_exists"

    def __init__(self, field_code, document_type_code):
        self.msg = f"Field with field code {field_code} and document_type_code {document_type_code} already exist"
        super().__init__(self.msg)


class ValidationResultNotFound(ValidationServiceException):
    code = "validation_results_not_found"

    def __init__(self, document_pk):
        self.msg = f"No validation results for document pk: {document_pk}"
        super().__init__(self.msg)


class ServiceError(ValidationServiceException):
    code = "service_error"

    def __init__(self, service_name, error_response):
        self.msg = f"Error while request to {service_name}. Error: {error_response}"
        super().__init__(self.msg)


class AuthError(ValidationServiceException):
    code = "authentication_error"

    def __init__(self, description):
        self.msg = f"Unauthorized. Error: {description}"
        super().__init__(self.msg)
