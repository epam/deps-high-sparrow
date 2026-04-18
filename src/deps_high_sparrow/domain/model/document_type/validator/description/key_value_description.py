from typing import Optional

from ....shared import Guard, ImmutableCheck
from ...operand_type import OperandType
from .description import Description
from .generic_description import GenericDescription

__all__ = ["KeyValueDescription"]


class KeyValueDescription(Description):
    key_type = Guard[OperandType](OperandType, ImmutableCheck())
    key_meta = Guard[GenericDescription](GenericDescription, ImmutableCheck())
    value_type = Guard[OperandType](OperandType, ImmutableCheck())
    value_meta = Guard[GenericDescription](GenericDescription, ImmutableCheck())

    def __init__(
        self,
        key_type: OperandType,
        value_type: OperandType,
        key_meta: Optional[GenericDescription] = None,
        value_meta: Optional[GenericDescription] = None,
    ) -> None:
        self.key_type = key_type
        if key_meta is not None:
            self.key_meta = key_meta

        self.value_type = value_type
        if value_meta is not None:
            self.value_meta = value_meta

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.key_type == other.key_type
            and self.key_meta == other.key_meta
            and self.value_type == other.value_type
            and self.value_meta == other.value_meta
        )
