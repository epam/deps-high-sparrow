from abc import ABC, abstractmethod
from typing import Any, Optional

__all__ = ["AbstractBuilder"]


class AbstractBuilder(ABC):
    def __init__(self, *, parent: Optional[Any] = None):
        self._parent = parent

    def build(self) -> Any:
        if self._parent:
            self._add_to_parent()
            return self._parent.build() if isinstance(self._parent, AbstractBuilder) else self._build()

        return self._build()

    @abstractmethod
    def _add_to_parent(self) -> None:
        pass

    def _add_element_to_parent(self) -> None:
        if self._parent is None:
            raise AttributeError("Method not available.")

        self._add_to_parent()

    @abstractmethod
    def _build(self) -> Any:
        pass
