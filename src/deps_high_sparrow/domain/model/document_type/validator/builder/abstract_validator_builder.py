from abc import ABC

from .abstract_builder import AbstractBuilder

__all__ = ["AbstractValidatorBuilder"]


class AbstractValidatorBuilder(AbstractBuilder, ABC):
    def is_required(self) -> "AbstractValidatorBuilder":
        self._add_element_to_parent()

        return self._parent.is_required()

    def with_description(self) -> "AbstractValidatorBuilder":
        self._add_element_to_parent()

        return self._parent.with_description()
