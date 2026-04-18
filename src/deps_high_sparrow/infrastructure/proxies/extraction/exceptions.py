from ..generic import RestClientError

__all__ = ["ExtractionProxyRequestError"]


class ExtractionProxyRequestError(RestClientError):
    code = "extraction_proxy_request_error"

    def __init__(self, error_response: str) -> None:
        super().__init__(f"Error while request to Extraction service. Reason: {error_response}")
