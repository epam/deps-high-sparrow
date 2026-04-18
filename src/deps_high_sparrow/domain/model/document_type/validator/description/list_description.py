from ....shared import Guard, ImmutableCheck
from ...operand_type import OperandType
from .description import Description

__all__ = ["ListDescription"]


class ListDescription(Description):
    item_type = Guard[OperandType](OperandType, ImmutableCheck())
    meta = Guard[Description](Description, ImmutableCheck())

    def __init__(
        self,
        item_type: OperandType,
        meta: Description,
    ) -> None:
        self.item_type = item_type
        self.meta = meta

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.item_type == other.item_type and self.meta == other.meta
