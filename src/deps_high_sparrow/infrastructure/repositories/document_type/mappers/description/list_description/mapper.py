from typing import Any

from deps_high_sparrow.domain.model import ListDescription, OperandType

from .list_type_mapping import LIST_TYPE_MAPPING

__all__ = ["ListDescriptionMapper"]


class ListDescriptionMapper:
    @staticmethod
    def from_dict(raw_description: dict[str, Any]) -> ListDescription:
        item_type = OperandType(raw_description["item_type"])
        item_type_class = LIST_TYPE_MAPPING[item_type]

        return ListDescription(
            item_type=item_type,
            meta=item_type_class.from_dict(raw_description["meta"]),
        )

    @staticmethod
    def to_dict(description: ListDescription) -> dict[str, Any]:
        item_type_class = LIST_TYPE_MAPPING[description.item_type]

        return {
            "item_type": description.item_type.value,
            "meta": item_type_class.to_dict(description.meta),
        }
