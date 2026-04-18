from abc import ABC, abstractmethod

from .ivalue_unit import ValueUnit

__all__ = ["IExtractionProxy"]


class IExtractionProxy(ABC):
    @abstractmethod
    def get_value_units_from_extracted_data(self, document_id: str) -> list[ValueUnit]:
        ...

    @abstractmethod
    def get_document_artifacts_for_fields(self, document_id: str, field_codes: list[str]) -> list[ValueUnit]:
        ...
