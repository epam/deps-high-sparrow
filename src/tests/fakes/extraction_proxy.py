from deps_high_sparrow.application.validation_result.iextraction import IExtractionProxy
from deps_high_sparrow.application.validation_result.ivalue_unit import ValueUnit

__all__ = ["FakeExtractionProxy"]


class FakeExtractionProxy(IExtractionProxy):
    def __init__(self) -> None:
        self._value_units: list[ValueUnit] = []
        self._field_value_units: list[ValueUnit] = []

    def set_value_units(self, value_units: list[ValueUnit]) -> None:
        self._value_units = value_units

    def set_field_value_units(self, value_units: list[ValueUnit]) -> None:
        self._field_value_units = value_units

    def get_value_units_from_extracted_data(self, document_id: str) -> list[ValueUnit]:
        return self._value_units

    def get_document_artifacts_for_fields(self, document_id: str, field_codes: list[str]) -> list[ValueUnit]:
        return self._field_value_units
