from typing import TYPE_CHECKING, Union

from ...operand_type import OperandType
from ..validator import Validator
from ..validator_type import ValidatorType
from .abstract_validator_builder import AbstractValidatorBuilder
from .generic_description_builder import GenericDescriptionBuilder
from .key_value_description_builder import KeyValueDescriptionBuilder
from .list_description_builder import ListDescriptionBuilder
from .table_description_builder import TableDescriptionBuilder

if TYPE_CHECKING:
    from ...document_type import DocumentType

__all__ = ["ValidatorBuilder"]

DescriptionBuilder = Union[
    GenericDescriptionBuilder,
    KeyValueDescriptionBuilder,
    TableDescriptionBuilder,
    ListDescriptionBuilder,
]


class ValidatorBuilder(AbstractValidatorBuilder):
    def __init__(self, code: str, type: OperandType, *, parent: "DocumentType") -> None:
        self._code = code
        self._type = type
        self._is_required = False
        self._description = None

        self._parent = parent

    def is_required(self) -> "ValidatorBuilder":
        self._is_required = True

        return self

    def with_description(self) -> DescriptionBuilder:
        if self._type == OperandType.DICT:
            return self._KeyValueDescriptionBuilder(parent=self)

        if self._type == OperandType.TABLE:
            return self._TableDescriptionBuilder(parent=self)

        if self._type == OperandType.ARRAY:
            return self._ListDescriptionBuilder(parent=self)

        return self._GenericDescriptionBuilder(type=self._type, parent=self)

    def _add_to_parent(self) -> None:
        ...

    def _build(self) -> Validator:
        return Validator(
            code=self._code,
            type_=ValidatorType(
                type=self._type,
                description=self._description,
            ),
            is_required=self._is_required,
        )

    class _GenericDescriptionBuilder(GenericDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()

    class _KeyValueDescriptionBuilder(KeyValueDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()

    class _TableDescriptionBuilder(TableDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()

    class _ListDescriptionBuilder(ListDescriptionBuilder):
        def _add_to_parent(self) -> None:
            self._parent._description = self._build()
