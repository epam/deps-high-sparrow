from typing import Any

from deps_high_sparrow.application.validation_result.ivalue_unit import ValueUnit
from deps_high_sparrow.domain.model import Base, KeyValue, Table

__all__ = ["ExtractedDataValueUnit"]

KEY_VALUE_MARKERS = ("key", "value")
TABLE_MARKER = "cells"
GENERIC_DATA_MARKER = "value"
FIRST_ELEMENT = 0


class ExtractedDataValueUnit(ValueUnit):
    @classmethod
    def from_dict(cls, unit: dict[str, Any]) -> "ExtractedDataValueUnit":
        unit_data = unit["data"]

        if isinstance(unit_data, list):
            return cls._from_list(unit)
        elif cls._is_key_value(unit_data):
            return cls._from_key_value_pairs(unit)
        elif cls._is_table(unit_data):
            return cls._from_table(unit)
        elif cls._is_generic_data(unit_data):
            return cls._from_generic_data(unit)

        raise ValueError(f"Unexpected field data: {unit_data}")

    @classmethod
    def _from_generic_data(cls, unit: dict[str, Any]) -> "ExtractedDataValueUnit":
        value = cls._get_value_from_generic_data(unit["data"])

        return cls(code=unit["fieldCode"], value=value)

    @classmethod
    def _from_key_value_pairs(cls, unit: dict[str, Any]) -> "ExtractedDataValueUnit":
        value = cls._get_value_from_key_value_pairs(unit["data"])

        return cls(code=unit["fieldCode"], value=value)

    @classmethod
    def _from_table(cls, unit: dict[str, Any]) -> "ExtractedDataValueUnit":
        value = cls._get_value_from_table(unit["data"])

        return cls(code=unit["fieldCode"], value=value)

    @classmethod
    def _from_list(cls, unit: dict[str, Any]) -> "ExtractedDataValueUnit":
        unit_data = unit["data"]

        if not unit_data:
            raise ValueError("Empty list field data")

        list_item = unit_data[FIRST_ELEMENT]

        if cls._is_key_value(list_item):
            value = [cls._get_value_from_key_value_pairs(kvp) for kvp in unit_data]
        elif cls._is_table(list_item):
            value = [cls._get_value_from_table(table) for table in unit_data]
        elif cls._is_generic_data(list_item):
            value = [cls._get_value_from_generic_data(data) for data in unit_data]

        else:
            raise ValueError(f"Unexpected list field data: {unit_data}")

        return cls(code=unit["fieldCode"], value=value)

    @classmethod
    def _get_value_from_key_value_pairs(cls, unit_data: dict[str, Any]) -> KeyValue:
        key_value = cls._get_value_from_generic_data(unit_data["key"])
        value_value = cls._get_value_from_generic_data(unit_data["value"])

        return key_value, value_value

    @staticmethod
    def _is_key_value(unit_data: dict[str, Any]) -> bool:
        return all(marker in unit_data for marker in KEY_VALUE_MARKERS)

    @staticmethod
    def _is_table(unit_data: dict[str, Any]) -> bool:
        return TABLE_MARKER in unit_data

    @staticmethod
    def _is_generic_data(unit_data: dict[str, Any]) -> bool:
        return GENERIC_DATA_MARKER in unit_data

    @staticmethod
    def _get_value_from_generic_data(unit_data: dict[str, Any]) -> Base:
        return unit_data["value"]

    @staticmethod
    def _get_value_from_table(unit_data: dict[str, Any]) -> Table:
        return [
            (
                cell["value"],
                (
                    cell["coordinates"]["column"],
                    cell["coordinates"]["row"],
                ),
            )
            for cell in unit_data["cells"]
        ]
