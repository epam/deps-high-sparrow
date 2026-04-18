from typing import Literal, Optional

from ...shared import Guard, ImmutableCheck

__all__ = ["Position"]


class Position:
    column = Guard[int](int, ImmutableCheck())
    row = Guard[int](int, ImmutableCheck())
    index = Guard[int](int, ImmutableCheck())
    kv_id = Guard[Literal["key", "value"]](str, ImmutableCheck())

    @classmethod
    def for_cell(cls, column: int, row: int, index: Optional[int] = None) -> "Position":
        position = cls()
        position.column = column
        position.row = row

        if index is not None:
            position.index = index

        return position

    @classmethod
    def for_kv_id(cls, kv_id: Literal["key", "value"], index: Optional[int] = None) -> "Position":
        position = cls()
        position.kv_id = kv_id

        if index is not None:
            position.index = index

        return position

    @classmethod
    def for_list(cls, index: int) -> "Position":
        position = cls()
        position.index = index

        return position
