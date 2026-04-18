from collections import defaultdict
from typing import Any, DefaultDict

from ....shared import EntityCode
from ...operand_type import OperandType
from ..description import Description
from ..validation.dto.prepared_field import ArrayData, ArrayDataToValidate
from ..validator_type import ValidatorType
from .abstract_preparer import AbstractPreparer
from .key_value_preparer import KeyValuePreparer
from .separated_value_preparer import SeparatedValuePreparer
from .table_preparer import TablePreparer

__all__ = ["ListPreparer"]


class ListPreparer(AbstractPreparer):
    def __init__(self, code: EntityCode, type_: ValidatorType, is_required: bool):
        super().__init__(code, type_, is_required)

        self._preparers: DefaultDict[OperandType, type[AbstractPreparer]] = defaultdict(lambda: SeparatedValuePreparer)
        self._preparers.update(
            {
                OperandType.TABLE: TablePreparer,
                OperandType.DICT: KeyValuePreparer,
            }
        )

    @property
    def item_type(self) -> OperandType:
        return self.type.description.item_type

    @property
    def item_meta(self) -> Description:
        return self.type.description.meta

    @property
    def item_preparer(self) -> AbstractPreparer:
        return self._preparers[self.item_type](
            self.code.for_array_item(),
            ValidatorType(self.item_type, self.item_meta),
            self.is_required,
        )

    def prepare(self, value: Any) -> ArrayDataToValidate:
        return ArrayDataToValidate(
            document_id=0,
            field_code=self.code(),
            document_type_code="type_code",
            field_type=self.type.type,
            meta=self.type.description,
            data=ArrayData(
                items=[self.item_preparer.prepare(item) for item in value] if value is not None else []  # type: ignore
            ),
            is_required=self.is_required,
        )
