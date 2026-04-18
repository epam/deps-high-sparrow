from abc import ABC, abstractmethod
from typing import Any, List, Optional, Union

from ...dto.field import ArrayFieldTypeMeta, BasicFieldTypeMeta, StringFieldTypeMeta
from ...dto.prepared_field import BaseDataToValidate
from ...entities.constants import OperandType


class IFieldCasterService(ABC):
    @abstractmethod
    def cast(
        self,
        value: Any,
        field_type: OperandType,
        meta: Optional[Union[ArrayFieldTypeMeta, BasicFieldTypeMeta, StringFieldTypeMeta]] = None,
    ):
        pass

    @abstractmethod
    def cast_field_values(self, fields: List[BaseDataToValidate]) -> List[BaseDataToValidate]:
        pass
