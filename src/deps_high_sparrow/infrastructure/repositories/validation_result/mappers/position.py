from typing import Any

from deps_high_sparrow.domain import Position

__all__ = ["PositionMapper"]


class PositionMapper:
    @staticmethod
    def to_dict(position: Position) -> dict[str, Any]:
        return {
            "column": position.column,
            "row": position.row,
            "index": position.index,
            "kv_id": position.kv_id,
        }
