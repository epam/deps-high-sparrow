import logging
from concurrent.futures import Future, as_completed

from deps_high_sparrow.domain.model import (
    DocumentType,
    ExternalValidator,
    ExternalValidatorName,
    RawIssues,
)
from deps_high_sparrow.infrastructure.proxies import ExternalValidationClientError
from deps_high_sparrow.shared import ContextSafeThreadPoolExecutor

from .iexternal_validation import IExternalValidationProxy

__all__ = ["ExternalValidationService"]


class ExternalValidationService:
    def __init__(self, external_validation_proxy: IExternalValidationProxy):
        self._external_validation_proxy = external_validation_proxy
        self._logger = logging.getLogger(self.__class__.__name__)

    def perform_validation(self, document_id: str, document_type: DocumentType) -> None:
        external_validators_issues = self._validate_by_external_validators(
            document_id=document_id,
            document_type_id=document_type.id(),
            external_validators=document_type.external_validators,
        )

        document_type.record_external_validation(external_validators_issues)

    def _validate_by_external_validators(
        self, document_id: str, document_type_id: str, external_validators: list[ExternalValidator]
    ) -> dict[ExternalValidatorName, list[RawIssues]]:
        external_validators_issues: dict[ExternalValidatorName, list[RawIssues]] = {}

        with ContextSafeThreadPoolExecutor() as executor:
            futures: dict[Future, ExternalValidatorName] = {}

            for external_validator in external_validators:
                future = executor.submit(
                    self._request_external_validate,
                    external_validator=external_validator,
                    document_id=document_id,
                    document_type_id=document_type_id,
                )
                futures[future] = external_validator.name

            for future in as_completed(futures):
                external_validator_issues = future.result()
                if external_validator_issues is not None:
                    external_validators_issues[futures[future]] = external_validator_issues

        return external_validators_issues

    def _request_external_validate(
        self, external_validator: ExternalValidator, document_id: str, document_type_id: str
    ) -> list[RawIssues]:
        try:
            return self._external_validation_proxy.validate_document(
                external_validator_url=external_validator.url,
                document_id=document_id,
                document_type_id=document_type_id,
            )
        except ExternalValidationClientError as error:
            self._logger.error(
                "Failed to validate document throw external validator `%s`, validation was skipped! Reason: %s",
                external_validator.name,
                error.__class__.__name__,
            )
