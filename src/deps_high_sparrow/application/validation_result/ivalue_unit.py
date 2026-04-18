from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from deps_high_sparrow.domain import Value

__all__ = ["ValueUnit"]


@dataclass
class ValueUnit(ABC):
    code: str
    value: Value

    @classmethod
    @abstractmethod
    def from_dict(cls, unit: dict[str, Any]) -> "ValueUnit":
        ...
