import logging

from deps_high_sparrow.application.validation_result.iextraction import IExtractionProxy

from ..generic import GenericProxy
from .exceptions import ExtractionProxyRequestError
from .value_unit import ExtractedDataValueUnit

__all__ = ["ExtractionProxy"]


class ExtractionProxy(GenericProxy, IExtractionProxy):
    v2_url_suffix = "/api/extraction/v2"
    exception = ExtractionProxyRequestError

    def __init__(self, base_url: str, timeout: int = 60, ssl_verify: bool = False) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._ssl_verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_value_units_from_extracted_data(self, document_id: str) -> list[ExtractedDataValueUnit]:
        url = f"{self._base_url}{self.v2_url_suffix}/extracted-data/{document_id}"

        response = self._session.get(url, timeout=self._timeout, verify=self._ssl_verify)

        self._check_response(response)

        return [ExtractedDataValueUnit.from_dict(field) for field in response.json()["fields"]]

    def get_document_artifacts_for_fields(
        self, document_id: str, field_codes: list[str]
    ) -> list[ExtractedDataValueUnit]:
        url = f"{self._base_url}{self.v2_url_suffix}/extracted-data/{document_id}/fields"
        params = [("fieldCodes", code) for code in field_codes]

        response = self._session.get(url, params=params, timeout=self._timeout, verify=self._ssl_verify)

        self._check_response(response)

        return [ExtractedDataValueUnit.from_dict(field) for field in response.json()]
