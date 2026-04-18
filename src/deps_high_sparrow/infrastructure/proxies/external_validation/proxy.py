import logging

from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from deps_high_sparrow.application.validation_result.iexternal_validation import (
    IExternalValidationProxy,
)
from deps_high_sparrow.domain import RawIssues

from ..generic import GenericProxy
from .exceptions import ExternalValidationClientError
from .validation_response_data import ExternalValidatorResponse

__all__ = ["ExternalValidationProxy"]


class ExternalValidationProxy(GenericProxy, IExternalValidationProxy):
    url_suffix = "validate"
    exception = ExternalValidationClientError

    def __init__(self, timeout: int = 60, ssl_verify: bool = False) -> None:
        super().__init__("")
        self._timeout = timeout
        self._ssl_verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def validate_document(
        self,
        external_validator_url: str,
        document_id: str,
        document_type_id: str,
    ) -> list[RawIssues]:
        url = f"{external_validator_url}/{self.url_suffix}"

        request_data = {
            "documentId": document_id,
            "documentTypeId": document_type_id,
        }
        try:
            response = self._session.post(
                url,
                timeout=self._timeout,
                verify=self._ssl_verify,
                json=request_data,
            )

            self._check_response(response)

        except (ConnectionError, Timeout, TooManyRedirects) as request_error:
            self._logger.error("Problem with requesting to external url %s", url)

            raise self.exception(str(request_error))

        return ExternalValidatorResponse.from_raw_response(response.json())
