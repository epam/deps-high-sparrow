__all__ = [
    "ValidationException",
    "NotFoundError",
    "IllegalArgument",
    "ForbiddenError",
    "AlreadyExistsError",
]


class ValidationException(Exception):
    code = "validation_exception"


class NotFoundError(ValidationException):
    code = "not_found_error"


class IllegalArgument(ValidationException):
    code = "illegal_argument"


class ForbiddenError(ValidationException):
    code = "forbidden_error"


class AlreadyExistsError(ValidationException):
    code = "already_exists_error"
