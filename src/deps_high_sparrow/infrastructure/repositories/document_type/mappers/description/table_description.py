from typing import Any

from deps_high_sparrow.domain.model import (
    ColumnDescription,
    OperandType,
    TableDescription,
)

from .type_mapping import TYPE_MAPPING

__all__ = ["TableDescriptionMapper"]


class ColumnDescriptionMapper:
    @staticmethod
    def from_dict(raw_column_description: dict[str, Any]) -> ColumnDescription:
        item_type = OperandType(raw_column_description["item_type"])
        item_type_class = TYPE_MAPPING[item_type]

        return ColumnDescription(
            index=raw_column_description["index"],
            is_required=raw_column_description["is_required"],
            item_type=OperandType(raw_column_description["item_type"]),
            meta=item_type_class.from_dict(raw_column_description["meta"]),
        )

    @staticmethod
    def to_dict(description: ColumnDescription) -> dict[str, Any]:
        item_type_class = TYPE_MAPPING[description.item_type]
        return {
            "index": description.index,
            "is_required": description.is_required,
            "item_type": description.item_type.value,
            "meta": item_type_class.to_dict(description.meta),
        }


class TableDescriptionMapper:
    @staticmethod
    def from_dict(raw_description: dict[str, Any]) -> TableDescription:
        columns_description = [
            ColumnDescriptionMapper.from_dict(column_description) for column_description in raw_description["columns"]
        ]
        return TableDescription(
            columns=columns_description,
        )

    @staticmethod
    def to_dict(description: TableDescription) -> dict[str, Any]:
        columns_description = [
            ColumnDescriptionMapper.to_dict(column_description) for column_description in description.columns
        ]
        return {
            "columns": columns_description,
        }
