from abc import ABC, abstractmethod

from deps_high_sparrow.domain.model import RawIssues

__all__ = ["IExternalValidationProxy"]


class IExternalValidationProxy(ABC):
    @abstractmethod
    def validate_document(
        self,
        external_validator_url: str,
        document_id: str,
        document_type_id: str,
    ) -> list[RawIssues]:
        ...
