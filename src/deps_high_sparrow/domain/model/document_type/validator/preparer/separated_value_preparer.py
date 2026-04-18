from typing import Any, Optional

from ..validation.dto.prepared_field import BaseData, FieldDataToValidate
from .abstract_preparer import AbstractPreparer

__all__ = ["SeparatedValuePreparer"]


class SeparatedValuePreparer(AbstractPreparer):
    def prepare(self, value: Optional[Any]) -> FieldDataToValidate:
        return FieldDataToValidate(
            document_id=0,
            field_code=self.code(),
            document_type_code="type_code",
            field_type=self.type.type,
            meta=self.type.description,
            data=BaseData(value=value),
            is_required=self.is_required,
        )
