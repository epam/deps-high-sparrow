from deps_high_sparrow.domain.exceptions import HighSparrowException

__all__ = ["RestClientError"]


class RestClientError(HighSparrowException):
    code = "rest_client_error"
