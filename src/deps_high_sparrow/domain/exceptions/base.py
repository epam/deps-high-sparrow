__all__ = ["HighSparrowException", "NotFoundError", "BusinessException"]


class HighSparrowException(Exception):
    code = "high_sparrow_exception"


class BusinessException(HighSparrowException):
    code = "business_exception"


class NotFoundError(BusinessException):
    code = "not_found_error"
