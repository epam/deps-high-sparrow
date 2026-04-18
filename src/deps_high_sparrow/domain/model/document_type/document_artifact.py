from typing import Union

from ..shared import EntityCode, Guard, ImmutableCheck

__all__ = ["DocumentArtifact", "Value", "KeyValue", "Base", "Table"]

Base = Union[str, bool, None]

KeyValue = tuple[Base, Base]

Coordinates = tuple[int, int]
Cell = tuple[str, Coordinates]
Table = list[Cell]

List = list[Union[Base, KeyValue, Table]]

Value = Union[Base, KeyValue, Table, List]


class DocumentArtifact:
    code = Guard[EntityCode](EntityCode, ImmutableCheck())

    def __init__(self, code: str, value: Value) -> None:
        self.code = EntityCode(code)
        self.value = value

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value and self.code == other.code
