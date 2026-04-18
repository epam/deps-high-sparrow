from typing import Optional

from ....shared import Guard, ImmutableCheck
from ...operand_type import OperandType
from .description import Description
from .generic_description import GenericDescription

__all__ = ["TableDescription", "ColumnDescription"]


class ColumnDescription:
    index = Guard[int](int, ImmutableCheck())
    is_required = Guard[bool](bool, ImmutableCheck())
    item_type = Guard[OperandType](OperandType, ImmutableCheck())
    meta = Guard[GenericDescription](GenericDescription, ImmutableCheck())

    def __init__(
        self,
        index: int,
        is_required: bool,
        item_type: OperandType,
        meta: Optional[GenericDescription] = None,
    ) -> None:
        self.index = index
        self.is_required = is_required
        self.item_type = item_type
        if meta is not None:
            self.meta = meta

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.index == other.index
            and self.is_required == other.is_required
            and self.item_type == other.item_type
            and self.meta == other.meta
        )


class TableDescription(Description):
    columns = Guard[list[ColumnDescription]](list, ImmutableCheck())

    def __init__(self, columns: list[ColumnDescription]) -> None:
        self.columns = columns

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.columns == other.columns
