from typing import Any

from deps_high_sparrow.domain.model import KeyValueDescription, OperandType

from .type_mapping import TYPE_MAPPING

__all__ = ["KeyValueDescriptionMapper"]


class KeyValueDescriptionMapper:
    @staticmethod
    def from_dict(raw_description: dict[str, Any]) -> KeyValueDescription:
        key_type = OperandType(raw_description["key_type"])
        key_type_class = TYPE_MAPPING[key_type]

        value_type = OperandType(raw_description["value_type"])
        value_type_class = TYPE_MAPPING[value_type]

        return KeyValueDescription(
            key_type=key_type,
            key_meta=key_type_class.from_dict(raw_description["key_meta"]),
            value_type=value_type,
            value_meta=value_type_class.from_dict(raw_description["value_meta"]),
        )

    @staticmethod
    def to_dict(description: KeyValueDescription) -> dict[str, Any]:
        key_meta_class = TYPE_MAPPING[description.key_type]
        value_meta_class = TYPE_MAPPING[description.value_type]

        return {
            "key_type": description.key_type.value,
            "key_meta": key_meta_class.to_dict(description.key_meta),
            "value_type": description.value_type.value,
            "value_meta": value_meta_class.to_dict(description.value_meta),
        }
