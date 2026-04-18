from typing import Any

from deps_high_sparrow.domain.model import OperandType, ValidatorType

from .description import (
    TYPE_MAPPING,
    KeyValueDescriptionMapper,
    ListDescriptionMapper,
    TableDescriptionMapper,
)

__all__ = ["ValidatorTypeMapper"]


VALIDATOR_TYPE_DESCRIPTION_MAP = {  # noqa: WPS407
    **TYPE_MAPPING,
    OperandType.DICT: KeyValueDescriptionMapper,
    OperandType.TABLE: TableDescriptionMapper,
    OperandType.ARRAY: ListDescriptionMapper,
}


class ValidatorTypeMapper:
    @staticmethod
    def from_dict(raw_validator_type: dict[str, Any]) -> ValidatorType:
        operand_type = OperandType(raw_validator_type["type"])
        description_class = VALIDATOR_TYPE_DESCRIPTION_MAP[operand_type]
        return ValidatorType(
            type=operand_type,
            description=description_class.from_dict(raw_validator_type["description"]),
        )

    @staticmethod
    def to_dict(validator_type: ValidatorType) -> dict[str, Any]:
        description_class = VALIDATOR_TYPE_DESCRIPTION_MAP[validator_type.type]
        return {
            "type": validator_type.type.value,
            "description": description_class.to_dict(validator_type.description),
        }
