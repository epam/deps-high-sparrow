from ..generic import RestClientError

__all__ = ["ExternalValidationClientError"]


class ExternalValidationClientError(RestClientError):
    code = "external_validation_proxy_request_error"

    def __init__(self, error_response: str) -> None:
        super().__init__(f"Error while request for validation to external service. Reason: {error_response}")
