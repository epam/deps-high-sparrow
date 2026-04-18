from typing import Optional

from ...shared import Guard, ImmutableCheck
from ..operand_type import OperandType
from .description import Description

__all__ = ["ValidatorType"]


class ValidatorType:
    type = Guard[OperandType](OperandType, ImmutableCheck())
    description = Guard[Description](Description, ImmutableCheck())

    def __init__(
        self,
        type: OperandType,
        description: Optional[Description] = None,
    ):
        self.type = type
        if description is not None:
            self.description = description

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.type == other.type and self.description == other.description
