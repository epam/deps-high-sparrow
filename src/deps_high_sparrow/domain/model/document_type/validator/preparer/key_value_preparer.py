from typing import Optional

from ..validation.dto.prepared_field import DictData, DictDataToValidate
from ..validator_type import ValidatorType
from .abstract_preparer import AbstractPreparer
from .separated_value_preparer import SeparatedValuePreparer

__all__ = ["KeyValuePreparer"]


class KeyValuePreparer(AbstractPreparer):
    def prepare(self, value: Optional[tuple[str, str]]) -> DictDataToValidate:
        key_preparer = SeparatedValuePreparer(
            self.code.for_key(),
            ValidatorType(self.type.description.key_type, self.type.description.key_meta),
            self.is_required,
        )
        value_preparer = SeparatedValuePreparer(
            self.code.for_value(),
            ValidatorType(self.type.description.value_type, self.type.description.value_meta),
            self.is_required,
        )
        key_item, value_item = value if value is not None else (None, None)

        return DictDataToValidate(
            document_id=0,
            field_code=self.code(),
            document_type_code="type_code",
            field_type=self.type.type,
            meta=self.type.description,
            data=DictData(
                items=(
                    key_preparer.prepare(key_item),
                    value_preparer.prepare(value_item),
                )
            ),
            is_required=self.is_required,
        )
